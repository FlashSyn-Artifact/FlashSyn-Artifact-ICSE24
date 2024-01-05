// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/bEarnFiI.sol";

contract bEarnFi is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;

    address private constant EminenceAddress = 0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8;
    EminenceCurrency Eminence = EminenceCurrency(EminenceAddress);
    address private constant eAAVEAddress = 0xc08f38f43ADB64d16Fe9f9eFCC2949d9eddEc198;
    EminenceCurrency eAAVE = EminenceCurrency(eAAVEAddress);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));
        vm.startPrank(0xD2f93484f2D319194cBa95C5171B18C1d8cfD6C4);
        BUSD.mint(7804239e18);
        BUSD.transfer(address(attacker), 7804239e18);
        vm.stopPrank();
        vm.startPrank(attacker);
        BUSD.approve(ProxyAddress, type(uint256).max);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance = BUSD.balanceOf(address(attacker)) / 1e18;
        return Strings.append("BUSD balance: ", Strings.uint2str(balance));
    }

    function testExample2_() public {
        revert(profitSummary());
    }

    function testExample0_() public {
        emit log("=================== Separator ==================");
        // Action: EminenceBuy
        Eminence.buy(1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample1_() public {
        // Action: EminenceBuy
        Eminence.buy(2 * 10 ** 18, 0);

        emit log("=================== Separator ==================");
        // Action: eAAVEBuy
        eAAVE.buy(1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        // Action: EminenceBuy
        Eminence.buy(2 * 10 ** 18, 0);

        emit log("=================== Separator ==================");
        // Action: EminenceSell
        Eminence.sell(1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample3_() public {
        // Action: EminenceBuy
        Eminence.buy(3 * 10 ** 18, 0);
        // Action: eAAVEBuy
        eAAVE.buy(2 * 10 ** 18, 0);

        emit log("=================== Separator ==================");
        // Action: eAAVESell
        eAAVE.sell(1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }
}
