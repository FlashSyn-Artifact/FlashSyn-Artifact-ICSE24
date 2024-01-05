// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/WdogeI.sol";

contract Wdoge is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;

    IWBNB wbnb = IWBNB(payable(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c));
    IERC20 busd = IERC20(0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56);
    IERC20 wdoge = IERC20(0x46bA8a59f4863Bd20a066Fd985B163235425B5F9);
    address public wdoge_wbnb = 0xB3e708a6d1221ed7C58B88622FDBeE2c03e4DB4d;
    IPancakePair wdoge_wbnb_pair = IPancakePair(wdoge_wbnb);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));

        vm.deal(attacker, 3000 ether);

        vm.startPrank(attacker);
        wbnb.deposit{value: 3000 * 10 ** 18}();
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance = wbnb.balanceOf(address(attacker)) / 1e18;
        return Strings.append("FlashSyn WBNB balance: ", Strings.uint2str(balance));
    }

    function testExample2_() public {
        revert(profitSummary());
    }

    function testExample0_() public {
        emit log("=================== Separator ==================");
        // Action: SwapWBNB2Wdoge
        WBNBIn = 1 * 1e18;
        wbnb.transfer(wdoge_wbnb, WBNBIn);
        (WdogeReserve, WbnbReserve,) = wdoge_wbnb_pair.getReserves();
        WdogeInput = 997 * WBNBIn * WdogeReserve / (1000 * WbnbReserve + 997 * WBNBIn) * 100 / 104;
        wdoge_wbnb_pair.swap(WdogeInput, 0, address(this), "");
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample1_() public {
        emit log("=================== Separator ==================");
        // Action: TransferWdoge
        wdoge.transfer(wdoge_wbnb, 1 * 1e24);
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
