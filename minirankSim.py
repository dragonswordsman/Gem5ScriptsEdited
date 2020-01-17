# !/usr/bin/python3
#
# Submit gem5 jobs to server
# Author: Yicheng Wang
# Date: 12/28/2019
#
# All rights reserved.

import subprocess
import os
import sys
import time
from pathlib import Path

# SPEC CPU2006 Benchmarks
# Benchmark #447 #481 #483 don't work
integer = ["400","401","429","445","456",\
    "458","462","464","471","473","483"]
floating = ["410","416","433","434","435",\
    "436","437","444","447","450",\
    "453","454","459","465","470",\
    "481","482"]


# configure gem5 running environment
home = str(Path.home())
# Run simulation on selected benchmark
# gem5 = "/tmp/minirank-gem5.debug"
# script = f"{home}/Research/Scripts/Gem5Scripts/minirank.py"
# job = [gem5,script,binary]
# subprocess.Popen(job)
def createJobs(workload):
    gem5 = f"{home}/Research/gem5-extensions-2/build/X86/gem5.opt"
    script = f"{home}/Research/Gem5Scripts/minirank-edited.py"
    if workload == "all":
        workloads = integer + floating
    elif workload == "integer":
        workloads = "integer"
    elif workload == "floating":
        workloads = "floating"
    else:
        workloads = [workload]

    jobs = {}

    for workload in workloads:
        assert(workload in (integer + floating)), "Wrong workload name."
        binary = f"--binary={workload}"
        jobs[workload] = [gem5,script,binary]
    
    return jobs

def runjobs(jobs, display=False, wait=10):
    # Create an active job list
    active_jobs = []
    # Run the jobs until the threshold of max_active_jobs is reached
    job_no = 0
    total_jobs = len(jobs)
    for key in jobs.keys():
        # If max_active_jobs is reached, sleep for a while and update
        # active job list
        while len(active_jobs) >= 8:
            time.sleep(wait)
            active_jobs = [x for x in active_jobs if x.poll() is None]

        # Submit the next job
        job_no = job_no + 1
        if (display):
            print("JOB # %d/%d" % (job_no, total_jobs))
            print("Preform simulation " + key)
        job = subprocess.Popen(jobs[key])
        active_jobs.append(job)
    # Wait for all jobs to finish
    while len(active_jobs) > 0:
        time.sleep(wait)
        active_jobs = [job for job in active_jobs if job.poll() is None]



if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit(1)
    else:
        jobs = createJobs(sys.argv[1])
        runjobs(jobs,display=True)
        
