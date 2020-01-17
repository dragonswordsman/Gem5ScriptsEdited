# !/usr/bin/python2
#
# This script can run gem5 simulation easily without options.
# Ruby related setting will not be implemented in this version.
# Positional arguments will not be accepted.
# Only CPU2006 benchmarks and hello will be accepted in this scripts.
# Author: Yicheng Wang
# Date: 04/22/2019
#
# All rights reserved.


import optparse
import sys
import os
from cpu2006 import CPU2006

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath

configs = os.path.expanduser("~/Research/gem5/configs")
addToPath(configs)

from common import Options
from common import Simulation
from common import CacheConfig
from common import CpuConfig
from common import MemConfig
from common.Caches import *


def get_processes(binary, np):
    """Interprets provided options and returns a list of processes"""
    multiprocesses = []

    for i in range(np):
        process = Process(pid = 100 + i)
        process.executable = binary.executable
        os.chdir(binary.run_dir)
        process.cwd = os.getcwd()

        if binary.option:
            process.cmd = [process.executable] + binary.option.split()
        else:
            process.cmd = [process.executable]

        if binary.input:
            process.input = binary.input

        multiprocesses.append(process)

    return multiprocesses

### Add options

parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

parser.add_option("--binary",action="store", type="string", default=None,
        help="base names for --take-checkpoint and --checkpoint-restore")
parser.add_option("--flags",action="store", type="string", default=None,
        help="trace names for simulation")
parser.add_option("--para",action="store", type="float", default=0,
        help="the para probability")
parser.add_option("--attack",action="store", type="string", default="0ns",
        help="the interval of malicious attack")
parser.add_option("--instructions",action="store", type="int", default=None,
        help="num of instructions after checkpoint restore")
parser.add_option("--stats",action="store", type="string", default=None,
        help="stats names for simulation")

options = parser.parse_args()[0] # only need option

### Configurations
assert(options.binary != None), "binary must be specified"

# system
sys_voltage = '1.0V'
sys_clock = '1GHz'
cpu_voltage_domain = '1.0V'
cpu_clock = "3GHz"

# cpu
num_cpus = 1
cpu_type = "DerivO3CPU"
mem_size = "16GB"
cache_line_size = 64

# external cache
caches = True
l2cache = True
l1i_size = "32kB"
l1i_assoc = 2
l1d_size = "64kB"
l1d_assoc = 2
l2_size = "8MB"
l2_assoc = 4
    

# memory
mem_type = "DDR4_2400_16x4"
mem_channels = 2
mem_ranks = 2
mem_device_size = "256MB"


# simulation
at_instruction = True


# Set the options
simpt = CPU2006(options.binary).simpt

options.sys_voltage = sys_voltage
options.sys_clock = sys_clock
options.cpu_clock = cpu_clock

options.num_cpus = num_cpus
options.cpu_type = cpu_type
options.mem_size = mem_size
options.cacheline_size = cache_line_size

options.caches = caches
options.l2cache = l2cache
options.l1i_size = l1i_size
options.l1i_assoc = l1i_assoc
options.l1d_size = l1d_size
options.l1d_assoc = l1d_assoc
options.l2_size = l2_size
options.l2_assoc = l2_assoc 

options.mem_type = mem_type
options.mem_channels = mem_channels
options.mem_ranks = mem_ranks

options.at_instruction = at_instruction

options.checkpoint_dir = os.path.expanduser("~/Research/outputs/"\
     + options.binary)
if options.num_cpus > 1:
    options.checkpoint_dir += '/mergeCkpts2'
print(options.checkpoint_dir)
options.checkpoint_restore = int(simpt*1e7)
options.maxinsts = options.instructions



folder = options.binary
stats_file = options.binary + "_"+ str(options.para) + "_" + str(options.attack) + "_PARA.txt"
config_file = options.binary + "restoreCkpts"


### Configurate the gem5 options

# Specify the output directory
outdir = os.path.expanduser("~/Research/outputs/" + folder)
m5.options.outdir = outdir
m5.core.setOutputDir(outdir)
# Specify the filename of stats
m5.stats.addStatVisitor(stats_file)
# Specify the debug flag and enable them
m5.debug.flags[options.flags].enable()
# Specify the filename of trace output. if not, it will print to screen
# m5.trace.output(options.binary + "_" + options.flags + ".gz")
# Specify the filename of pydot config
m5.options.dot_config = config_file

### Configurate the system parameters

# create the system we are going to simulate
system = System()

# create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = options.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock = options.sys_clock,
    voltage_domain = system.voltage_domain)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain(voltage = cpu_voltage_domain)

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = options.cpu_clock,
    voltage_domain = system.cpu_voltage_domain)



### Configurate cpu, cache, memory

(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)


system.cpu = [CPUClass(cpu_id=i) for i in range(num_cpus)]
system.mem_mode = test_mem_mode
system.mem_ranges = [AddrRange(options.mem_size)]
system.cache_line_size = options.cacheline_size

# All cpus belong to a common cpu_clk_domain, therefore running at a common
# frequency.
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain


### Assign processes to cpus

multiprocesses = []
multiprocesses = get_processes(CPU2006(options.binary),num_cpus)

# set the cpu to use the process as its workload and create thread contexts
for i in range(num_cpus):
    system.cpu[i].workload = multiprocesses[i]
    system.cpu[i].createThreads()


### Configurate cache and memory

MemClass = Simulation.setMemClass(options)
system.membus = SystemXBar()
system.system_port = system.membus.slave
CacheConfig.config_cache(options, system)
MemConfig.config_mem(options, system)

for i in range(mem_channels):
    system.mem_ctrls[i].device_size = mem_device_size
    system.mem_ctrls[i].para = options.para
    system.mem_ctrls[i].insert_read_latency = options.attack



# Create the "root". (All scripts must have a root)
root = Root(full_system = False, system = system)
# Instantiate the system and simulation
Simulation.run(options, root, system, FutureClass)