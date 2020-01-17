# !/usr/local/bin/python3
#
# This script is used to configurate the gem5 simulation options.
# Author: Yicheng Wang
# Date: 04/10/2019
#
# All rights reserved.

import os
import subprocess
import re
from pathlib import Path



class Gem5Config(object):
    """
    TestGem5(gem5DirName) -> class
    gem5DirName specify the name or path of gem5 directory
    """
    def __init__(self,gem5DirName):
        self.home = str(Path.home()) + '/Research'
        self.gem5Dir = f'{self.home}/{gem5DirName}'
        self.gem5 = f'{self.gem5Dir}/build/X86/gem5.opt'
        self.outputDir = f'--outdir={self.gem5Dir}/m5out'
        self.script = f'{self.gem5Dir}/configs/example/se.py'


    def setDebugFlag(self,debugFlags):
        """
        Set gem5 simulation debug flag.
        """
        # assert(len(self.args)==1),"debugFlags should be set first of all"
        self.debugFlags = f'--debug-flags={debugFlags}'
        # self.debugFiles = f'--debug-file={debugFlags}_trace.gz'


    def setDebugFiles(self,debugFiles):
        """
        Set gem5 simulation debugfile name. Must set debug flag first
        """
        assert(self.debugFlags),"Set debugFlags first."
        self.debugFiles = f'--debug-file={debugFiles}_trace.gz'


    def setOutputDir(self,outputDir,addon=None):
        """
        setOutputDir(self,outputDir,addon=None)
        self.outputDir = f'--outdir={self.home}/outputs/{outputDir}'
        self.ckptsDir = f'{self.home}/outputs/{outputDir}'
        Set gem5 simulation output directory path
        """
        self.outputDir = f'--outdir={self.home}/outputs/{outputDir}'
        self.ckptsDir = f'{self.home}/outputs/{outputDir}'
        if addon:
            self.outputDir += f'/{addon}'
            self.ckptsDir += f'/{addon}'


    def setScript(self,script):
        """
        Set gem5 simulation configuration script file path
        """
        self.script = f'{script}'


    def runSimulation(self,addon=None):
        """
        run minimal gem5 simulation configuration
        """
        workload = f'--cmd={self.gem5Dir}/tests/test-progs'\
            '/hello/bin/x86/linux/hello'
        args = [self.gem5]

        try:
            args.append(self.debugFlags)
        except:
            pass
        try:
            args.append(self.debugFiles)
        except:
            pass

        args.extend([self.outputDir,self.script,workload])

        args.extend(addon)
        subprocess.run(args)


