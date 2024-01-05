// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;



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


interface IWBNB {
    function name() external view returns (string memory);
    function approve(address guy, uint256 wad) external returns (bool);
    function totalSupply() external view returns (uint256);
    function transferFrom(
        address src,
        address dst,
        uint256 wad
    ) external returns (bool);
    function withdraw(uint256 wad) external;
    function decimals() external view returns (uint8);
    function balanceOf(address) external view returns (uint256);
    function symbol() external view returns (string memory);
    function transfer(address dst, uint256 wad) external returns (bool);
    function deposit() external payable;
    function allowance(address, address) external view returns (uint256);
    fallback() external payable;
    receive() external payable;
    event Approval(address indexed src, address indexed guy, uint256 wad);
    event Transfer(address indexed src, address indexed dst, uint256 wad);
    event Deposit(address indexed dst, uint256 wad);
    event Withdrawal(address indexed src, uint256 wad);
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





