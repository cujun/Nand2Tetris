load Nand2.hdl,
output-file Nand2.out,
compare-to Nand2.cmp,
output-list x%B3.1.3 y%B3.1.3 out%B3.1.3 ;
set x 0,
set y 0,
eval,
output;

set x 1,
set y 0,
eval,
output;

set x 0,
set y 1,
eval,
output;

set x 1,
set y 1,
eval,
output;

