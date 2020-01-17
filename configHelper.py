# !/usr/bin/python2
#
# helper file for gem5 jobs
# Author: Yicheng Wang
# Date: 04/22/2019
#
# All rights reserved.

import os
import m5
from m5.objects import *


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


