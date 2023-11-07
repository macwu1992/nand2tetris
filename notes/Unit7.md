# 2-tier compilation

"Write once, run anywhere." Java uses VM to implement.
Tier 1 is to compile the Java to JVM byte code.
Tier 2 is VM to translate the JVM byte code to machine language on each target platform.

# Stack machine
A stack is maintained in the VM, which has 2 operations:
1. pop (To memory segment location)
2. push (From memory segment location)

These 2 basic operations are performed on stack and memory segments. Values in memory segments are poped or pushed into stack for oprands like ADD, SUB, NEG and etc...

Other operations are like ADD SUB NEG, which ALU supports

# Memory segments for variables
Separate symbols according to its category, which comes from the high level program definition:
1. Static variable
2. Local variable
3. Argument variable
4. constant.
5. this
6. that
7. pointer
8. temp

## How to change values in memory segment?
Quiz:
let static 2 = argument 1
What is the operations in stack machine?

     Stack   argument    local   static  constant
0    _____   ___2_       __-3_    ___2_   _0____
1    __52_   __12_       __982_   __54_   _1____
2    __-3_   __982_      _9862_   __171_  _2____

push argument 1
     Stack       argument    local   static  constant
0    _____       ___2_       __-3_    ___2_   _0____
1    __52_    -  __12_       __982_   __54_   _1____
2    __-3_    |  __982_      _9862_   __171_  _2____
3    __12_  <-|

pop static 2
     Stack   argument    local   static  constant
0    _____   ___2_       __-3_    ___2_   _0____
1    __52_   __12_       __982_   __54_   _1____
2    __-3_   __982_      _9862_   __12_  _2____
3    __12_  -------------------------^

     Stack       argument    local   static  constant
0    _____       ___2_       __-3_    ___2_   _0____
1    __52_    -  __12_       __982_   __54_   _1____
2    __-3_    |  __982_      _9862_   __12_  _2____

# Pointer Manipulation

## Pointer explaination
     Stack
0       _256_   p
1       __52_   q
2       __-3_
3       __-2_
4       __22_
5       __52_
6       __14_
...
...
256     ___1_

Q = *p means Q is assigned to the value where p points to.
p points to 256, so *p will be the content of 256, which means Q = *p = 256

# Implementation of stack
Assumption:
SP is stored in RAM[0], which always points to NEXT available location.
Stack base address = 256

 RAM
0   _258_ SP
1   __12_
2   _____
3   _____
4   ___5_
5   _____
.......
256 _100_
257 _110_
258 _141_
......

Example:
push 17
->

*SP = 17
SP++

Assembly language:
@17
D=A     // D=17
@SP
A=M     // Get the content in SP, and assign the content to A to change the address
M=D     // Change the value of M at A to the value of D
@SP
M=M+1   // The value in SP increase by 1

# VM translator perspetive
(The VM code is operations on VM stacks.)

VM code             VM Translator   Assemly code
push constant i        ===>        *SP = i; SP++

# VM memory segment implementation
## LCL - local variable segment(ARG, THIS, THAT are the same, but with different base address)
Take local variable as example:
LCL is the pointer of local variable memory segment address

 RAM
0   _258_ SP
1   __12_ LCL
2   _____
3   _____
4   ___5_
5   _____
.......
256 _100_
257 _110_
258 _141_
......

VM code:
push local 2
           ^
           |
        offset
====>
address = *LCL + offset(2)
*SP = *address
SP++

Assembly code:
@LCL
A=M+2
D=M
@SP
A=M
M=D
@SP
M=M+1

## Implementing 'constant' segment
push constant i => *SP = i; SP++
NO pop operations on constant

Assembly code:
@i
D=A
@SP
A=M
M=D
@SP
M=M+1

## Implementing 'static' segment
'static' variables are accessiable for all classes, so the variables in it should be in global space. So VM code of 'static' definition is put in a separate file.

Example:
// File Foo.vm
pop static 5
pop static 2

Assembly code:
// D = stack.pop(code omitted)
@Foo.5
M=D
...
// D = stack.pop(code omitted)
@Foo.2
M=D

According to the variable table definition in assembly language, Foo.5 will be stored as RAM[16], and Foo.2 will be stored as RAM[17].

push static 2

Assembly code:
@Foo.2
D=M
@SP
A=M
M=D

## Implementing 'temp' segment
Mapped to 5 to 12, so the base address of 'temp' is 5.

VM code:
push temp i -> *SP = *(5+i); SP++
pop temp i -> SP--; *(5+i) = *SP;

## Implementing 'pointer' segment
0: THIS
1: THAT

VM code:
push pointer 0/1 -> *SP = THIS/THAT; SP++
pop pointer 0/1 -> SP--; THIS/THAT = *SP

# VM implementation
## RAM Mapping
Standard VM mapping on the hack platform
Hack RAM
 RAM
0   _258_   SP
1   __12_   LCL
2   _____   ARG
3   _____   THIS
4   ___5_   THAT
5   _____   temp segment
.......
13   _____  general purpose segment
......
16   _____  static segment
......
256  __100_ Stack
257  __110_
258  __141_
......

## Structure of VM translator
Proposed design:

Parser          Parse the code to lexical elements
CodeWriter      Output the HDL
Main            drives the whole process

Main:
input: fileName.vm
output: fileName.asm