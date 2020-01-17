# !/usr/bin/python3
#
# Submit gem5 jobs to server
# Author: Yicheng Wang
# Date: 06/06/2019
#
# All rights reserved.

import os

benchlist  = ["400","401","403","410","416",
           "429","433","434","435","436",
           "437","444","445","450","453",
           "454","456","458","459","462",
           "464","465","470","471","473","482"]

# probability
probability = [0.0,0.001,0.005,0.01,0.05]


prefix = os.path.expanduser('~/Research/outputs/')



def readParaData():
    """
    read data from files
    files might not exist
    """
    data = {}
    for bench in benchlist:
        for p in probability:
            filename = f"{prefix}{bench}/{bench}_{str(p)}_0ns_PARA.txt"
            try:
                stat = open(filename)
                if bench not in data:
                    data[bench] = {}
                    data[bench][p] = []
                else:    
                    data[bench][p] = []
                for line in stat:
                    for keyword in keywords:
                        if keyword in line:
                            data[bench][p].append(int(line.split()[1]))
            except:
                continue
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


data = readRefreshData()
