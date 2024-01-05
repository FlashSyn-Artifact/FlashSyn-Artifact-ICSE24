// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/ElevenFiI.sol";

contract ElevenFi is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;

    address private PancakeRouterAddress = 0x10ED43C718714eb63d5aA57B78B54704E256024E;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private nrvFUSDTAddress = 0x2e91A0CECf28c5E518bB2E7fdcd9F8e2cd511c10;
    address private MetaSwapDepositAddress = 0xC924A8a789d7FafD089cc285e2546FC851b0942c;
    address private ElevenNeverSellVaultAddress = 0x030970f2378748Eca951ca5b2f063C45225c8f6c;

    IBUSD BUSD = IBUSD(0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56);
    IWBNB WBNB = IWBNB(payable(WBNBAddress));
    IBEP20 nrvFUSDT = IBEP20(nrvFUSDTAddress);
    IMetaSwapDeposit MetaSwapDeposit = IMetaSwapDeposit(MetaSwapDepositAddress);
    IElevenNeverSellVault ElevenNeverSellVault = IElevenNeverSellVault(ElevenNeverSellVaultAddress);

    uint256 temp;
    string str80;
    string str81;
    uint256[] amounts = new uint[](4);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));

        vm.startPrank(0xD2f93484f2D319194cBa95C5171B18C1d8cfD6C4);
        BUSD.mint(130001e18);
        BUSD.transfer(address(attacker), 130001e18);
        vm.stopPrank();

        vm.startPrank(attacker);
        WBNB.approve(PancakeRouterAddress, 2 ** 256 - 1);
        BUSD.approve(PancakeRouterAddress, 2 ** 256 - 1);
        BUSD.approve(MetaSwapDepositAddress, 2 ** 256 - 1);
        nrvFUSDT.approve(ElevenNeverSellVaultAddress, 2 ** 256 - 1);
        nrvFUSDT.approve(MetaSwapDepositAddress, 2 ** 256 - 1);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        return Strings.append("FlashSyn BUSD balance: ", BUSD.balanceOf(address(attacker)) / 1e18);
    }

    function testExample1_() public {
        emit log("=================== Separator ==================");

        // Action: AddLiquidity
        amounts[0] = 0;
        amounts[1] = 12000 * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 2 ** 256 - 1);

        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        // Action: AddLiquidity
        amounts[0] = 0;
        amounts[1] = 12000 * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 2 ** 256 - 1);

        emit log("=================== Separator ==================");
        // Action: Deposit
        ElevenNeverSellVault.deposit(12 * 10 ** 18);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample3_() public {
        // Action: AddLiquidity
        amounts[0] = 0;
        amounts[1] = 12000 * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 2 ** 256 - 1);

        // Action: Deposit
        ElevenNeverSellVault.deposit(12 * 10 ** 18);

        emit log("=================== Separator ==================");
        // Action: EmergencyBurn
        ElevenNeverSellVault.emergencyBurn();
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample4_() public {
        // Action: AddLiquidity
        amounts[0] = 0;
        amounts[1] = 12000 * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 2 ** 256 - 1);

        // Action: Deposit
        ElevenNeverSellVault.deposit(1200 * 10 ** 18);

        emit log("=================== Separator ==================");
        // Action: Withdraw
        ElevenNeverSellVault.withdraw(12 * 10 ** 18);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample5_() public {
        // Action: AddLiquidity
        amounts[0] = 0;
        amounts[1] = 12000 * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 2 ** 256 - 1);

        emit log("=================== Separator ==================");
        // Action: RemoveLiquidity
        MetaSwapDeposit.removeLiquidityOneToken(12 * 10 ** 18, 1, 0, 2 ** 256 - 1);
        emit log("=================== Separator ==================");
        revert("");
    }
}
