# !/usr/bin/python3
#
# Submit gem5 jobs to server
# Author: Yicheng Wang
# Date: 08/04/2019
#
# All rights reserved.

import os
import math

benchlist  = ["400","401","403","410","416",
           "429","433","434","435","436",
           "437","444","445","450","453",
           "454","456","458","459","462",
           "464","465","470","471","473"]

targetRefInterval = ["8000ns"]

keywords = ["host_seconds","sim_insts","sim_seconds","system.mem_ctrls1.targetRefNum"]

prefix = os.path.expanduser('~/Research/outputs/refresh')



def readTargetRef():
    """
    read data from files
    files might not exist
    """
    data = {}
    for bench in benchlist:
        for interval in targetRefInterval:
            filename = f"{prefix}/{bench}_{interval}_TRR.txt"
            if os.stat(filename).st_size != 0:
                stat = open(filename)

                if bench not in data:
                    data[bench] = {}
                    data[bench][interval] = []

                for line in stat:
                    for keyword in keywords:
                        if keyword in line:
                            num = line.split()[1]
                            if keyword == "host_seconds":
                                num = math.ceil(float(num)/60)
                                num = str(num) + " mins"
                            elif keyword == "sim_insts":
                                num =  float("{0:.2f}".format(int(num)/1e9))
                                num = str(num) + " B insts"
                            elif keyword == "sim_seconds":
                                num = float("{0:.2f}".format(float(num)*1e3))
                                num = str(num) + " ms"
                            else:
                                num = int(num)
                                num = str(num) + " equal to " + \
                                str(float("{0:.2f}".format(num*int(interval[:-2])/1e6))) + " ms"
                            data[bench][interval].append(num)

    return data

def readRefreshData():
    """
    read data from files
    files might not exist
    """
    sim_insts = "# Number of instructions simulated"
    sim_ticks = "# Number of ticks simulated"
    channle0ReadReq = "system.mem_ctrls0.readReqs"
    channle1ReadReq = "system.mem_ctrls0.readReqs"
    channle0TargetRead = "system.mem_ctrls0.targetReadReqs"
    channle1TargetRead = "system.mem_ctrls1.targetReadReqs"
    keywords = [sim_insts,sim_ticks,channle0ReadReq,\
        channle1ReadReq,channle0TargetRead,channle1TargetRead]
    keywords = {"sim_insts":sim_insts,"sim_ticks":sim_ticks,\
        "readReqs":channle0ReadReq,"targetReadReqs":channle0TargetRead}


    insertLatency = ["0ns","200ns","8000ns","16000ns","64000ns"]

    data = {}
    for bench in benchlist:
        for latency in insertLatency:
            filename = f"{prefix}/refresh/{bench}_{latency}_TRR.txt"
            try:
                stat = open(filename)
                if bench not in data:
                    data[bench] = {}
                data[bench][latency] = {}
                for line in stat:
                    for key in keywords.keys():
                        if keywords[key] in line:
                            data[bench][latency][key] = int(line.split()[1])
            except:
                continue

    for bench in data.keys():

        benchData = data[bench]
        if checkData(benchData):
            for latency in benchData.keys():
                stats = benchData[latency]
                outputString = ""
                if latency == "0ns":
                    outputString = "\n" + outputString
                outputString += "For {0:3} simulated with latency {1:5}ns, ".format(bench, int(latency[:-2]))
                outputString += "{0:9} is {1:10}, ".format("sim_insts",int(stats["sim_insts"]))
                outputString += "{0:9} is {1:15}, ".format("sim_ticks",int(stats["sim_ticks"]))
                outputString += "{0:9} is {1:8}, ".format("readReqs",int(stats["readReqs"]))
                outputString += "{0:9} is {1:8}, ".format("targetReadReqs",int(stats["targetReadReqs"]))

                insertRatio = "insertRatio is {0:5.2%}, ".format(int(stats["targetReadReqs"])/int(stats["readReqs"]))
                outputString += insertRatio

                if int(stats["targetReadReqs"]) != 0:
                    trrCost = "perTRRcost is {0:5.2}ns".format((int(benchData[latency]["sim_ticks"]) - \
                        int(benchData["0ns"]["sim_ticks"]))/(1000*int(stats["targetReadReqs"])))
                    outputString += trrCost
                print(outputString)
    return data


def checkData(benchData):
    if len(benchData.keys()) != 5:
        return False
    else:
        for latency in benchData.keys():
            stat = benchData[latency]
            if len(stat.keys()) != 4:
                return False
    return True


data = readTargetRef()
for key in data.keys():
    print(key,data[key])
