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

// n = 512 * 256 / 16 = 8192
    @8192
    D=A
    @n
    M=D
(LOOP)
    @KBD
    D=M
    @WHITE
    D;JEQ

  // BLACK START
    @i
    M=0
(LOOP_BLACK)
    @i
    D=M
    @n
    D=D-M
    @LOOP
    D;JEQ

    @SCREEN
    D=A
    @i
    A=D+M
    M=-1
    @i
    M=M+1
    @LOOP_BLACK
    0;JMP
    // BLACK END

    @LOOP
    0;JMP 
(WHITE)
    // WHITE START
    @i
    M=0
(LOOP_WHITE)
    @i
    D=M
    @n
    D=D-M
    @LOOP
    D;JEQ

    @SCREEN
    D=A
    @i
    A=D+M
    M=0
    @i
    M=M+1
    @LOOP_WHITE
    0;JMP
    // WHITE END

    @LOOP
    0;JMP

//   @SCREEN
//   D=A
//   @cursor
//   M=D
// 
//   @8192 // 256 x 32 (rows x 16-bit words)
//   D=A
//   @SCREEN
//   D=D+A
//   @size
//   M=D
// 
// (LOOP)
//   @KBD
//   D=M
//   @WHITE
//   D;JEQ
//   @BLACK
//   0;JMP
// 
// (WHITE)
//   @color
//   M=0
//   @FILL
//   0;JMP
// 
// (BLACK)
//   @color
//   M=-1
//   @FILL
//   0;JMP
// 
// (FILL)
//   @color
//   D=M
//   @cursor
//   A=M
//   M=D
//   @cursor
//   M=M+1
//   D=M
//   @size
//   D=D-M
//   @RESETCURSOR
//   D;JGT
//   @LOOP
//   0;JMP
// 
// (RESETCURSOR)
//   @SCREEN
//   D=A
//   @cursor
//   M=D
//   @LOOP
//   0;JMP
