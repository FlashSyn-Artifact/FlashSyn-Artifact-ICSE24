// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/EminenceI.sol";

contract Eminence is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;
    address private constant EminenceAddress = 0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant eAAVEAddress = 0xc08f38f43ADB64d16Fe9f9eFCC2949d9eddEc198;

    EminenceCurrency Eminence = EminenceCurrency(EminenceAddress);
    IDAI DAI = IDAI(DAIAddress);
    EminenceCurrency eAAVE = EminenceCurrency(eAAVEAddress);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));

        vm.startPrank(address(0x9759A6Ac90977b93B58547b4A71c78317f391A28));
        DAI.mint(address(attacker), 15000000 * 10 ** 18);
        vm.stopPrank();

        vm.startPrank(attacker);
        DAI.approve(EminenceAddress, type(uint256).max);
        Eminence.approve(eAAVEAddress, type(uint256).max);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance1 = DAI.balanceOf(address(attacker)) / 1e18;
        return Strings.append("DAI balance: ", Strings.uint2str(balance1));
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
        Eminence.buy(20 * 10 ** 18, 0);

        emit log("=================== Separator ==================");
        // Action: eAAVEBuy
        eAAVE.buy(1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        // Action: EminenceBuy
        Eminence.buy(20 * 10 ** 18, 0);

        emit log("=================== Separator ==================");
        // Action: EminenceSell
        Eminence.sell(1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample3_() public {
        // Action: EminenceBuy
        Eminence.buy(3000 * 10 ** 18, 0);
        // Action: eAAVEBuy
        eAAVE.buy(2000 * 10 ** 18, 0);

        emit log("=================== Separator ==================");
        // Action: eAAVESell
        eAAVE.sell(1 * 10 ** 18, 0);
        emit log("=================== Separator ==================");
        revert("");
    }
}
