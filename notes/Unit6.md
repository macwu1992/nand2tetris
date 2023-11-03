# Questions
- What language does the assembler is writen?
In this course, Java/C/C++ is used, but what is the first assembler programmed with?
Nowadays, people just use disctinct computer to write assemblers for developing platforms and convert or cross-compile it to binary code, and burn it into ROM of the platform.

But the first assembler must be written in machine language.

- How the assembly program compiled and loaded?

- How symbols are processed?
There are 3 categories of symbols:
1. Pre-defined symbols
Use a pre-defined table to map symbols to binary values.
1. Label symbols
Create a table to store lable characters and the line number it is representing.
1. Variable symbols
Any symbol that is not found in pre-defined or lable symbol defined table, is variable symbol.
Every symbol is given with a unique memory address, starting from 16. (16 is an arbitary value, which can be any value)
Eg:
i   16
sum 17
... etc
Policy to handle to variable symbol:
1. First time seeing the symbol, allocate memory space, staring with 16.
2. In the later context of program, if the value is updated, go to related position in memory and update; if the value is referenced, just look up address 16 to find the value of a symbol.

# Whole process of the assembly program
To parse the symbols, just to look up the symbol table.

The process can be devided into 2 parts.

Plus: Symbol table is a table that mapping symbol characters to their memory address counterpart.

1. First pass
Put pre-defined symbols and its pre-defined memory address into symbol table.
Put label symbols and its memory address(line number) into symbol table.

2. Second pass
Any other symbols that are not seen in symbol table are variable symbols. Thus, put them in symbol tables, starting from 16.