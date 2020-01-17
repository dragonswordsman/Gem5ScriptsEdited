# !/usr/bin/python3
#
# Submit gem5 jobs to server
# Author: Yicheng Wang
# Date: 08/22/2019
#
# All rights reserved.

import os
import os.path as path



benchlist  = ["401","403","410","416",
           "429","433","434","435","436",
           "437","444","445","450",
           "454","456","458","462","470","473"]

prefix = os.path.expanduser('~/Research/outputs/')

def checkDBC():
    argument = input("What is the argument you use?\n")

    for bench in benchlist:
        file = f"{prefix}/dbc/simout_{bench}_{argument}"
        if path.exists(file) and os.stat(file).st_size != 0:
            f = open(file)
            lines = f.readlines()
            if "exits from simulation" not in lines[-1]:
                print(f"Workload {bench} simulate with argument {argument} has error.")


checkDBC()