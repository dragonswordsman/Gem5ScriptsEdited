import os
class CPU2017(object):
    """
    CPU2017() -> class
    Set CPU2017 benchmarks configurations for gem5 simulation
    """
    def __init__(self,bench):
        """
        Initialize the benchmark instance with its name
        """
        if bench in ['500', 'perlbench_r']:
            ret = ['perlbench_r','500.perlbench_r','-I./lib splitmail.pl 6400 12 26 16 100 0']

        elif bench in ['502', 'gcc_r']:
            ret = ['gcc_r','502.gcc_r','ref32.c -O3 -fselective-scheduling -fselective-scheduling2']
        
        elif bench in ['503', 'bwaves_r']:
            ret = ['bwaves_r','503.bwaves_r','bwaves_4','bwaves_4.in']
        
        elif bench in ['505', 'mcf_r']:
            ret = ['mcf_r','505.mcf_r','inp.in']

        elif bench in ['507', 'cactuBSSN_r']:
            ret = ['cactuBSSN_r','507.cactuBSSN_r','spec_ref.par']

        elif bench in ['508', 'namd_r']:
            ret = ['namd_r','508.namd_r','--input apoa1.input --iterations 65']

        elif bench in ['510', 'parest_r']:
            ret = ['parest_r','510.parest_r','ref.prm']

        elif bench in ['511', 'povray_r']:
            ret = ['povray_r','511.povray_r','SPEC-benchmark-ref.ini']

        elif bench in ['519', 'lbm_r']:
            ret = ['lbm_r','519.lbm_r','3000 lbm.in 0 0 100_100_130_ldc.of']

        elif bench in ['520', 'omnetpp_r']:
            ret = ['omnetpp_r','520.omnetpp_r','-c General -r 0']

        elif bench in ['521', 'wrf_r']:
            ret = ['wrf_r','521.wrf_r','']
        
        elif bench in ['523', 'xalancbmk_r']:
            ret = ['xalancbmk_r','523.xalancbmk_r','-v t5.xml xalanc.xsl']
        
        elif bench in ['525', 'x264_r']:
            ret = ['x264_r','525.x264_r','--seek 500 --dumpyuv 200 --frames 1250 -o BuckBunny_New.264 BuckBunny.yuv 1280x720']

        elif bench in ['526', 'blender_r']:
            ret = ['blender_r','526.blender_r','sh3_no_char.blend --render-output sh3_no_char_ --threads 1 -b -F RAWTGA -s 849 -e 849 -a']

        elif bench in ['527', 'cam4_r']:
            ret = ['cam4_r','527.cam4_r','',"atm_in"]

        elif bench in ['531', 'deepsjeng_r']:
            ret = ['deepsjeng_r','531.deepsjeng_r','ref.txt']

        elif bench in ['538', 'imagick_r']:
            ret = ['imagick_r','538.imagick_r','-limit disk 0 refrate_input.tga -edge 41 -resample 181% -emboss 31 -colorspace YUV -mean-shift 19x19+15% -resize 30% refrate_output.tga']

        elif bench in ['541', 'leela_r']:
            ret = ['leela_r','541.leela_r','ref.sgf']

        elif bench in ['544', 'nab_r']:
            ret = ['nab_r','544.nab_r','1am0 1122214447 122']

        elif bench in ['548', 'exchange2_r']:
            ret = ['exchange2_r','548.exchange2_r','6']

        elif bench in ['549', 'fotonik3d_r']:
            ret = ['fotonik3d_r','549.fotonik3d_r','']

        elif bench in ['554', 'roms_r']:
            ret = ['roms_r','554.roms_r','','ocean_benchmark2.in.x']

        elif bench in ['557', 'xz_r']:
            ret = ['xz_r','557.xz_r','input.combined.xz 250 a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf 40401484 41217675 7']

        else:
            raise ValueError("Wrong bench name.")
        
        head = os.path.expanduser("~/Research/CPU2017/")
        if int(bench) < 600:
            tail = '/run/run_base_refrate_O2Static-m64.0000/'
        else:
            tail = '/run/run_base_refspeed_O2Static-m64.0000/'

        self.run_dir = head + ret[1] + tail
        self.executable = self.run_dir + ret[0] + '_base.O2Static-m64'
        self.option = ret[2] if len(ret[2]) > 0 else None
        self.input = ret[3] if len(ret) > 3 else None