class ScriptConfig(Gem5Config):
    """
    ScriptConfig() -> class
    Set detailed se.py options for gem5 simulation
    Memory configuraiton must be specified carefully.
    The memory configuration will influence the checkpoints
    """

    # Memory configurations
    mem_type = '--mem-type=DDR4_2400_16x4'
    mem_channles = '--mem-channels=2'
    mem_ranks = '--mem-ranks=2'
    mem_size = '--mem-size=16GB'
    # warning: device size not match. can be ignored
    # 16x4 configuration suitable for server DRAM with ECC
    mem_config = [mem_type,mem_channles,mem_ranks,mem_size]

    # CPU configurations
    cpu_type = '--cpu-type=DerivO3CPU'
    # np is short for number of processors
    np = 1
    num_cpus = f'--num-cpus={np}'
    cpu_clock = '--cpu-clock=3GHz'
    # when cpu is out of order must have cache
    caches = '--caches'
    l2cache = '--l2cache'
    cpu_config = [cpu_type,num_cpus,cpu_clock,caches,l2cache]

    # Cache configurations
    # detailed cache configuration is not vital for some tasks
    l1d_size = '--l1d_size=32kB'
    l1i_size = '--l1i_size=32kB'
    l1d_assoc = '--l1d_assoc=8'
    l1i_assoc = '--l1i_assoc=8'
    l2_size = '--l2_size=256kB'
    l2_assoc = '--l2_assoc=4'
    cacheline_size = '--cacheline_size=64'
    cache_config = []

    def setMEM(self,type,channel,rank,size):
        self.mem_type = f'--mem-type={type}'
        self.mem_channles = f'--mem-channels={channel}'
        self.mem_ranks = f'--mem-ranks={rank}'
        self.mem_size = f'--mem-size={size}GB'

        self.mem_config = [self.mem_type,self.mem_channles,\
            self.mem_ranks,self.mem_size]

    def setCPU(self,cpu,num=1,clock=3):
        """
        Set cpu type, number of cpus and the clock
        """
        self.cpu_type = f'--cpu-type={cpu}'
        self.np = num
        self.num_cpus = f'--num-cpus={num}'
        self.cpu_clock = f'--cpu-clock={clock}GHz'

        self.cpu_config = [self.cpu_type,self.num_cpus,\
            self.cpu_clock,self.caches,self.l2cache]

    def setCache(self,addon=None):
        """
        Add more options for cache configurations
        """
        self.cache_config = [self.l1d_size,self.l1i_size,\
            self.l1d_assoc,self.l1i_assoc,self.l2_size,\
            self.l2_assoc,self.cacheline_size]
        if addon:
            self.cache_config.append(addon)

    def resetCache(self):
        """
        Clear cache setting
        """
        self.cache_config = []

    def setWorkload(self,bench):
        """
        bench is an input of class CPU2006(object)
        Set workload options for the configuration script
        """
        wrkld = CPU2006(bench)
        self.program = f'--cmd={wrkld.name}'
        self.option = f'--option={wrkld.option}' if wrkld.option else None
        self.input = f'--input={wrkld.input}' if wrkld.input else None
        self.wrkldDir = f'{self.home}{wrkld.dir}'
        self.simpt = wrkld.simpt

        for _ in range(self.np - 1):
            self.program += f';{wrkld.name}'
            if self.option:
                self.option += f';{wrkld.option}'
            if self.input:
                self.input += f';{wrkld.input}'

        self.binary = []
        self.binary.append(self.program)
        if self.option:
            self.binary.append(self.option)
        if self.input:
            self.binary.append(self.input)
        assert('' not in self.binary), "Wrong bench configurations"
        self.setOutputDir(bench)


    def setPARA(self,prob,tAttack="0ns"):
        """
        prob -> float, tAttack -> str
        setPARA() add options for para
        """
        self.prob = f'--para={prob}'
        self.tAttack = f'--tAttack={tAttack}'
        self.paraConfig = [self.prob,self.tAttack]


    def takeCheckpoints(self,insts):
        """
        Add options for taking checkpoint
        """
        assert(self.np == 1), "Only single core allowed while take ckpts"
        assert(self.program), "Must set program before take ckpts"
        at_inst = '--at-instruction'
        take_ckpts = f'--take-checkpoints={insts}'
        config = [at_inst,take_ckpts]
        return self.compound(config)


    def takeSimptCkpt(self):
        """
        Add options for taking checkpoint
        """
        return self.takeCheckpoints(int(self.simpt*1e7))


    def restoreCheckpoint(self,insts,maxinsts,merge=False):
        """
        Add options for restore from checkpoints
        """
        assert(self.program), "Must set program before restore ckpts"
        at_inst = '--at-instruction'
        if merge:
            assert(self.np > 1), "While using merge chkpts,\
                 numer of cpu should larger than 1"
            ckpts_dir = f'--checkpoint-dir={self.ckptsDir}/mergeCkpts'
        else:
            ckpts_dir = f'--checkpoint-dir={self.ckptsDir}'
        ckpts_restore = f'--checkpoint-restore={insts}'
        maxinsts = f'--maxinsts={maxinsts}'
        config = [at_inst,ckpts_dir,ckpts_restore,maxinsts]
        try:
            config.extend(self.paraConfig)
        except:
            pass
        return self.compound(config)



    def compound(self,addon):
        """
        Override the runSimulation in Gem5Config()
        Take arguments to specify task
        This version is more comprehensive.
        """

        # Set current working directory
        os.chdir(self.wrkldDir)

        # append script first, others can't be gem5's argument
        args = [self.gem5]
        try:
            args.append(self.debugFlags)
        except:
            pass
        try:
            args.append(self.debugFiles)
        except:
            pass
        args.extend([self.outputDir,self.script])
        # append binary configuration
        args.extend(self.binary)
        # append memory configuration
        args.extend(self.mem_config)
        # append cpu configuration
        args.extend(self.cpu_config)
        # append cache configuration
        if self.cache_config:
            args.extend(self.cache_config)
        # other task will call this function with more options
        args.extend(addon)
        # subprocess.run(args)
        return args


    ### useful tools
    def mergeCheckpoints(self,insts):
        args = ['python']
        script = f'{self.gem5Dir}/util/checkpoint_aggregator.py'
        args.append(script)
        outdir = f'{self.ckptsDir}/mergeCkpts/cpt.None.{insts}'
        args.extend(['-o',outdir])
        ckpts = f'{self.ckptsDir}/cpt.None.{insts}'
        args.append('--cpts')
        for _ in range(self.np):
            args.append(ckpts)
        size = int(re.findall(r'\d{1,3}',self.mem_size)[0])* pow(1024,3)
        args.extend(['--memory-size',str(size)])
        subprocess.run(args)


    def simulate(self,args):
        subprocess.run(args)

