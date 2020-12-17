// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// n = -R1 if R1 < 0 else R1
    @R1
    D=M
    @R1_LESS_THAN_ZERO_0
    D;JLT
    @n
    M=D
    @END_N
    0;JMP
(R1_LESS_THAN_ZERO_0)
    @n
    M=-D
(END_N)

// mul = 0
    @mul
    M=0
// i = 0
    @i
    M=0

(LOOP)
    @i
    D=M
    @n
    D=D-M
    @END_LOOP
    D;JEQ

    // mul = mul + R0
    @mul
    D=M
    @R0
    D=D+M
    @mul
    M=D
    // i = i + 1
    @i
    M=M+1
    @LOOP
    0;JMP
(END_LOOP)
    @R1
    D=M
    @R1_LESS_THAN_ZERO_1
    D;JLT
    @mul
    D=M
    @R2
    M=D
    @END
    0;JMP
(R1_LESS_THAN_ZERO_1)
    @mul
    D=M
    @R2
    M=-D

(END)
    @END
    0;JMP
