# !/usr/bin/python3
# 
# Simpoint Profiling
# Author: Yicheng Wang
# Date: 11/17/201

import subprocess
import os
import sys
from cpu2017 import CPU2017


# Run simulation on selected benchmark
def run(bench):
    # Change current working directory to the binary folder
    binary = chooseBench(bench)
    os.chdir('/home/ywang/Research/CPU2006/' + binary[1] + 
        '/run/run_base_ref_amd64-m64-gcc41-nn.0000')


    args = []
    # Gem5 configurations
    gem5 = '/home/ywang/Research/gem5/build/X86/gem5.opt'
    gem5_output = '--outdir=/home/ywang/Research/outputs/' + bench
    script = '/home/ywang/Research/gem5/configs/example/se.py'
    args.extend([gem5,gem5_output,script])

    # Binary Selection
    program = '--cmd=' + binary[0] + '_base.amd64-m64-gcc41-nn'
    args.extend([program])
    if len(binary) > 2:
        option = '--option=' + binary[2]
        args.extend([option])
    if len(binary) > 3:
        Input = '--input=' + binary[3]
        args.extend([Input])

    # CPU configuration
    cpu_type = '--cpu-type=AtomicSimpleCPU'
    args.extend([cpu_type])

    # Memory configurations
    mem_size = '--mem-size=8GB'
    mem_type = '--mem-type=SimpleMemory'
    args.extend([mem_size,mem_type])

    # Task configurations
    simpoint_profile = '--simpoint-profile'
    simpoint_interval = '--simpoint-interval=10000000'
    args.extend([simpoint_profile,simpoint_interval])

    return args

# Run simulation on all benchmarks
def main(max_active_jobs, display=False, wait=10):
    """ Run a batch of commands with a limit on active jobs. All jobs
        should be put into bench_list before
        running, for maximum parallelism. """
    assert(max_active_jobs > 0)
    
    bench_list = ["400","401","403","410","416",
            "429","433","434","435","436",
            "437","444","445","450","453",
            "454","456","458","459","462",
            "464","465","470","473","482"]
    
    # Create an active job list
    active_jobs = []

    # Run the jobs until the threshold of max_active_jobs is reached
    job_no = 0
    jobs = len(bench_list)
    for bench in bench_list:
        # If max_active_jobs is reached, sleep for a while and update
        # active job list
        while len(active_jobs) >= max_active_jobs:
            time.sleep(wait)
            active_jobs = [x for x in active_jobs if x.poll() is None]

        # Submit the next job
        job_no = job_no + 1
        if (display):
            print("JOB # %d/%d" % (job_no, jobs))
            print("Preform simulation " + bench)
        job = subprocess.Popen(run(bench))
        active_jobs.append(job)

    # Wait for all jobs to finish
    while len(active_jobs) > 0:
        time.sleep(wait)
        active_jobs = [job for job in active_jobs if job.poll() is None]

def confirm():
    """ Confirm from command line for execution """
    answer = input("Press 0 to stop ")
    if answer != 0:
        return True
    return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        bench = sys.argv[1]
    else:
        bench = 'hello'
    if bench != 'all':
        subprocess.run(run(bench))
    else:
        if confirm():
            main(13,display=True)