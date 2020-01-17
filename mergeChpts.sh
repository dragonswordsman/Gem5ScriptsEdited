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

chpts=~/Research/gem5out/checkpoints/

echo "-------------------checkpoint combine---------------------" | tee -a $runscript

cd $GEM5/util
    python checkpoint_aggregator.py\
    -o $OUTPUT/$1/mergeChpt\
    --cpts $chpts/$1/cpt.None.$simpts $chpts/$1/cpt.None.$simpts $chpts/$1/cpt.None.$simpts $chpts/$1/cpt.None.$simpts\
    --memory-size 8\
    | tee -a $runscript

echo " "|                       tee -a $runscript
echo " "|                       tee -a $runscript       
echo "=======================Shell Script Ends=========================" | tee -a $runscript
date    
