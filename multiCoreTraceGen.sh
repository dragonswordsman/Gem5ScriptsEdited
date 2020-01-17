#!/bin/bash
# Modify this setting in different machine
home=~/Gem4Refresh

############ DIRECTORY VARIABLES: MODIFY ACCORDINGLY #############
GEM5=$home/gem5                            # Install location of gem5
SPEC=~/Research/cpu2006/benchspec/CPU2006       # Install location of SPEC2006 benchmarks
SIMPOINT=~/Research/simpoint			           # Install location of simpoit
OUTPUT=$home/traceOut                       # Output directory
SCRIPT=$home/script/                       # File log for this script's stdout henceforth
##################################################################
bench=$1 # First variable in commandline
simpts=$20000000 # Seconde variable in commandline with interval lenght 10M

cd $OUTPUT
if [ -d "$bench" ]; then
    echo "====================Folder \"$bench\" Existed================"
else
    mkdir $bench
    echo "====================Folder \"$bench\" Created================"
fi
runscript=$OUTPUT/$bench/runscript.log
echo "=======================Shell Script Starts=========================" | tee $runscript
date                            | tee -a $runscript
echo "Author: Yicheng Wang"     | tee -a $runscript
echo "Email: ywang271@uic.edu"  | tee -a $runscript
echo " "|                       tee -a $runscript
echo " "|                       tee -a $runscript

#######################Benchmark List#############################
bzip2="401" 
gcc="403"
bwaves="410"
gamess="416"
mcf="429"
milc="433"
zeusmp="434"
gromacs="435"
cactusADM="436"
leslie3d="437"
namd="444"
gobmk="445"
soplex="450"
povray="453"
calculix="454"
hmmer="456"
sjeng="458"
GemsFDTD="459"
libquantum="462"
h264ref="464"
tonto="465"
lbm="470"
omnetpp="471"
astar="473"
wrf="481"
sphinx3="482"
xalancbmk="483"
specrandint="998"
specrandfp="999"
##################################################################



################## REPORT SCRIPT CONFIGURATION ###################
echo "====================== Hardcoded directories ========================"   | tee -a $runscript
echo "GEM5:                                         $GEM5"          | tee -a $runscript
echo "SPEC:                                         $SPEC"          | tee -a $runscript
echo "SIMPOINT:                                     $SIMPOINT"      | tee -a $runscript
echo "OUTPUT:                                       $OUTPUT"        | tee -a $runscript
echo "SCRIPT                                        $SCRIPT"        | tee -a $runscript
echo "====================================================================="   | tee -a $runscript
##################################################################


#####################Benchmark Selection###########################
#perlbench AND dealII do not work

#bzip2
if [ "$bench" == "$bzip2" ] || [ "$bench" == "bzip2" ]; then
    DIR=$SPEC/401.bzip2/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=bzip2_base.amd64-m64-gcc42-nn
    OPTION="chicken.jpg 30"
fi
#gcc
if [ "$bench" == "$gcc" ] || [ "$bench" == "gcc" ]; then
    DIR=$SPEC/403.gcc/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=gcc_base.amd64-m64-gcc42-nn
    OPTION="166.i -o 166.s"
fi
#bwaves
if [ "$bench" == "$bwaves" ] || [ "$bench" == "bwaves" ]; then
    DIR=$SPEC/410.bwaves/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=bwaves_base.amd64-m64-gcc42-nn
    OPTION=""
fi
#gamess
if [ "$bench" == "$gamess" ] || [ "$bench" == "gamess" ]; then
    DIR=$SPEC/416.gamess/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=gamess_base.amd64-m64-gcc42-nn
    OPTION=" "
    INPUT="cytosine.2.config"
fi
#mcf
if [ "$bench" == "$mcf" ] || [ "$bench" == "mcf" ]; then
    DIR=$SPEC/429.mcf/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=mcf_base.amd64-m64-gcc42-nn
    OPTION="inp.in"
