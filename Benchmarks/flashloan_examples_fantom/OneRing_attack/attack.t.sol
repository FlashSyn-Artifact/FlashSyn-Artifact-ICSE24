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
    OneRing_attack attackContract;
    Vm public constant vm = Vm(HEVM_ADDRESS);
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    constructor() {
        attackContract = new OneRing_attack();
        IUSDC usdc = IUSDC(0x04068DA6C83AFCFA0e13ba15A6696662335D5B75);
        address owner_of_usdc = 0xC564EE9f21Ed8A2d8E7e76c085740d5e4c5FaFbE;
        cheats.stopPrank();
        cheats.prank(owner_of_usdc);
        usdc.Swapin(0x33e48143c6ea17476eeabfa202d8034190ea3f2280b643e2570c54265fe33c98, address(attackContract), 150000000*10**6);
    }

    function testExample() public {
        cheats.expectRevert("");
        attackContract.attack();
    }

}