# Instructions for running gem5

## Preparations

```bash
# go to home folder
mkdir Research # skip if already have

## config gem5
cd ~/Research
git clone git@github.com:CSAGroupUIC/ywang-gem5.git # find the repository you need
cd ywang-gem5 # enter the folder
git checkout targetREF # checkout to the branch you need
scons -j12 build/X86/gem5.opt # build gem5

## config CPU2006
cd /tmp # enter share space
cp -r CPU2006 ~/Research/CPU2006 # skip if already have

## config python script
cd ~/Research
git clone git@github.com:CSAGroupUIC/Scripts.git # skip if already have
```

## For test run

```bash
cd ~/Research/Scripts/Gem5Scripts
python3 submitJobs.py ywang-gem5 refreshSim.py 401
## this line means use python3 to execute the python script submitJobs.py
## For submitJobs.py, it needs to specify the gem5 executable folder, the configuration scripts and the workload. If no workload specify, it will run all the workloads.
```

The simulation instruction number is 5M predefined in **refreshSim.py**. If you wish to simulate more or less instructions, you can modify the code on line 75 of **refreshSim.py**.

## For normal debugging

1. Set debug flags in the gem5 code and rebuild the gem5.opt.
2. You need to specify your own debug flag inside **refreshSim.py**. For example, you wish to see the print out message of **DRAMPower**. You need to substitute line 76 of **refreshSim.py** to **options.flags = "DRAMPower**.
3. Test run and see the print out message.

## For gdb debug

```bash
cd ~/Research/ywang-gem5 # enter the gem5 folder you wish to debug
git checkout targetREF # checkout to your branch
scons build/X86/gem5.debug # build the debug version of gem5 to work with gdb
gdb build/X86/gem5.debug -h # get used to the gem5 debug help options first

cd ~/Research/Scripts/Gem5Scripts/
gdb ~/Research/ywang-gem5/build/X86/gem5.debug # open the gdb
# after gdb initialize
run refreshSim.py --binary=401 --argument=8000ns
# you can setup gbd options here
```
