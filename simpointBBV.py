# This script can run gem5 simulation easily without options.
# Positional arguments will not be accepted.
# The purpose of this script is generate bbv file for simpoint
#
# Author: Yicheng Wang
# Date: 12/12/2019
#
# All rights reserved.

from __future__ import print_function
from __future__ import absolute_import

import optparse
import sys
import os
from cpu2017 import CPU2017

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

options = parser.parse_args()[0] # only need option

### Configurations

# binary
assert(options.binary != None), "Please specify the binary."

# Set the options
options.cpu_type = "NonCachingSimpleCPU"
options.mem_size = "8GB"
options.simpoint_profile = True
options.simpoint_interval = 1e7


folder = options.binary
stats_file = options.binary + "_simpoint.txt"
config_file = "createSimPoints"

### Configurate the gem5 options

# Specify the output directory
outdir = os.path.expanduser("~/Research/outputs2017/" + folder)
m5.options.outdir = outdir
m5.core.setOutputDir(outdir)
# Specify the filename of stats
m5.stats.addStatVisitor(stats_file)
# Specify the filename of pydot config
m5.options.dot_config = config_file
# redirect stdout
stdout_file = "simout_" + options.binary
stdout_file = os.path.join(outdir, stdout_file)
redir_fd = os.open(stdout_file, os. O_WRONLY | os.O_CREAT | os.O_TRUNC)
os.dup2(redir_fd, sys.stdout.fileno())
# redirect stderr
stderr_file = "simerr_" + options.binary
stderr_file = os.path.join(outdir, stderr_file)
redir_fd = os.open(stderr_file, os. O_WRONLY | os.O_CREAT | os.O_TRUNC)
os.dup2(redir_fd, sys.stderr.fileno())


### Display simulation configurations
print("\n" + "=" * 30)
print("""Simulation workload is %s.\n\
The simulation simpoint interval %d instructions.\n\
The output folder is %s.\n"""\
% (options.binary, options.simpoint_interval, m5.options.outdir))
print("=" * 30 + "\n")

### Configurate the system parameters

# create the system we are going to simulate
system = System()

# create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = options.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock = options.sys_clock,
    voltage_domain = system.voltage_domain)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = options.cpu_clock,
    voltage_domain = system.cpu_voltage_domain)



### Configurate cpu, cache, memory

(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)


system.cpu = [CPUClass(cpu_id=i) for i in range(options.num_cpus)]
system.mem_mode = test_mem_mode
system.mem_ranges = [AddrRange(options.mem_size)]
system.cache_line_size = options.cacheline_size

# All cpus belong to a common cpu_clk_domain, therefore running at a common
# frequency.
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain
    


### Assign processes to cpus

multiprocesses = []
multiprocesses = get_processes(CPU2017(options.binary),options.num_cpus)

# set the cpu to use the process as its workload and create thread contexts
for i in range(options.num_cpus):
    system.cpu[i].workload = multiprocesses[i]
    system.cpu[i].createThreads()
    if options.simpoint_profile:
        system.cpu[i].addSimPointProbe(options.simpoint_interval)


### Configurate cache and memory

MemClass = Simulation.setMemClass(options)
system.membus = SystemXBar()
system.system_port = system.membus.slave
CacheConfig.config_cache(options, system)
MemConfig.config_mem(options, system)


# Create the "root". (All scripts must have a root)
root = Root(full_system = False, system = system)
# Instantiate the system and simulation
Simulation.run(options, root, system, FutureClass)
print("Workload " + options.binary + " exits from simulation after simulating " + str(options.take_checkpoints))