fi
#milc
if [ "$bench" == "$milc" ] || [ "$bench" == "milc" ]; then
    DIR=$SPEC/433.milc/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=milc_base.amd64-m64-gcc42-nn
    OPTION=""
    INPUT="su3imp.in"
fi
#zeusmp
if [ "$bench" == "$zeusmp" ] || [ "$bench" == "zeusmp" ]; then
    DIR=$SPEC/434.zeusmp/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=zeusmp_base.amd64-m64-gcc42-nn
    OPTION=" "
fi
#gromacs
if [ "$bench" == "$gromacs" ] || [ "$bench" == "gromacs" ]; then
    DIR=$SPEC/435.gromacs/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=gromacs_base.amd64-m64-gcc42-nn
    OPTION="-silent -deffnm gromacs.tpr -nice 0 "
fi
#cactusADM
if [ "$bench" == "$cactusADM" ] || [ "$bench" == "cactusADM" ]; then
    DIR=$SPEC/436.cactusADM/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=cactusADM_base.amd64-m64-gcc42-nn
    OPTION=" benchADM.par"
fi
#leslie3d
if [ "$bench" == "$leslie3d" ] || [ "$bench" == "leslie3d" ]; then
    DIR=$SPEC/437.leslie3d/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=leslie3d_base.amd64-m64-gcc42-nn
    OPTION=""
    INPUT="leslie3d.in"
fi
#namd
if [ "$bench" == "$namd" ] || [ "$bench" == "namd" ]; then
    DIR=$SPEC/444.namd/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=namd_base.amd64-m64-gcc42-nn
    OPTION=" --input namd.input --iterations 38"
fi
#gobmk
if [ "$bench" == "$gobmk" ] || [ "$bench" == "gobmk" ]; then
    DIR=$SPEC/445.gobmk/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=gobmk_base.amd64-m64-gcc42-nn
    OPTION=" --quiet --mode gtp "
    INPUT="13x13.tst"
fi
#soplex
if [ "$bench" == "$soplex" ] || [ "$bench" == "soplex" ]; then
    DIR=$SPEC/450.soplex/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=soplex_base.amd64-m64-gcc42-nn
    OPTION=" -m3500 ref.mps"
fi
#povray
if [ "$bench" == "$povray" ] || [ "$bench" == "povray" ]; then
    DIR=$SPEC/453.povray/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=povray_base.amd64-m64-gcc42-nn
    OPTION=" SPEC-benchmark-ref.ini"
fi
#calculix
if [ "$bench" == "$calculix" ] || [ "$bench" == "calculix" ]; then
    DIR=$SPEC/454.calculix/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=calculix_base.amd64-m64-gcc42-nn
    OPTION=" -i hyperviscoplastic"
fi
#hmmer
if [ "$bench" == "$hmmer" ] || [ "$bench" == "hmmer" ]; then
    DIR=$SPEC/456.hmmer/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=hmmer_base.amd64-m64-gcc42-nn
    OPTION=" nph3.hmm swiss41"
fi
#sjeng
if [ "$bench" == "$sjeng" ] || [ "$bench" == "sjeng" ]; then
    DIR=$SPEC/458.sjeng/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=sjeng_base.amd64-m64-gcc42-nn
    OPTION="ref.txt"
fi
#GemsFDTD
if [ "$bench" == "$GemsFDTD" ] || [ "$bench" == "GemsFDTD" ]; then
    DIR=$SPEC/459.GemsFDTD/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=$DIR/GemsFDTD_base.amd64-m64-gcc42-nn
    OPTION=""
fi
#libquantum
if [ "$bench" == "$libquantum" ] || [ "$bench" == "libquantum" ]; then
    DIR=$SPEC/462.libquantum/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=$DIR/libquantum_base.amd64-m64-gcc42-nn
    OPTION=" 1297 8"
