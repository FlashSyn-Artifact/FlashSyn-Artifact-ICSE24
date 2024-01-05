// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "../attack.sol";
import "../stdlib.sol";
import "../Vm.sol";
import "../CheatCodes.sol";


contract attackTester is DSTest, stdCheats {
    bZx1_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        startHoax(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 90000000000 ether);
        attackContract = new bZx1_attack{value: 4500 ether}();
        cheats.stopPrank();
        IWBTC WBTC = IWBTC(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
        cheats.prank(0xCA06411bd7a7296d7dbdd0050DFc846E95fEBEB7);
        WBTC.mint(address(attackContract), 112*10**8);
        cheats.stopPrank();
    }    function testExample0_() public {
      attackContract.attack0(1300,112);
    }

}