@256
D=A
@SP
M=D
@Sys.init$return0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// GOTO Sys.init
@Sys.init
0;JMP
(Sys.init$return0)
(Class1.set)
// PUSH ARGUMENT 0
@0
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// POP STATIC 0
@SP
M=M-1
@SP
A=M
D=M
@Class1.0
M=D
// PUSH ARGUMENT 1
@1
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// POP STATIC 1
@SP
M=M-1
@SP
A=M
D=M
@Class1.1
M=D
// PUSH CONSTANT 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Class1.get)
// PUSH STATIC 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH STATIC 1
@Class1.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// SUB
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Sys.init)
// PUSH CONSTANT 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// PUSH CONSTANT 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class1.set$return1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// GOTO Class1.set
@Class1.set
0;JMP
(Class1.set$return1)
// POP TEMP 0
@0
D=A
@5
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// PUSH CONSTANT 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// PUSH CONSTANT 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class2.set$return2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// GOTO Class2.set
@Class2.set
0;JMP
(Class2.set$return2)
// POP TEMP 0
@0
D=A
@5
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
@Class1.get$return3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// GOTO Class1.get
@Class1.get
0;JMP
(Class1.get$return3)
@Class2.get$return4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// GOTO Class2.get
@Class2.get
0;JMP
(Class2.get$return4)
(Sys.init$WHILE)
// GOTO Sys.init$WHILE
@Sys.init$WHILE
0;JMP
(Class2.set)
// PUSH ARGUMENT 0
@0
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// POP STATIC 0
@SP
M=M-1
@SP
A=M
D=M
@Class2.0
M=D
// PUSH ARGUMENT 1
@1
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// POP STATIC 1
@SP
M=M-1
@SP
A=M
D=M
@Class2.1
M=D
// PUSH CONSTANT 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Class2.get)
// PUSH STATIC 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// PUSH STATIC 1
@Class2.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// SUB
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret
A=M
0;JMP