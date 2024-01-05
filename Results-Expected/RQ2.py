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
    'Eminence', 'ValueDeFi', 'CheeseBank', 'Warp', 'Yearn', 'InverseFi', \
    'bEarnFi', 'AutoShark', 'ElevenFi', 'ApeRocket', 'Wdoge',  'Novo', 'OneRing',  \
    'Puppet', 'PuppetV2' 
    ]

    folder_list = ["precise"]

    print("benchmark", end="")
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
        historyProfit = getProfitinHistory(benchmark)
        # print(historyProfit, end = ", ")

        folder = "precise"

        filename = SCRIPT_DIR + "/FlashSynData/" + folder + "/" + benchmark + "_precise.txt"
        # print(filename)

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
                else:
                    print("/", end = " ")
        else:
            print("/", end = "  ")
        print("")


if __name__ == "__main__":
    main()

            