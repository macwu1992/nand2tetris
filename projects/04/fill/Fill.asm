// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@24576
D=A
@END_PIXEL
M=D

(LISTEN_KEY_LOOP)
    @SCREEN
    D=A
    @address
    M=D

    @KBD
    D=M

    @BLACKENS_SCREEN
    D;JGT

    @WHITENS_SCREEN
    D;JEQ

    @LISTEN_KEY_LOOP
    0;JMP

(WHITENS_SCREEN)
    @address
    D=M
    @END_PIXEL
    D=M-D
    @LISTEN_KEY_LOOP
    D;JEQ

    @address
    A=M
    M=0
    @address
    M=M+1

    @WHITENS_SCREEN
    0;JMP

(BLACKENS_SCREEN)
    @address
    D=M
    @END_PIXEL
    D=M-D
    @LISTEN_KEY_LOOP
    D;JEQ

    @address
    A=M
    M=-1
    @address
    M=M+1

    @BLACKENS_SCREEN
    0;JMP