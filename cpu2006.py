import os
class CPU2006(object):
    """
    CPU2006() -> class
    Set CPU2005 benchmarks configurations for gem5 simulation
    """
    def __init__(self,bench):
        """
        Initialize the benchmark instance with its name
        """
        head = os.path.expanduser("~/Research/CPU2006/")
        tail = '/run/run_base_ref_amd64-m64-gcc41-nn.0000/'
        if bench in ['400','perlbench']:
            ret = ['perlbench','400.perlbench',\
                '-I./lib diffmail.pl 4 800 10 17 19 300']
            self.simpt = 8646

        elif bench in ['401', 'bzip2']:
            ret = ['bzip2','401.bzip2','chicken.jpg 30']
            self.simpt = 3078


        elif bench in ['403', 'gcc']:
            ret = ['gcc','403.gcc','166.i -o 166.s']
            self.simpt = 5681

        elif bench in ['410', 'bwaves']:
            ret = ['bwaves','410.bwaves']
            # self.simpt = 195834
            self.simpt = 88

        elif bench in ['416','gamess']:
            ret = ['gamess','416.gamess','', 'cytosine.2.config']
            self.simpt = 52844

        elif bench in ['429', 'mcf']:
            ret = ['mcf','429.mcf','inp.in']
            self.simpt = 24182


        elif bench in ['433', 'milc']:
            ret = ['milc','433.milc','','su3imp.in']
            self.simpt = 42171

        elif bench in ['434', 'zeusmp']:
            ret = ['zeusmp','434.zeusmp']
            # self.simpt = 143391
            self.simpt = 88

        elif bench in ['435', 'gromacs']:
            ret = ['gromacs','435.gromacs',\
                '-silent -deffnm gromacs.tpr -nice 0']
            # self.simpt = 73566
            self.simpt = 88


        elif bench in ['436', 'cactusADM']:
            ret = ['cactusADM','436.cactusADM','benchADM.par']
            self.simpt = 41811

        elif bench in ['437', 'leslie3d']:
            ret = ['leslie3d','437.leslie3d','','leslie3d.in']
            self.simpt = 102866

        elif bench in ['444', 'namd']:
            ret = ['namd','444.namd','--input namd.input --iterations 38']
            self.simpt = 14239

        elif bench in ['445', 'gobmk']:
            ret = ['gobmk','445.gobmk','--quiet --mode gtp','13x13.tst']
            self.simpt = 2922

        elif bench in ['450','soplex']:
            ret = ['soplex','450.soplex','-m3500 ref.mps']
            self.simpt = 3988

        elif bench in ['453', 'povray']:
            ret = ['povray','453.povray','SPEC-benchmark-ref.ini']
            self.simpt = 61412

        elif bench in ['454', 'calculix']:
            ret = ['calculix','454.calculix','-i hyperviscoplastic']
            # self.simpt = 210709
            self.simpt = 88


        elif bench in ['456', 'hmmer']:
            ret = ['hmmer','456.hmmer','nph3.hmm swiss41']
            self.simpt = 6286

        elif bench in ['458', 'sjeng']:
            ret = ['sjeng','458.sjeng','ref.txt']
            # self.simpt = 134141
            self.simpt = 88

        elif bench in ['459', 'GemsFDTD']:
            ret = ['GemsFDTD','459.GemsFDTD']
            # self.simpt = 131941
            self.simpt = 88

        elif bench in ['462', 'libquantum']:
            ret = ['libquantum','462.libquantum','1297 8']
            self.simpt = 41938

        elif bench in ['464', 'h264ref']:
            ret = ['h264ref','464.h264ref',\
                '-d foreman_ref_encoder_baseline.cfg']
            self.simpt = 4289

        elif bench in ['465', 'tonto']:
            ret = ['tonto','465.tonto']
            self.simpt = 23

        elif bench in ['470', 'lbm']:
            ret = ['lbm','470.lbm','3000 reference.dat 0 0 100_100_130_ldc.of']
            self.simpt = 1820

        elif bench in ['471', 'omnetpp']:
            ret = ['omnetpp','471.omnetpp','omnetpp.ini']
            self.simpt = 34112

        elif bench in ['473', 'astar']:
            ret = ['astar','473.astar','rivers.cfg']
            self.simpt = 18680

        elif bench in ['481','wrf']:
            raise ValueError("Can't run in simulation.")
            # ret = ['wrf','481.wrf']
            # self.simpt = 228382

        elif bench in ['482', 'sphinx3']:
            ret = ['sphinx_livepretend','482.sphinx3','ctlfile . args.an4']
            # self.simpt = 96412
            self.simpt = 88

        elif bench in ['483','xalancbmk']:
            raise ValueError("Can't build.")
            # ret = ['xalancbmk','483.xalancbmk','-v test.xml xalanc.xsl']
            # self.simpt = 1820

        else:
            raise ValueError("Wrong bench name.")

        self.run_dir = head + ret[1] + tail
        self.executable = self.run_dir + ret[0] + '_base.amd64-m64-gcc41-nn'
        self.option = ret[2] if len(ret) > 2 else None
        self.input = ret[3] if len(ret) > 3 else None
