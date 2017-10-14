    @24544 // bottom-left pixel
    D=A
    @addr
    M=D
    @3 // 0x0003
    D=A
    @val
    M=D
(DRAW_LOOP)
    @val
    D=M
    @addr
    A=M
    AM=D // draw
    AD=D+A
    D=D+A // D=D<<2
    @NOT_OVERFLOW
    D;JNE
    @addr
    M=M+1
    @3 // 0x0003
    D=A
(NOT_OVERFLOW)
    @val
    M=D
    @32 // 0x0010
    D=A
    @addr
    MD=M-D
    @16384 // @SCREEN
    D=D-A
    @DRAW_LOOP
    D;JGE
(INFINITE_LOOP)
    @INFINITE_LOOP
    0;JMP
