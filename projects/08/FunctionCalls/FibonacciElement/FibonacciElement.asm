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
(Main.fibonacci)
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
    @2
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    A=A-1
    D=D-M
    @GT1_IN
    D;JGT
    D=0
    @GT1_OUT
    0;JMP
(GT1_IN)
    D=-1
(GT1_OUT)
    @SP
    A=M-1
    M=D
    @SP
    AM=M-1
    D=M
    @Main.fibonacci$IF_TRUE
    D;JNE
    @Main.fibonacci$IF_FALSE
    0;JMP
(Main.fibonacci$IF_TRUE)
    @0
    D=A
    @ARG
    A=D+M
    D=M
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
(Main.fibonacci$IF_FALSE)
    @0
    D=A
    @ARG
    A=D+M
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @2
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    A=A-1
    M=M-D
    @RET2_Main.fibonacci
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
    @1
    D=D-A
    @5
    D=D-A
    @ARG
    M=D
    @Main.fibonacci
    0;JMP
(RET2_Main.fibonacci)
    @0
    D=A
    @ARG
    A=D+M
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @1
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    AM=M-1
    D=M
    A=A-1
    M=M-D
    @RET3_Main.fibonacci
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
    @1
    D=D-A
    @5
    D=D-A
    @ARG
    M=D
    @Main.fibonacci
    0;JMP
(RET3_Main.fibonacci)
    @SP
    AM=M-1
    D=M
    A=A-1
    M=D+M
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
    @4
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @RET4_Main.fibonacci
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
    @1
    D=D-A
    @5
    D=D-A
    @ARG
    M=D
    @Main.fibonacci
    0;JMP
(RET4_Main.fibonacci)
(Sys.init$WHILE)
    @Sys.init$WHILE
    0;JMP
