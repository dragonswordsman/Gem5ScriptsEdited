# !/usr/bin/python3
#
# Submit gem5 jobs to server
# Author: Yicheng Wang
# Date: 08/12/2019
# Update: 11/15/2019
#
# All rights reserved.

import subprocess
import os
import sys
import time
from pathlib import Path

home = str(Path.home())
intrate = ["500","502","505","520","523",\
    "525","531","541","548","557"]
fprate = ["503","507","508","510","511",\
    "519","521","526","527","538",\
    "544","549","554"]

# Run simulation on selected benchmark
def createJobs(gem5_folder, script_name, workload):
    """
    Create jobs for simulation
    """
    gem5 = f"{home}/Research/{gem5_folder}/build/X86/gem5.opt"
    script = f"{home}/Research/Scripts/Gem5Scripts/{script_name}"
    if workload == "all":
        workloads = intrate + fprate
    elif workload == "intrate":
        workloads = intrate
    elif workload == "fprate":
        workloads = fprate
    else:
        workloads = [workload]

    jobs = {}

    if script_name == "mergeCheckpts.py":
        for workload in workloads:
            assert(workload in (intrate + fprate)), "Wrong workload name."
            binary = f"--binary={workload}"
            jobs[workload] = ["python3",script,binary]
            
    for workload in workloads:
        assert(workload in (intrate + fprate)), "Wrong workload name."
        binary = f"--binary={workload}"
        jobs[workload] = [gem5,script,binary]

    return jobs

# Run simulation on all benchmarks
def main(jobs, max_active_jobs, display=False, wait=10):
    """ 
    Run a batch of commands with a limit on active jobs. All jobs
    should be put into bench_list before running, 
    for maximum parallelism. 
    """
    assert(max_active_jobs > 0), "Active jobs number must be positive!"

    # Create an active job list
    active_jobs = []

    # Run the jobs until the threshold of max_active_jobs is reached
    job_no = 0
    total_jobs = len(jobs)
    for key in jobs.keys():
        # If max_active_jobs is reached, sleep for a while and update
        # active job list
        while len(active_jobs) >= max_active_jobs:
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

def confirm():
    """ Confirm from command line for execution """
    answer = input("Press c to continue ")
    if answer == 'c':
        return True
    return False


if __name__ == "__main__":
    if len(sys.argv) == 4:
        if sys.argv[3] in ["intrate","fprate","all"]:
            job_Num = input("Maximum active jobs: ")
            assert(job_Num.isdigit()), "Input must be digit."
            if confirm():
                jobs = createJobs(sys.argv[1],sys.argv[2],sys.argv[3])
                main(jobs,int(job_Num),display=True)
        else:
            jobs = createJobs(sys.argv[1],sys.argv[2],sys.argv[3])
            main(jobs,1,display=False)
    else:
        print(f"Expected 3 arguments got {len(sys.argv) - 1}!")
        print("Please follow the format as below:")
        print("py submitJobs.py gem5_folder_name script_name workload_name\n")
        sys.exit(1)
