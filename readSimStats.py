bench_list = ["400","401","403","410","416",
            "429","433","434","435","436",
            "437","444","445","450","453",
            "456","458","459","462",
            "464","465","470","473"]

def readSimstats(bench):
    file1 = open(f'/home/ywang/Research/stats/{bench}/{bench}simpts')
    file2 = open(f'/home/ywang/Research/stats/{bench}/{bench}_weights')
    weights = file2.readlines()
    weight = []
    for item in weights:
        tmp = item.split(' ')
        weight.append(float(tmp[0]))

    idx = weight.index(max(weight))
    simpts = file1.readlines()
    tmp = simpts[idx].split(' ')
    print(f'For bench:{bench} checkpoint {idx} at {tmp[0]}')

for item in bench_list:
    readSimstats(item)



# benchmark that be used to generate stats
benchmarks = {"mcf":6079,"milc":17568,"zeusmp":40669,"sphinx3":51646,
    "cactusADM":246595,"leslie3d":92132,"povray":39321,"GemsFDTD":99389,
    "lbm":82717,"omnetpp":34112,"astar":22856,"wrf":228382}

# probability
probability = [0.0,0.001,0.002,0.005,0.01]

bench_list = benchmarks.keys()

prefix = '/home/ywang/Research/outputs/ISCA2019Stats/'


filename = '/home/ywang/Research/outputs/ISCA2019Stats/milc/0.001/stats.txt'

sim_insts = '# Number of instructions simulated'
cpu_cycles = '# number of cpu cycles simulated'
sim_ticks = '# Number of ticks simulated'

keywords = [sim_insts,cpu_cycles,sim_ticks]

def readData(filename,keywords):
    """
    data index 0,1 is sim_seconds, sim_ticks,
    index 2,3,4 is the accepted read request of
    memory_ctrl0, memory_ctrl1 and the total
    """
    data = []
    with open(filename) as stat:
        for line in stat:
            for keyword in keywords:
                if keyword in line:
                    data.append(int(line.split()[1]))

    return data

def computeData(bench,probability):
    dataset = {}
    for P in probability:
        filename = prefix + bench + '/' + str(P) + '/stats.txt'
        dataset[P] = readData(filename,keywords)
    for key in dataset.keys():
        IPC = dataset[key][2]/dataset[key][1]
        dataset[key].append(IPC)
    return dataset


def printData(Data):
    for key in Data.keys():
        print("when P is " + str(key) + ", the IPC is " +
        str(Data[key][-1]))


data = computeData('bzip2',probability)
printData(data)


data = computeData('gobmk',probability)
printData(data)
