    @R2
    M=0
    @counter
    MD=1
(LOOP)
    @R1
    D=D&M
    @READY
    D;JEQ
    @R0
    D=M
    @R2
    M=D+M
(READY)
    @R0
    D=M
    M=D+M
    @counter
    D=M
    MD=D+M
    @LOOP
    D;JNE
(INFINITE_LOOP)
    @INFINITE_LOOP
    0;JMP
