# !/usr/bin/python3
#
# upgrade checkpoint and merge it
# after merging, the merged checkpoints
# Author: Yicheng Wang
# Date: 5/28/2019

import os
from pathlib import Path
import subprocess
import optparse
from cpu2006 import CPU2006


parser = optparse.OptionParser()

parser.add_option("--binary",action="store", type="string", default=None,
    help="base names for merge and upgrade checkpoints")

options = parser.parse_args()[0]

home = os.path.expanduser("~/Research/gem5/util/")


### Upgrade checkpoints
upgrade = ["python"]
merge_script = f"{home}cpt_upgrader.py"
upgrade.append(merge_script)
args = ['-r','-v']
upgrade.extend(args)
cpt_dir = f"{Path.home()}/Research/outputs/{options.binary}"
upgrade.append(cpt_dir)
subprocess.run(upgrade)
print("Checkpoints upgrade completed.\n")


### Merge checkpoints
merge = ["python"]
insts = int(1e7*CPU2006(options.binary).simpt)
script = f'{home}checkpoint_aggregator.py'
merge.append(script)
cpt_dir = f"{Path.home()}/Research/outputs/{options.binary}"
outdir = f"{cpt_dir}/mergeCkpts4/cpt.None.{insts}"
merge.extend(['-o',outdir])

ckpts = f"{cpt_dir}/cpt.None.{insts}"
merge.append('--cpts')
# the memory configuration is two channel
for _ in range(4):
    merge.append(ckpts)
# the memory capacity preset to 16GB in takeCkpts.py
size = int(16* pow(1024,3))
merge.extend(['--memory-size',str(size)])
subprocess.run(merge)
