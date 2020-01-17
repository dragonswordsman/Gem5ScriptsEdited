# !/usr/bin/python2
#
# This script can run gem5 simulation easily without options.
# Ruby related setting will not be implemented in this version.
# Positional arguments will not be accepted.
# Only CPU2006 benchmarks and hello will be accepted in this scripts.
# Author: Yicheng Wang
# Date: 04/18/2019
#
# All rights reserved.

from __future__ import print_function
from __future__ import absolute_import

import os
import m5
import math
from m5.objects import *
from configHelper import get_processes
from cpu2006 import CPU2006
from m5.util import addToPath

configs = os.path.expanduser("~/Research/gem5/configs")
addToPath(configs)


from common.MemConfig import create_mem_ctrl
from common.Caches import *



folder = "test"
stats_file = "test"
config_file = "test.ini"
flag = "DRAM"

### Configurate the gem5 options
# Specify the output directory
outdir = os.path.expanduser("~/Research/outputs/" + folder)
m5.options.outdir = outdir
m5.core.setOutputDir(outdir)
# Specify the filename of stats
m5.stats.addStatVisitor(stats_file)
# Specify the debug flag and enable them
m5.debug.flags[flag].enable()
# Specify the filename of trace output. if not, it will print to screen
m5.trace.output(flag + ".gz")
# Specify the filename of pydot config
m5.options.dot_config = config_file


### Configurate the system parameters

# create the system we are going to simulate
system = System()

# create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = "1.0V")

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock = "1GHz",
    voltage_domain = system.voltage_domain)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain(voltage = "1.0V")

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = "3GHz",
    voltage_domain = system.cpu_voltage_domain)


### Configurate the cpu and caches options

# Create a memory bus first to be able to connect with cpu
system.membus = SystemXBar()
system.system_port = system.membus.slave

# create l2Xbar fisrt to able to connect with L1Cache
system.tol2bus = L2XBar()
system.tol2bus.clk_domain = system.cpu_clk_domain

# create L2Cache
system.l2 = L2Cache()
system.l2.clk_domain = system.cpu_clk_domain
system.l2.size = "2MB"
system.l2.assoc = 8

# Conect L2XBar, L2Cache, membus
system.tol2bus.master = system.l2.cpu_side
system.l2.mem_side = system.membus.slave

nums_cpus = 1
cpu_type = "AtomicSimpleCPU"
system.mem_mode = "atomic"
system.mem_ranges = [AddrRange('16GB')]  # Create an address range
system.cache_line_size = 64 # default is 64
if cpu_type == "DerivO3CPU":
    system.cpu = [DerivO3CPU() for _ in range(nums_cpus)]
elif cpu_type == "AtomicSimpleCPU":
    cpu = AtomicSimpleCPU()
    system.cpu = [cpu(cpu_id=i) for i in range(nums_cpus)]
else:
    raise ValueError("Wrong cpu type.")

for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain

    # Create InterruptController
    cpu.createInterruptController()
    cpu.interrupts[0].pio = system.membus.master
    cpu.interrupts[0].int_slave = system.membus.master
    cpu.interrupts[0].int_master = system.membus.slave

    # create itb & dtb
    cpu.itb = X86TLB()
    cpu.dtb = X86TLB()

    # create itb_walker_cache & dtb_walker_cache
    cpu.itb_walker_cache = PageTableWalkerCache()
    cpu.dtb_walker_cache = PageTableWalkerCache()

    # connect itb & dtb with itb_walker cache & dtb_walker_cache
    cpu.dtb.walker.port = cpu.dtb_walker_cache.cpu_side
    cpu.itb.walker.port = cpu.itb_walker_cache.cpu_side



    # create icache
    cpu.icache = L1_ICache()
    cpu.icache.size = "32kB"
    cpu.icache.assoc = 2

    # create dcache
    cpu.dcache = L1_DCache()
    cpu.dcache.size = "64kB"
    cpu.dcache.assoc = 2

    # connect icache_port with icache, dcache_port with dcache
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side

    # connect icache & dcache with L2XBar
    cpu.icache.mem_side = system.tol2bus.slave
    cpu.dcache.mem_side = system.tol2bus.slave

    # connect itb_walker cache & dtb_walker_cache with L2XBar
    cpu.itb_walker_cache.mem_side = system.tol2bus.slave
    cpu.dtb_walker_cache.mem_side = system.tol2bus.slave


### Configureate memory options

nbr_mem_ctrls = 2
intlv_size = max(128, system.cache_line_size.value)
intlv_bits = int(math.log(nbr_mem_ctrls, 2))

mem_ctrls = []

for i in range(nbr_mem_ctrls):
    mem_ctrl = create_mem_ctrl(DDR4_2400_16x4, system.mem_ranges[0],
     i, nbr_mem_ctrls, intlv_bits, intlv_size)
    mem_ctrl.device_size = "256MB"
    mem_ctrls.append(mem_ctrl)

system.mem_ctrls = mem_ctrls

# connect memory with membus
for i in range(nbr_mem_ctrls):
    system.membus.master = system.mem_ctrls[i].port



### Assign processes to cpus

multiprocesses = []
multiprocesses = get_processes(CPU2006("433"),nums_cpus)

# set the cpu to use the process as its workload and create thread contexts
for i in range(nums_cpus):
    system.cpu[i].workload = multiprocesses[i]
    system.cpu[i].createThreads()



### Start the simulation

# set up the root SimObject
root = Root(full_system = False, system = system)
# Simulation.run(options, root, system, FutureClass)


# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
