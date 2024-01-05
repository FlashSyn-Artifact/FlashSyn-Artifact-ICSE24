import time
import itertools
import os
import sys
import inspect

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import Actions.Novo as Novo
import Actions.bZx1 as bZx1
import Actions.bEarnFi as bEarnFi
import Actions.Harvest_USDC as Harvest_USDC
import Actions.Harvest_USDT as Harvest_USDT
import Actions.Eminence as Eminence
import Actions.Warp as Warp
import Actions.Puppet as Puppet
import Actions.PuppetV2 as PuppetV2
import Actions.ElevenFi as ElevenFi
import Actions.CheeseBank as CheeseBank
import Actions.ValueDeFi as ValueDeFi
import Actions.Yearn as Yearn
import Actions.OneRing as OneRing
import Actions.Novo as Novo
import Actions.AutoShark as AutoShark
import Actions.ApeRocket as ApeRocket
import Actions.Wdoge as Wdoge
import Actions.InverseFi as InverseFi


from tabulate import tabulate

if __name__ == '__main__':
    benchmark_names = []
    actual_profits = []
    inte_approx1 = []
    poly_approx1 = []
    inte_approx2 = []
    poly_approx2 = []


# ApeRocket
# Novo
# OneRing
# Yearn
# ValueDeFi
# Harvest_USDC
# Harvest_USDT

    for mo in [bZx1, Harvest_USDC, Harvest_USDT, Warp, ValueDeFi, \
                Yearn, Eminence, CheeseBank, InverseFi, \
                ElevenFi, bEarnFi, ApeRocket, Novo, \
                Wdoge, OneRing, Puppet, PuppetV2]:
        print(mo.__name__)
        benchmark_names.append(mo.__name__)
        actual_profit, e1, e2, e3, e4 = mo.main()
        actual_profits.append(actual_profit)
        inte_approx1.append(e1)
        poly_approx1.append(e2)
        inte_approx2.append(e3)
        poly_approx2.append(e4)
        print('\n')

    N = len(actual_profits)
    data = [ [] for _ in range(N) ]
    for i in range(len(actual_profits)):
        data[i] = [benchmark_names[i], actual_profits[i], inte_approx1[i], poly_approx1[i], inte_approx2[i], poly_approx2[i]]

    print (tabulate(data, headers=["Benchmark", "Actual Profit", "Inte Approx Profit1", "Poly Approx Profit1", \
                                    "Inte Approx Profit2", "Poly Approx Profit2"]))   

    print("\n\n")
    data = [[]]
    inte1dev = 0
    poly1dev = 0
    inte2dev = 0
    poly2dev = 0
    for i in range(len(actual_profits)):
        inte1dev += abs(actual_profits[i] - inte_approx1[i]) / actual_profits[i]
        poly1dev += abs(actual_profits[i] - poly_approx1[i]) / actual_profits[i]
        inte2dev += abs(actual_profits[i] - inte_approx2[i]) / actual_profits[i]
        poly2dev += abs(actual_profits[i] - poly_approx2[i]) / actual_profits[i]
    inte1dev = inte1dev / len(actual_profits)
    poly1dev = poly1dev / len(actual_profits)
    inte2dev = inte2dev / len(actual_profits)
    poly2dev = poly2dev / len(actual_profits)
    data[0] = [inte1dev, poly1dev, inte2dev, poly2dev]
    # data = [[1, 'Liquid', 24, 12],
    # [2, 'Virtus.pro', 19, 14],
    # [3, 'PSG.LGD', 15, 19],
    # [4,'Team Secret', 10, 20]]

    print (tabulate(data, headers=["Inte Approx Profit1 Deviation", "Poly Approx Profit1 Deviation", \
                                    "Inte Approx Profit2 Deviation", "Poly Approx Profit2 Deviation"]))   





# contains 1D:
# CheeseBank
# Warp