class CPU2006(object):
    """
    CPU2006() -> class
    Set CPU2005 benchmarks configurations for gem5 simulation
    """
    def __init__(self,bench):
        """
        Initialize the benchmark instance with its name
        """
        if bench in ['400','perlbenc']:
            ret = ['perlbench','400.perlbench',\
                '-I./lib diffmail.pl 4 800 10 17 19 300']
            simpt = 8646

        elif bench in ['401', 'bzip2']:
            ret = ['bzip2','401.bzip2','chicken.jpg 30']
            simpt = 3978

        elif bench in ['403', 'gcc']:
            ret = ['gcc','403.gcc','166.i -o 166.s']
            simpt = 5681

        elif bench in ['410', 'bwaves']:
            ret = ['bwaves','410.bwaves']
            simpt = 195834

        elif bench in ['416','gamess']:
            ret = ['gamess','416.gamess','', 'cytosine.2.config']
            simpt = 52844

        elif bench in ['429', 'mcf']:
            ret = ['mcf','429.mcf','inp.in']
            simpt = 24182

        elif bench in ['433', 'milc']:
            ret = ['milc','433.milc','','su3imp.in']
            simpt = 42171

        elif bench in ['434', 'zeusmp']:
            ret = ['zeusmp','434.zeusmp']
            simpt = 143391

        elif bench in ['435', 'gromacs']:
            ret = ['gromacs','435.gromacs',\
                '-silent -deffnm gromacs.tpr -nice 0']
            simpt = 73566

        elif bench in ['436', 'cactusADM']:
            ret = ['cactusADM','436.cactusADM','benchADM.par']
            simpt = 41811

        elif bench in ['437', 'leslie3d']:
            ret = ['leslie3d','437.leslie3d','','leslie3d.in']
            simpt = 102866

        elif bench in ['444', 'namd']:
            ret = ['namd','444.namd','--input namd.input --iterations 38']
            simpt = 14239

        elif bench in ['445', 'gobmk']:
            ret = ['gobmk','445.gobmk','--quiet --mode gtp','13x13.tst']
            simpt = 2922

        elif bench in ['450','soplex']:
            ret = ['soplex','450.soplex','-m3500 ref.mps']
            simpt = 3988

        elif bench in ['453', 'povray']:
            ret = ['povray','453.povray','SPEC-benchmark-ref.ini']
            simpt = 61412

        elif bench in ['454', 'calculix']:
            ret = ['calculix','454.calculix','-i hyperviscoplastic']
            simpt = 210709

        elif bench in ['456', 'hmmer']:
            ret = ['hmmer','456.hmmer','nph3.hmm swiss41']
            simpt = 6286

        elif bench in ['458', 'sjeng']:
            ret = ['sjeng','458.sjeng','ref.txt']
            simpt = 134141

        elif bench in ['459', 'GemsFDTD']:
            ret = ['GemsFDTD','459.GemsFDTD']
            simpt = 131941

        elif bench in ['462', 'libquantum']:
            ret = ['libquantum','462.libquantum','1297 8']
            simpt = 41938

        elif bench in ['464', 'h264ref']:
            ret = ['h264ref','464.h264ref',\
                '-d foreman_ref_encoder_baseline.cfg']
            simpt = 4289

        elif bench in ['465', 'tonto']:
            ret = ['tonto','465.tonto']
            simpt = 23

        elif bench in ['470', 'lbm']:
            ret = ['lbm','470.lbm','3000 reference.dat 0 0 100_100_130_ldc.of']
            simpt = 1820

        elif bench in ['471', 'omnetpp']:
            ret = ['omnetpp','471.omnetpp','omnetpp.ini']
            simpt = 34112
            raise ValueError("Can't run in simulation.")

        elif bench in ['473', 'astar']:
            ret = ['astar','473.astar','rivers.cfg']
            simpt = 18680

        elif bench in ['481','wrf']:
            ret = ['wrf','481.wrf']
            raise ValueError("Can't run in simulation.")

        elif bench in ['482', 'sphinx3']:
            ret = ['sphinx_livepretend','482.sphinx3','ctlfile . args.an4']
            self.simpt = 1110

        elif bench in ['483','xalancbmk']:
            ret = ['xalancbmk','483.xalancbmk','-v test.xml xalanc.xsl']
            raise ValueError("Can't build.")

        else:
            raise ValueError("Wrong bench name.")

        self.name = f'{ret[0]}_base.amd64-m64-gcc41-nn'
        self.dir = f'/CPU2006/{ret[1]}'\
            '/run/run_base_ref_amd64-m64-gcc41-nn.0000'
        self.option = ret[2] if len(ret) > 2 else None
        self.input = ret[3] if len(ret) == 4 else None
        self.simpt = simpt


