// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "../attack.sol";
import "../stdlib.sol";
import "../Vm.sol";

interface CheatCodes {
    function prank(address) external;
    function stopPrank() external;
    function expectRevert(bytes calldata) external;
}

contract attackTester is DSTest, stdCheats {
    ApeRocket_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        startHoax(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 90000000000 ether);
        attackContract = new ApeRocket_attack();
        cheats.stopPrank();
        cheats.prank(0x73feaa1eE314F8c655E354234017bE2193C9E24E);
        ICAKE CAKE = ICAKE(0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82);
        CAKE.mint(address(attackContract),  1615000e18);
    }
    function testExample0_() public {
      cheats.expectRevert("");
      attackContract.attack();
    }
    
}