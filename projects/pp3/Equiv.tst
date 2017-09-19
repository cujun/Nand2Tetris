load Equiv.hdl,
output-file Equiv.out,
compare-to Equiv.cmp,
output-list inA%B3.1.3 inB%B3.1.3 out%B3.1.3 ;
set inA 0,
set inB 0,
eval,
output;

set inA 1,
set inB 0,
eval,
output;

set inA 0,
set inB 1,
eval,
output;

set inA 1,
set inB 1,
eval,
output;

