# CPU2006 Benchmarks Build Status

|   | Bench  |  SPEC Build  |Real Machine  | Gem5 Simulator| Category |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1  | 400.perlbench    | S | S  | S  | SPECint |
| 2  | 401.bizp2        | S | S  | S  | SPECint |
| 3  | 403.gcc          | S | S  | S  | SPECint |
| 4  | 410.bwaves       | S | S  | S  | SPECfp |
| 5  | 416.gamess       | S | S  | S  | SPECfp |
| 6  | 429.mcf          | S | S  | S  | SPECint |
| 7  | 433.milc         | S | S  | S  | SPECfp |
| 8  | 434.zeusmp       | S | S  | S  | SPECfp |
| 9  | 435.gromacs      | S | S  | S  | SPECfp |
| 10  | 436.cactusADM   | S | S  | S  | SPECfp |
| 11  | 437.leslie3d    | S | S  | S  | SPECfp |
| 12  | 444.namd        | S | S  | S  | SPECfp |
| 13  | 445.gobmk       | S | S  | S  | SPECint |
| 14  | 447.dealII      | NR |   |   | SPECfp |
| 15  | 450.soplex      | S | S  | S  | SPECfp |
| 16  | 453.povray      | S | S  | S  | SPECfp |
| 17  | 454.calculix    | S | S  | S  | SPECfp |
| 18  | 456.hmmer       | S | S  | S  | SPECint |
| 19  | 458.sjeng       | S | S  | S  | SPECint |
| 20  | 459.GemsFDTD    | S | S  | S  | SPECfp |
| 21  | 462.libquantum  | S | S  | S  | SPECint |
| 22  | 464.h264ref     | S | S  | S  | SPECint |
| 23  | 465.tonto       | S | S  | S  | SPECfp |
| 24  | 470.lbm         | S | S  | S  | SPECfp |
| 25  | 471.omnetpp     | S | S  | F  | SPECint |
| 26  | 473.astar       | S | S  | S  | SPECint |
| 27  | 481.wrf         | NR |   |   | SPECfp |
| 28  | 482.sphinx3     | S | S  | S  | SPECfp |
| 29  | 483.xalancbmk   | NR |   |   | SPECfp |

## Build Platform

Ubuntu 12.04 in the Virtual Machine

## Conclusions on Jan 21, 2019

There are 26 benchmarks can be succefully built.
And 26 of them can succefully excute on real machine (X86_64). Bench 471.omnetpp 
will encounter gem5 segmentation fault.
However, there are only 25 benchmarks can excute on Gem5 simulator.
We might need SPEC binaries other than SPEC CPU2006.