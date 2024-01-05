// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/Harvest_USDCI.sol";

contract Harvest_USDC is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;
    address private constant CurveFiAddress = 0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51;
    address private constant USDT_VaultProxyAddress = 0x053c80eA73Dc6941F518a68E2FC52Ac45BDE7c9C;

    yERC20 CURVE_yPool = yERC20(CurveFiAddress);
    IfUSDT fUSDT = IfUSDT(USDT_VaultProxyAddress);
    IUSDT USDT = IUSDT(0xdAC17F958D2ee523a2206206994597C13D831ec7);
    IUSDC USDC = IUSDC(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    uint256 temp;
    string str80;
    string str81;

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));

        vm.startPrank(address(0xC6CDE7C39eB2f0F0095F41570af89eFC2C1Ea828));
        USDT.issue(50000000 * 10 ** 6);
        USDT.transfer(address(attacker), 50000000 * 10 ** 6);
        vm.stopPrank();
        vm.startPrank(address(0x55FE002aefF02F77364de339a1292923A15844B8));
        address MasterMinter = USDC.masterMinter();
        vm.stopPrank();
        vm.startPrank(MasterMinter);
        USDC.configureMinter(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 2 ** 256 - 1);
        vm.stopPrank();
        vm.startPrank(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58));
        USDC.mint(address(attacker), 20000000e6);
        vm.stopPrank();

        vm.startPrank(attacker);
        StandardToken(USDTAddress).approve(CurveFiAddress, 2 ** 256 - 1);
        StandardToken(USDCAddress).approve(CurveFiAddress, 2 ** 256 - 1);
        StandardToken(USDTAddress).approve(USDT_VaultProxyAddress, 2 ** 256 - 1);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        uint256 balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        str80 = Strings.append("FlashSyn USDT balance: ", balance1);
        str81 = Strings.append(" || USDC balance: ", balance2);
        return Strings.append(str80, str81);
    }

    function testExample0_() public {
        revert(profitSummary());
    }

    function testExample1_() public {
        emit log("=================== Separator ==================");

        // Action: Curve_USDC2USDT
        CURVE_yPool.exchange_underlying(1, 2, 1 * 10 ** 6, 0);

        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        emit log("=================== Separator ==================");
        // Action: Curve_USDT2USDC
        CURVE_yPool.exchange_underlying(2, 1, 1 * 10 ** 6, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample3_() public {
        emit log("=================== Separator ==================");
        fUSDT.deposit(1 * 10 ** 6);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample4_() public {
        fUSDT.deposit(2 * 10 ** 6);

        emit log("=================== Separator ==================");
        fUSDT.withdraw(1 * 10 ** 6);
        emit log("=================== Separator ==================");
        revert("");
    }
}
