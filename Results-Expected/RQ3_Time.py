import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from os.path import exists
import re
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def getICtimeMap() -> dict:
    map = {} # key, benchmark+Number, value, time
    benchmarkList = ['bZx1', 'Harvest_USDC','Harvest_USDT', \
    'Warp', 'ValueDeFi', 'Yearn', 'Eminence', 'CheeseBank', 'InverseFi', \
    'ElevenFi',  'bEarnFi', 'ApeRocket', 'AutoShark',  'Novo', 'Wdoge',  'OneRing',  \
    'Puppet', 'PuppetV2' 
    ]
    #  skipped for now
    # 'Puppet', 'PuppetV2' skipped for now
    #  skipped for now

    folder_list = ["200+X", "500+X", "1000+X", "2000+X"]
    timeList = [[], [], [], []]

    # print("benchmark ", end="")
    # for folder in folder_list:
    #     print(folder[:-2], end = " ")
    # print("")

    for index in range(len(benchmarkList)):
        benchmark = benchmarkList[index]
        # if benchmark == "Harvest_USDC":
        #     print("Harvest_USDT", end = " ")
        # elif benchmark == "Harvest_USDT":
        #     print("Harvest_USDC", end = " ")
        # else:
        #     print(benchmark, end = " ")

        for jj in range(len(folder_list)):
            folder = folder_list[jj]

            filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/data/" + benchmark + "_initial_data.txt"

            file_exists = exists(filename)
            if file_exists:
                with open(filename) as file:
                    Time = 0
                    for line in file:
                        if "in total it takes " in line:
                            rr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
                            time = rr[-1]
                            Time = float(time)
                            

                    if Time > 0:
                        # print(int(Time), end = " ")
                        timeList[jj].append(int(Time))
                        map[benchmark + folder[:-2]] = int(Time)
                    # else:
                        # print("/", end = " ")

            # else:
        #         print("-", end = " ")
        # print("")

    # print("Avg. Time: ", end = "")
    # for jj in range(len(timeList)):
    #     print(round(sum(timeList[jj]) / len(timeList[jj])), end = " ")
    # print("")
    return map






def main():
    method = 1 # 0 for interpolation 
               # 1 for polynormial

    map = getICtimeMap() 

    benchmarkList = ['bZx1', 'Harvest_USDC','Harvest_USDT', \
    'Warp', 'ValueDeFi', 'Yearn', 'Eminence', 'CheeseBank', 'InverseFi', \
    'ElevenFi',  'bEarnFi', 'ApeRocket', 'AutoShark',  'Novo', 'Wdoge',  'OneRing',  \
    'Puppet', 'PuppetV2' 
    ]
    #  skipped for now
    # 'Puppet', 'PuppetV2' skipped for now
    #  skipped for now
    folder_list = [ "200_noloop", "200+X", "500_noloop", "500+X", "1000_noloop", "1000+X",  "2000_noloop" ,"2000+X"]

    time_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    time_list_synthesis = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    print("benchmark ", end="")
    for _ in range(2):  
        for folder in folder_list:
            if "_noloop" in folder:
                print(folder[:-7], end = " ")
            else:
                print(folder, end = " ")
    print("")
    for index in range(len(benchmarkList)):
        benchmark = benchmarkList[index]
        if benchmark == "Harvest_USDC":
            print("Harvest_USDT", end = " ")
        elif benchmark == "Harvest_USDT":
            print("Harvest_USDC", end = " ")
        else:
            print(benchmark, end = " ")

        if benchmark == "Yearn" or benchmark == "InverseFi":  # they cannot be solved
            print(" ---------------------------------------")
            continue 


        for method in [1, 0]:
            for jj in range(len(folder_list)):
                numberStr = folder_list[jj]
                if "_noloop" in numberStr:
                    numberStr = str(numberStr[:-7])
                else:
                    numberStr = str(numberStr[:-2])

                jj_ii = 0
                if method == 1:
                    jj_ii = jj
                else:
                    jj_ii = jj + 8
                folder = folder_list[jj]
                if folder == "precise" and method == 1:
                    continue

                filename = ""
                if folder == "precise":
                    filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_precise.txt"
                elif method == 0:
                    filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_inte.txt"
                elif method == 1:
                    filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_poly.txt"
                

                file_exists = exists(filename)
                if file_exists:
                    with open(filename) as file:
                        Time = 0
                        globalbestProfit = 0
                        for line in file:
                            if "Best Global Profit:" in line:
                                split = line.split()
                                # if split[-1] != '0':
                                #     print(line.split())
                                profit = float(split[-2])
                                if profit > globalbestProfit:
                                    globalbestProfit = profit

                            if "time" in line:
                                rr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
                                time = rr[-1]
                                Time = float(time)
                        if Time > 0 and globalbestProfit > 30:
                            if Time < 10000:
                                time_list_synthesis[jj_ii].append(int(Time))
                                time_list[jj_ii].append(int(Time) + map[benchmark + numberStr])
                                print(int(Time), end = " ")
                            else:  # if in log file the last <Time> > 10000, then it reaches time limit of 4 hours
                                time_list_synthesis[jj_ii].append(10800)
                                time_list[jj_ii].append(10800 + map[benchmark + numberStr] )
                                print("10800", end = " ")
                        else:
                            print("/", end = " ")

                else:
                    print("-", end = " ")
        print("")

    print("Avg.Synthesis Time(s): ", end = "")
    for jj in range(len(time_list_synthesis)):
        
        # print(len(time_list[jj]), end = " ")
        print(round(sum(time_list_synthesis[jj])/len(time_list_synthesis[jj])), end = " ")

    print("")

    # print(time_list[-1])
    print("==================================================== Summary =========================================")
    print("Avg.Total Time(s): ", end = "")
    for jj in range(len(time_list)):
        
        # print(len(time_list[jj]), end = " ")
        print(round(sum(time_list[jj])/len(time_list[jj])), end = " ")

    print("")

if __name__ == "__main__":
    main()

            