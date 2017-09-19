load Food.hdl,
output-file Food.out,
compare-to Food.cmp,
output-list bread%B3.1.3 noodles%B3.1.3 potatoes%B3.1.3 out%B3.1.3 ;
set bread 0,
set noodles 0,
set potatoes 0,
eval,
output;

set bread 1,
set noodles 0,
set potatoes 0,
eval,
output;

set bread 0,
set noodles 1,
set potatoes 0,
eval,
output;

set bread 1,
set noodles 1,
set potatoes 0,
eval,
output;

set bread 0,
set noodles 0,
set potatoes 1,
eval,
output;

set bread 1,
set noodles 0,
set potatoes 1,
eval,
output;

set bread 0,
set noodles 1,
set potatoes 1,
eval,
output;

set bread 1,
set noodles 1,
set potatoes 1,
eval,
output;

