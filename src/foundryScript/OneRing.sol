// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/OneRingI.sol";

contract OneRing is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;

    IUSDC usdc = IUSDC(0x04068DA6C83AFCFA0e13ba15A6696662335D5B75);
    IOneRingVault vault = IOneRingVault(0x4e332D616b5bA1eDFd87c899E534D996c336a2FC);

    uint256 temp;
    string str80;
    string str81;
    uint256[] amounts = new uint[](4);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));

        address owner_of_usdc = 0xC564EE9f21Ed8A2d8E7e76c085740d5e4c5FaFbE;
        vm.startPrank(owner_of_usdc);
        usdc.Swapin(
            0x33e48143c6ea17476eeabfa202d8034190ea3f2280b643e2570c54265fe33c98, address(attacker), 150000000 * 10 ** 6
        );

        vm.stopPrank();
        vm.startPrank(attacker);
        usdc.approve(address(vault), 2 ** 256 - 1);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance1 = usdc.balanceOf(address(attacker)) / 10 ** 6;
        return Strings.append("FlashSyn USDC balance: ", balance1);
    }

    function testExample1_() public {
        emit log("=================== Separator ==================");
        // Action: Deposit
        vault.depositSafe(1 * 1e6, address(usdc), 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        // Action: Deposit
        vault.depositSafe(1000 * 1e6, address(usdc), 0);
        emit log("=================== Separator ==================");
        // Action: WithdrawOShare
        vault.withdraw(1 * 1e18, address(usdc));
        emit log("=================== Separator ==================");
        revert("");
    }
}