fi
#h264ref
if [ "$bench" == "$h264ref" ] || [ "$bench" == "h264ref" ]; then
    DIR=$SPEC/464.h264ref/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=h264ref_base.amd64-m64-gcc42-nn
    OPTION=" -d foreman_ref_encoder_baseline.cfg"
fi
#tonto
if [ "$bench" == "$tonto" ] || [ "$bench" == "tonto" ]; then
    DIR=$SPEC/465.tonto/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=tonto_base.amd64-m64-gcc42-nn
    OPTION=" "
fi
#lbm
if [ "$bench" == "$lbm" ] || [ "$bench" == "lbm" ]; then
    DIR=$SPEC/470.lbm/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=lbm_base.amd64-m64-gcc42-nn
    OPTION=" 3000 reference.dat 0 0 100_100_130_ldc.of"
fi
#omnetpp can't open omnetpp.ini
if [ "$bench" == "$omnetpp" ] || [ "$bench" == "omnetpp" ]; then
    DIR=$SPEC/471.omnetpp/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=omnetpp_base.amd64-m64-gcc42-nn
    OPTION="omnetpp.ini"
fi
#astar
if [ "$bench" == "$astar" ] || [ "$bench" == "astar" ]; then
    DIR=$SPEC/473.astar/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=astar_base.amd64-m64-gcc42-nn
    OPTION="rivers.cfg"
fi
#wrf
if [ "$bench" == "$wrf" ] || [ "$bench" == "wrf" ]; then
    DIR=$SPEC/481.wrf/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=wrf_base.amd64-m64-gcc42-nn
    OPTION=" "
fi
#sphinx3 
if [ "$bench" == "$sphinx3" ] || [ "$bench" == "sphinx3" ]; then
    DIR=$SPEC/482.sphinx3/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=sphinx_livepretend_base.amd64-m64-gcc42-nn
    OPTION=" ctlfile . args.an4"
fi
#xalancbmk
if [ "$bench" == "$xalancbmk" ] || [ "$bench" == "xalancbmk" ]; then
    DIR=$SPEC/483.xalancbmk/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=Xalan_base.amd64-m64-gcc42-nn
    OPTION=" -v test.xml xalanc.xsl"
fi
#specrandint
if [ "$bench" == "$specrandint" ] || [ "$bench" == "specrandint" ]; then
    DIR=$SPEC/998.specrand/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=$DIR/specrand_base.amd64-m64-gcc42-nn
    OPTION=" 1255432124 234923"
fi
#specrandfp
if [ "$bench" == "$specrandfp" ] || [ "$bench" == "specrandfp" ]; then
    DIR=$SPEC/999.specrand/run/run_base_ref_amd64-m64-gcc42-nn.0000
    EXE=$DIR/specrand_base.amd64-m64-gcc42-nn
    OPTION=" 1255432124 234923"
fi
##################################################################

program="$EXE;$EXE;$EXE;$EXE"
option="$OPTION;$OPTION;$OPTION;$OPTION"


echo " "| tee -a $runscript
echo " "| tee -a $runscript
echo "==========================Gem5 Starts========================" | tee -a $runscript
cd $DIR
        $GEM5/build/X86/gem5.opt\
        --debug-flags=ECC\
        --debug-file=$1_multi_core_trace.gz\
        --outdir=$OUTPUT/$1\
        $GEM5/configs/example/se.py\
        --num-cpus=4\
        --cmd=$program\
        --option="$option"\
        --checkpoint-dir=$OUTPUT/$1/mergeChpts\
        --maxinsts=1000000000\
        --cpu-type=DerivO3CPU\
        --mem-type=DDR4_2400_16x4\
        --mem-channels=1\
        --mem-ranks=1\
        --mem-size=8GB\
        --caches\
        --l2cache\
        | tee -a $runscript
echo "=======================Gem5 Ended=========================" | tee -a $runscript


echo " "|                       tee -a $runscript
echo " "|                       tee -a $runscript       
echo "=======================Shell Script Ends=========================" | tee -a $runscript
date    

