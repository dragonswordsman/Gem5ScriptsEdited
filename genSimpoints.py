# !/usr/bin/python3
# 
# Analyze the data after simpoint profiling
# Author: Yicheng Wang
# Date: 1/29/2018

import subprocess
import os
import sys
import time


# Run simulation on selected benchmark
def run(bench):
    # Change current working directory to the binary folder
    os.chdir('/home/ywang/Research/stats/'+bench)


    args = ''
    # Simpoint 
    simpoint = '/home/ywang/Research/Simpoint/bin/simpoint'
    args += simpoint

    # File path configurations
    loadFile = ' -loadFVFile simpoint.bb.gz'
    maxK = ' -maxK 30'
    save_Simpoints = ' -saveSimpoints '+bench+'simpts'
    save_SimpointWeights = ' -saveSimpointWeights '+bench+'_weights'
    inputVectorsGzipped = ' -inputVectorsGzipped true'
    args += loadFile  + maxK + save_Simpoints + save_SimpointWeights + inputVectorsGzipped

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
            "456","458","459","462",
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
        job = subprocess.Popen(run(bench),shell=True)
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
        subprocess.run(run(bench),shell=True)
    else:
        if confirm():
            main(13,display=True)