// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/rect/Rect.asm

// Draws a rectangle at the top-left corner of the screen.
// The rectangle is 16 pixels wide and R0 pixels high.

   @0               // comment
   D=M
   @INFINITE_LOOP               // comment
   D;JLE 
   @counter
   M=D
   @SCREEN
   D=A
   @address
   M=D
   M=D  M=D
(LOOP)              // ok ok ok // comment // ok ok:as[faqwojr1935ut9ew0sgkm
   @address
   A=M
   A=MO
   A=D             /                         /
   M=-1//is it comment?
   @address
   D=M
   @32
   D=D+A// yeah
   @0       / / This is error comment
   @0/          // This is error
   @address
   M=D
   @counter
   MD=M-1
   @LOOP
   D;JGT
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP
