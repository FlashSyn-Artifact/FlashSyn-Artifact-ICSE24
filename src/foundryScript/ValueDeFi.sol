// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/ValueDeFiI.sol";

contract ValueDeFi is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;

    IUSDT USDT = IUSDT(0xdAC17F958D2ee523a2206206994597C13D831ec7);
    IDAI DAI = IDAI(0x6B175474E89094C44Da98b954EedeAC495271d0F);
    IERC20 CRV = IERC20(0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490);
    IERC20 USDC = IERC20(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    ICurveFi CurveFi = ICurveFi(CurveFisUSDPoolAddress);

    address private constant CurveFisUSDPoolAddress = 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address private constant ValueDefiMultiVaultAddress = 0x55BF8304C78Ba6fe47fd251F37d7beb485f86d26;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant ValueMultiVaultBankAddress = 0x8764f2c305b79680CfCc3398a96aedeA9260f7ff;
    address private constant Curve3crvAddress = 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490;

    IValueMultiVaultBank ValueMultiVaultBank = IValueMultiVaultBank(ValueMultiVaultBankAddress);
    IMultiStablesVault ValueMultiVault = IMultiStablesVault(ValueDefiMultiVaultAddress);

    uint256 temp;
    string str80;
    string str81;
    uint256[] amounts = new uint[](4);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("attacker"))))));

        vm.startPrank(address(0xC6CDE7C39eB2f0F0095F41570af89eFC2C1Ea828));
        USDT.issue(100000000 * 10 ** 6);
        USDT.transfer(address(attacker), 100000000 * 10 ** 6);
        vm.stopPrank();

        vm.startPrank(address(0x9759A6Ac90977b93B58547b4A71c78317f391A28));
        DAI.mint(address(attacker), 116000000 * 10 ** 18);
        vm.stopPrank();

        vm.startPrank(attacker);
        DAI.approve(CurveFisUSDPoolAddress, 2 ** 256 - 1);
        StandardToken(USDTAddress).approve(CurveFisUSDPoolAddress, 2 ** 256 - 1);
        DAI.approve(ValueDefiMultiVaultAddress, 2 ** 256 - 1);
        CRV.approve(CurveFisUSDPoolAddress, 2 ** 256 - 1);
        StandardToken(USDTAddress).approve(UniswapV2Router02Address, 2 ** 256 - 1);
        USDC.approve(CurveFisUSDPoolAddress, 2 ** 256 - 1);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        uint256 balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        uint256 balance3 = DAI.balanceOf(address(this)) / 10 ** 18;
        uint256 balance4 = CRV.balanceOf(address(this)) / 10 ** 18; // 1.02
        str80 = Strings.appendWithSpace(balance1, balance2);
        str81 = Strings.appendWithSpace(balance3, balance4);
        return Strings.append("FlashSyn USDT USDC DAI CRV balance: ", Strings.appendWithSpace(str80, str81));
    }

    function testExample1_() public {
        emit log("=================== Separator ==================");

        // Action: VaultBankDeposit
        ValueMultiVaultBank.deposit(ValueDefiMultiVaultAddress, DAIAddress, 11 * 1e18, 0, false, 0);

        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        emit log("=================== Separator ==================");
        // Action: Curve_DAI2USDC
        CurveFi.exchange(0, 1, 1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample3_() public {
        emit log("=================== Separator ==================");
        // Action: Curve_USDT2USDC
        CurveFi.exchange(2, 1, 1 * 10 ** 6, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample4_() public {
        // Action: VaultBankDeposit
        ValueMultiVaultBank.deposit(ValueDefiMultiVaultAddress, DAIAddress, 11 * 1e18, 0, false, 0);

        emit log("=================== Separator ==================");
        // Action: ValueWithdrawFor
        ValueMultiVault.withdrawFor(address(this), 1 * 10 ** 18, Curve3crvAddress, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample5_() public {
        // Action: Curve_DAI2USDC
        CurveFi.exchange(0, 1, 100 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        // Action: Curve_USDC2USDT
        CurveFi.exchange(1, 2, 1 * 10 ** 6, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample6_() public {
        // Action: Curve_DAI2USDC
        CurveFi.exchange(0, 1, 100 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        // Action: Curve_USDC2DAI
        CurveFi.exchange(1, 0, 1 * 10 ** 6, 0);
        emit log("=================== Separator ==================");
        revert("");
    }
}
