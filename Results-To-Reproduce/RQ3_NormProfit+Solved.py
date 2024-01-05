import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from os.path import exists
import re
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))



def getProfitinHistory(benchmark: str):
    profit = 0
    if benchmark == "bZx1":
        profit = 1194.4527388702236
    elif benchmark == "bEarnFi":
        profit = 18077.148053847253
    elif benchmark == "Harvest_USDC":
        profit = 338448
    elif benchmark == "Harvest_USDT":
        profit = 307416.5824059993
    elif benchmark == "Eminence":
        profit = 1674278
    elif benchmark == "Warp":
        profit = 1693523.4500000002
    elif benchmark == "Puppet":
        profit = 89000.0
    elif benchmark == "PuppetV2":
        profit = 953100.0
    elif benchmark == "ElevenFi":
        profit = 129741.57
    elif benchmark == "CheeseBank":
        profit = 3270347.8
    elif benchmark == "ValueDeFi":
        profit = 8618002.36
    elif benchmark == "Yearn":
        profit = 56924.128741149354
    elif benchmark == "OneRing":
        profit = 1534752
    elif benchmark == "Novo":
        profit = 24857
    elif benchmark == "AutoShark":
        profit = 1381.57
    elif benchmark == "ApeRocket":
        profit = 1345.8301500000016
    elif benchmark == "Wdoge":
        profit = 78
    elif benchmark == "InverseFi":
        profit = 2515606

    return int(profit)


def main():
    method = 0 # 0 for interpolation 
               # 1 for polynomial

    benchmarkList = ['bZx1', 'Harvest_USDC','Harvest_USDT', \
    'Warp', 'ValueDeFi', 'Yearn', 'Eminence', 'CheeseBank', 'InverseFi', \
    'ElevenFi',  'bEarnFi', 'ApeRocket', 'AutoShark',  'Novo', 'Wdoge',  'OneRing',  \
    'Puppet', 'PuppetV2' 
    ]


    folder_list = ["200_noloop", "200+X", "500_noloop", "500+X", "1000_noloop", "1000+X",  "2000_noloop" ,"2000+X"]

    # "200_noloop", "200+X", 

    a = [[], [], [], [], \
         [], [], [], [], \
        [], [], [], [], \
        [], [], [], []]

    print("benchmark", "historyProfit ", end="")
    for _ in range(2):  
        for folder in folder_list:
            if "_noloop" in folder:
                print(folder[:-7], end = " ")
            else:
                print(folder, end = " ")
    print("")

    current_row = -1
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
        
        historyProfit = getProfitinHistory(benchmark)
        print(historyProfit, end = " ")
        current_row += 1
        a[current_row].append(historyProfit)

        for method in [1, 0]:
            for folder in folder_list:
                if folder == "precise" and method == 1:
                    continue

                filename = ""
                if method == 0:
                    filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_inte.txt"
                elif method == 1:
                    filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_poly.txt"
                

                file_exists = exists(filename)
                if file_exists:
                    with open(filename) as file:
                        globalbestProfit = 0
                        profitPerRound = [0.0]
                        round = [0.0]
                        for line in file:
                            if "Best Global Profit:" in line:
                                split = line.split()
                                # if split[-1] != '0':
                                #     print(line.split())
                                profit = float(split[-2])
                                if profit > globalbestProfit:
                                    globalbestProfit = profit
                                    # print("New global Profit: ", globalbestProfit)
                                round.append(len(round))

                                profitPerRound.append(globalbestProfit)
                        if globalbestProfit > 30:
                            print(int(globalbestProfit), end = " ")
                            a[current_row].append(int(globalbestProfit))
                        else:
                            a[current_row].append(0)
                            print("/", end = " ")
                else:
                    print("-", end = " ")
        print("")


    print("==================================================== Summary =========================================")
    print("==== Avg. Norm Profit =====")

    # for row in a:
    #     print(row)

    # Calculate Normalized Profit
    for i in range(len(a[0])):
        if i == 0:
            continue
        total = 0
        for j in range(len(a)):
            normalized_profit = a[j][i] / a[j][0]
            # print("normalized_profit: ", a[j][i], "/", a[j][0], "=", normalized_profit)
            total += normalized_profit
        print("%.3f" % float(total / 16), end=" ")
    print("")

    print("==== # Benchmarks Solved =====")
    # Calculate Number of Benchmark solved
    for i in range(len(a[0])):
        if i == 0:
            continue
        total = 0
        for j in range(len(a)):
            if a[j][i] > 0:
                total += 1
        print(total, end=" ")
    print("")


if __name__ == "__main__":
    main()


            