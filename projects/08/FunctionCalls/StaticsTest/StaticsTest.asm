    @256
    D=A
    @SP
    M=D
    @RET0_Sys.init
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @LCL
    M=D
    @5
    D=D-A
    @ARG
    M=D
    @Sys.init
    0;JMP
(RET0_Sys.init)
(Class1.set)
    @SP
    A=M
    D=A
    @SP
    M=D
    @0
    D=A
    @ARG
    A=D+M
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    @Class1.0
    M=D
    @1
    D=A
    @ARG
    A=D+M
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    @Class1.1
    M=D
    @0
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @R13
    M=D
    @5
    A=D-A
    D=M
    @R14
    M=D
    @SP
    A=M-1
    D=M
    @ARG
    A=M
    M=D
    D=A+1
    @SP
    M=D
    @R13
    D=M-1
    @R15
    AM=D
    D=M
    @THAT
    M=D
    @R15
    AM=M-1
    D=M
    @THIS
    M=D
    @R15
    AM=M-1
    D=M
    @ARG
    M=D
    @R15
    AM=M-1
    D=M
    @LCL
    M=D
    @R14
    A=M
    0;JMP
(Class1.get)
    @SP
    A=M
    D=A
    @SP
    M=D
    @Class1.0
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @Class1.1
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    A=A-1
    M=M-D
    @LCL
    D=M
    @R13
    M=D
    @5
    A=D-A
    D=M
    @R14
    M=D
    @SP
    A=M-1
    D=M
    @ARG
    A=M
    M=D
    D=A+1
    @SP
    M=D
    @R13
    D=M-1
    @R15
    AM=D
    D=M
    @THAT
    M=D
    @R15
    AM=M-1
    D=M
    @THIS
    M=D
    @R15
    AM=M-1
    D=M
    @ARG
    M=D
    @R15
    AM=M-1
    D=M
    @LCL
    M=D
    @R14
    A=M
    0;JMP
(Sys.init)
    @SP
    A=M
    D=A
    @SP
    M=D
    @6
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @8
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @RET1_Class1.set
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @LCL
    M=D
    @2
    D=D-A
    @5
    D=D-A
    @ARG
    M=D
    @Class1.set
    0;JMP
(RET1_Class1.set)
    @0
    D=A
    @R5
    D=D+A
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D
    @23
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @15
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @RET2_Class2.set
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @LCL
    M=D
    @2
    D=D-A
    @5
    D=D-A
    @ARG
    M=D
    @Class2.set
    0;JMP
(RET2_Class2.set)
    @0
    D=A
    @R5
    D=D+A
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D
    @RET3_Class1.get
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @LCL
    M=D
    @0
    D=D-A
    @5
    D=D-A
    @ARG
    M=D
    @Class1.get
    0;JMP
(RET3_Class1.get)
    @RET4_Class2.get
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @LCL
    M=D
    @0
    D=D-A
    @5
    D=D-A
    @ARG
    M=D
    @Class2.get
    0;JMP
(RET4_Class2.get)
(Sys.init$WHILE)
    @Sys.init$WHILE
    0;JMP
(Class2.set)
    @SP
    A=M
    D=A
    @SP
    M=D
    @0
    D=A
    @ARG
    A=D+M
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    @Class2.0
    M=D
    @1
    D=A
    @ARG
    A=D+M
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    @Class2.1
    M=D
    @0
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @R13
    M=D
    @5
    A=D-A
    D=M
    @R14
    M=D
    @SP
    A=M-1
    D=M
    @ARG
    A=M
    M=D
    D=A+1
    @SP
    M=D
    @R13
    D=M-1
    @R15
    AM=D
    D=M
    @THAT
    M=D
    @R15
    AM=M-1
    D=M
    @THIS
    M=D
    @R15
    AM=M-1
    D=M
    @ARG
    M=D
    @R15
    AM=M-1
    D=M
    @LCL
    M=D
    @R14
    A=M
    0;JMP
(Class2.get)
    @SP
    A=M
    D=A
    @SP
    M=D
    @Class2.0
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @Class2.1
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    A=A-1
    M=M-D
    @LCL
    D=M
    @R13
    M=D
    @5
    A=D-A
    D=M
    @R14
    M=D
    @SP
    A=M-1
    D=M
    @ARG
    A=M
    M=D
    D=A+1
    @SP
    M=D
    @R13
    D=M-1
    @R15
    AM=D
    D=M
    @THAT
    M=D
    @R15
    AM=M-1
    D=M
    @THIS
    M=D
    @R15
    AM=M-1
    D=M
    @ARG
    M=D
    @R15
    AM=M-1
    D=M
    @LCL
    M=D
    @R14
    A=M
    0;JMP