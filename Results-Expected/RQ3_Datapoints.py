import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from os.path import exists
import re
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():

    method = 0 # 0 for interpolation 
               # 1 for polynormial

    benchmarkList = ['bZx1', 'Harvest_USDC','Harvest_USDT', \
    'Warp', 'ValueDeFi', 'Yearn', 'Eminence', 'CheeseBank', 'InverseFi', \
    'ElevenFi',  'bEarnFi', 'ApeRocket', 'AutoShark',  'Novo', 'Wdoge',  'OneRing',  \
    'Puppet', 'PuppetV2' 
    ]
    #  skipped for now
    # 'Puppet', 'PuppetV2' skipped for now
    #  skipped for now

    folder_list = [ "200_noloop", "200+X", \
                    "500_noloop", "500+X", \
                    "1000_noloop", "1000+X", \
                "2000_noloop" ,"2000+X"]
    # folder_list = [  "500+X" ]
    datapoints_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

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
            
        if benchmark == "Yearn" or benchmark == "InverseFi":
            print("----------------------------------------------")
            continue
        
        for method in [1, 0]:
            for jj in range(len(folder_list)):
                jj_ii = 0
                if method == 1:
                    jj_ii = jj
                else:
                    jj_ii = jj + 8

                folder = folder_list[jj]
                filename = ""
                if method == 0:
                    filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_inte.txt"
                elif method == 1:
                    filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_poly.txt"

                file_exists = exists(filename)
                if file_exists:
                    with open(filename) as file:
                        Round = 0
                        startDataPoints = False
                        NumPointsList = []
                        NumPoints = 0
                        for line in file:
                            if "number of new data points added ===========" in line:
                                rr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
                                datapoints = int(rr[-1])
                                if datapoints > 0:
                                    Round += 1

                            if "number of points:" in line:
                                startDataPoints = True
                            elif startDataPoints and "skip" not in line \
                                and "Check" not in line and "======" not in line \
                                and "For" not in line and "Best" not in line :
                                split = line.split()
                                # print(line)
                                NumPoints += int(split[0])
                            
                            if startDataPoints and ("Check Contract:" in line or "======" in line):
                                startDataPoints = False
                                NumPointsList.append(NumPoints)
                                NumPoints = 0

                        if len(NumPointsList) >= 2:
                            datapoints_list[jj_ii].append(NumPointsList[-1])
                            print(NumPointsList[-1], end = " ")
                            # print(str(NumPointsList[-1]) + "(" + str(Round) + ")", end = " ")
                            # print("(", len(NumPointsList), ")")
                        else:
                            print("notTwo", end = " ")

                else:
                    print("-", end = " ")
        print("")


    print("==================================================== Summary =========================================")
    print("Avg. Data Points:", end = " ")
    for jj in range(len(datapoints_list)):
        print(round(sum(datapoints_list[jj])/len(datapoints_list[jj])), end = " ")
    print("")


if __name__ == "__main__":
    main()