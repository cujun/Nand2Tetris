load Drinks.hdl,
output-file Drinks.out,
compare-to Drinks.cmp,
output-list juice%B3.1.3 water%B3.1.3 wine%B3.1.3 out%B3.1.3 ;
set juice 0,
set water 0,
set wine 0,
eval,
output;

set juice 1,
set water 0,
set wine 0,
eval,
output;

set juice 0,
set water 1,
set wine 0,
eval,
output;

set juice 1,
set water 1,
set wine 0,
eval,
output;

set juice 0,
set water 0,
set wine 1,
eval,
output;

set juice 1,
set water 0,
set wine 1,
eval,
output;

set juice 0,
set water 1,
set wine 1,
eval,
output;

set juice 1,
set water 1,
set wine 1,
eval,
output;

