import argparse
from pathlib import Path

# Parser
# Code
# SymbolTable
# Main

class Parser:
    blockCommentFlag = False
    labelSymbolCount = 0
    variableSymbolReg = 16

    preDefinedSymbolTable = {
        'R0':       '0',
        'R1':       '1',
        'R2':       '2',
        'R3':       '3',
        'R4':       '4',
        'R5':       '5',
        'R6':       '6',
        'R7':       '7',
        'R8':       '8',
        'R9':       '9',
        'R10':      '10',
        'R11':      '11',
        'R12':      '12',
        'R13':      '13',
        'R14':      '14',
        'R15':      '15',
        'SCREEN':   '16384',
        'KBD':      '25476',
        'SP':       '0',
        'LCL':      '1',
        'ARG':      '2',
        'THIS':     '3',
        'THAT':     '4'
        }
    
    labelSymbolTable = {}

    variableSymbolTable = {}

    def parseLines(__self__, lines):
        parsedLines = [__self__.parse(l) for l in lines]

        if (__self__.blockCommentFlag):
            raise Exception('Syntax error: ' + 'no ending in block comment.')

        return parsedLines

    def parse(__self__, line):
        line = str(line)

        # process '/n'
        if (line == '\n'):
            line = ''

        # process comments //
        if (line.startswith('//')):
            line = ''

        # process block comments starter /*
        if (line.startswith('/*') and line.endswith('*/\n')):
            line = ''

        if (line.startswith('/*') and not line.endswith('*/\n')):
            __self__.blockCommentFlag = True
            line = ''

        # process block comments ender */
        if (line.endswith('*/\n') and __self__.blockCommentFlag):
            __self__.blockCommentFlag = False
            line = ''

        if(__self__.blockCommentFlag):
            line = ''

        if(line.__contains__('//')):
            line = line.split('//')[0]

        line = line.strip()

        if(not line == ''):
            line = line + '\n'

        return line

    def codeLines(__self__, lines):
        linesWithoutSymbol = [__self__.codeBasicInstructions(lineNumber, lines[lineNumber]) for lineNumber in range(len(lines))]
        linesWithoutSymbol = [l for l in linesWithoutSymbol if l != '']

        linesLabelSymbol = [__self__.recordLableSymbol(lineNumber, linesWithoutSymbol[lineNumber]) for lineNumber in range(len(linesWithoutSymbol))]
        linesLabelSymbol = [l for l in linesLabelSymbol if l != '']

        linesAllSymbol = [__self__.recordVarSymbol(lineNumber, linesLabelSymbol[lineNumber]) for lineNumber in range(len(linesLabelSymbol))]
        linesAllSymbol = [l for l in linesAllSymbol if l != '']

        linesWithSymbol = [__self__.codeSymbol(lineNumber, linesAllSymbol[lineNumber]) for lineNumber in range(len(linesAllSymbol))]
        linesWithSymbol = [l for l in linesWithSymbol if l != '']

        return linesWithSymbol

    def codeBasicInstructions(__self__, lineNumber, line):
        line = str(line)
        line = line.replace('\n', '')

        if (line.startswith('@')):
            # A-instruction
            line = __self__.codeAInstruction(lineNumber, line)
        elif (line.__contains__('=') or line.__contains__(';')):
            # C-instruction
            line = __self__.codeCInstruction(lineNumber, line)
        elif (line == ''):
            # ignore the comments
            pass
        elif (line.startswith('(') and line.endswith(')')):
            # ignore the label symbols
            line = line
        else:
            raise Exception('Syntax error; Invalid expressions. Line: ' + str(lineNumber + 1))

        return line

    def codeAInstruction(__self__, lineNumber, line):
        line = line.replace('@', '')
        line = line.replace('\n', '')

        binaryValue = ''
        if (line.isdigit()):
            try:
                binaryValue = '{0:016b}'.format(int(line))
                if (binaryValue.startswith('1')):
                    raise Exception('Exceeding max 16-bit value. Line: ' + str(lineNumber + 1))

                line = str(binaryValue)
            except Exception:
                raise Exception('Syntax error; invalid value for A-instruction. Line: ' + str(lineNumber + 1))
        else:
            # Could be variable symbols, keep it as it is
            line = '@' + line

        return line

    def codeCInstruction(__self__, lineNumber, line):
        destStr = ''
        compStr = ''
        jmpStr = ''

        # Little endian
        finalValue = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1]

        compTable = {
            '0':[0,1,0,1,0,1], # 0
            '1': [1,1,1,1,1,1], # 1
            '-1': [0,1,0,1,1,1], # -1
            'D': [0,0,1,1,0,0], # D
            'A': [0,0,0,0,1,1], # A or M
            'M': [0,0,0,0,1,1], # A or M
            '!D': [1,0,1,1,0,0], # !D
            '!A': [1,0,0,0,1,1], # !A or !M
            '!M': [1,0,0,0,1,1], # !A or !M
            '-D': [1,1,1,1,0,0], # -D
            '-A': [1,1,0,0,1,1], # -A or -M
            '-M': [1,1,0,0,1,1], # -A or -M
            'D+1': [1,1,1,1,1,0], # D+1
            'A+1': [1,1,1,0,1,1], # A+1 or M+1
            'M+1': [1,1,1,0,1,1], # A+1 or M+1
            'D-1': [0,1,1,1,0,0], # D-1
            'A-1': [0,1,0,0,1,1], # A-1 or M-1
            'M-1': [0,1,0,0,1,1], # A-1 or M-1
            'D+A': [0,1,0,0,0,0], # D+A or D+M
            'D+M': [0,1,0,0,0,0], # D+A or D+M
            'D-A': [1,1,0,0,1,0], # D-A or D-M
            'D-M': [1,1,0,0,1,0], # D-A or D-M
            'A-D': [1,1,1,0,0,0], # A-D or M-D
            'M-D': [1,1,1,0,0,0], # A-D or M-D
            'D&A': [0,0,0,0,0,0], # D&A or D&M
            'D&M': [0,0,0,0,0,0], # D&A or D&M
            'D|A': [1,0,1,0,1,0],  # D|A or D|M
            'D|M': [1,0,1,0,1,0]  # D|A or D|M
        }

        jumpTable = {
            'JGT': [1,0,0],
            'JEQ': [0,1,0],
            'JGE': [1,1,0],
            'JLT': [0,0,1],
            'JNE': [1,0,1],
            'JLE': [0,1,1],
            'JMP': [1,1,1]
        }

        # Transcode dest finalValue[3:5]
        if (line.__contains__('=') and line.__contains__(';')):
            raise Exception('Sytax error; Invalid C-instruction with both \'=\' and \';\'' + str(lineNumber + 1))

        if (line.__contains__('=')):
            destValue = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            # dest definition
            if (line.startswith('=')):
                raise Exception('Sytax error; Destination must be assigned before \'=\'. Line: ' + str(lineNumber + 1))

            if (line.endswith('=\n')):
                raise Exception('Sytax error; Computation must be assigned after \'=\'. Line: ' + str(lineNumber + 1))

            destStr = line.split('=')[0]

            if destStr.__contains__('M'):
                destValue[3] = 1
            if destStr.__contains__('D'):
                destValue[4] = 1
            if destStr.__contains__('A'):
                destValue[5] = 1

            finalValue = [a | b for a, b in zip(finalValue, destValue)]

            compStr = line.split('=')[1]
        else:
            # no dest defined keep destValue as b'0000000000000000'
            pass

        if (line.__contains__(';')):

            if (line.startswith(';')):
                raise Exception('Syntax error; no computation defined in C-instructions. Line: ' + str(lineNumber + 1))

            if (line.endswith(';')):
                raise Exception('Syntax error; no jump defined in C-instructions. Line: ' + str(lineNumber + 1))

            compStr = line.split(';')[0]
            jmpStr = line.split(';')[1].replace('\n', '')

            # Transcode jump finalValue[0:2]
            if (jmpStr == ''):
                pass

            if (not jumpTable.keys().__contains__(jmpStr)):
                raise Exception('Syntax error; Invalid jump expression. Line: ' + str(lineNumber + 1))

            finalValue[0:3] = jumpTable[jmpStr]

        if (not line.__contains__('=') and not line.__contains__(';')):
            compStr = line

        if (len(compStr) == 0):
            raise Exception('Syntax error; Computation expression required. Line: ' + str(lineNumber + 1))

        # Transcode comp finalValue[6:11]
        if (compStr.__contains__('A') and compStr.__contains__('M')):
                raise Exception('Syntax error; Invalid computation expression in C-Instruction. Line: ' + str(lineNumber + 1))

        if (compStr.__contains__('A')):
            finalValue[12] = 0

        if (compStr.__contains__('M')):
            finalValue[12] = 1

        compStr = compStr.replace('\n', '')

        if (not compTable.keys().__contains__(compStr)):
            raise Exception('Syntax error; Invalid computation expression. Line: ' + str(lineNumber + 1))

        finalValue[6:12] = compTable[compStr]

        finalValue.reverse()
        line = ''.join([str(value) for value in finalValue])

        return line

    def recordLableSymbol(__self__, lineNumber, line):
        if (line.startswith('(') and line.endswith(')')):
            line = line.replace('(', '').replace(')', '')
            __self__.labelSymbolTable[line] = str(lineNumber - __self__.labelSymbolCount)
            __self__.labelSymbolCount += 1
            line = ''

        return line

    def recordVarSymbol(__self__, lineNumber, line):
        if (line.startswith('@')):
            line = line.replace('@', '')
            if (not __self__.preDefinedSymbolTable.keys().__contains__(line) and
                not __self__.labelSymbolTable.keys().__contains__(line) and 
                not __self__.variableSymbolTable.keys().__contains__(line)):

                __self__.variableSymbolTable[line] = str(__self__.variableSymbolReg)
                __self__.variableSymbolReg += 1

            line = '@' + line

        return line

    def codeSymbol(__self__, lineNumber, line):
        if (line.startswith('@')):
            line = line.replace('@', '')
            if (not __self__.preDefinedSymbolTable.keys().__contains__(line) and
                not __self__.labelSymbolTable.keys().__contains__(line) and 
                not __self__.variableSymbolTable.keys().__contains__(line)):
                raise Exception('Syntax error; Symbol not defined: ' + line)

            if (__self__.preDefinedSymbolTable.keys().__contains__(line)):
                line = '@' + __self__.preDefinedSymbolTable[line]
                line = __self__.codeAInstruction(line=line, lineNumber=0)

            if (__self__.labelSymbolTable.keys().__contains__(line)):
                line = '@' + __self__.labelSymbolTable[line]
                line = __self__.codeAInstruction(line=line, lineNumber=0)

            if (__self__.variableSymbolTable.keys().__contains__(line)):
                line = '@' + __self__.variableSymbolTable[line]
                line = __self__.codeAInstruction(line=line, lineNumber=0)

        return line

def main(filePath):
    if (filePath is None):
        raise FileNotFoundError

    file = Path(filePath)

    if (not file.is_absolute()):
        file = Path(Path(__file__).parent / filePath)

    if (not file.exists()):
        raise FileExistsError('File not exist: ' + filePath)
    
    if (not file.suffix.endswith('.asm')):
        raise Exception('.asm File type required: ' + filePath)

    file = file.absolute()

    lines = []
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()

    parser = Parser()
    instructionLines = parser.parseLines(lines)
    codedInstructionLines = parser.codeLines(instructionLines)
    codedInstructionLines = [l + '\n' for l in codedInstructionLines]

    instructionFile = file.with_suffix('.hack')
    with open(instructionFile, 'w+', encoding='utf-8') as f:
        f.writelines(codedInstructionLines)
        f.close()

    if (not instructionFile.exists()):
        raise Exception('Failed to create file: ' + str(instructionFile))

if __name__ == '__main__':
    fileParser = argparse.ArgumentParser(description='Transcoding .asm files to machine binary code')
    fileParser.add_argument('filePath', metavar='File', help='A file path.')
    args = fileParser.parse_args()
    filePath = args.filePath
    main(filePath)