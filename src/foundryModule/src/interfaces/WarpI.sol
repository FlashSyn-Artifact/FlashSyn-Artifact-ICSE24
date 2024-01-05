// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;


interface IUniswapV2Pair {
    event Approval(address indexed owner, address indexed spender, uint value);
    event Transfer(address indexed from, address indexed to, uint value);
    function name() external pure returns (string memory);
    function symbol() external pure returns (string memory);
    function decimals() external pure returns (uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address owner) external view returns (uint);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function transferFrom(address from, address to, uint value) external returns (bool);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
    function PERMIT_TYPEHASH() external pure returns (bytes32);
    function nonces(address owner) external view returns (uint);
    function permit(address owner, address spender, uint value, uint deadline, uint8 v, bytes32 r, bytes32 s) external;

    event Mint(address indexed sender, uint amount0, uint amount1);
    event Burn(address indexed sender, uint amount0, uint amount1, address indexed to);
    event Swap(
        address indexed sender,
        uint amount0In,
        uint amount1In,
        uint amount0Out,
        uint amount1Out,
        address indexed to
    );
    event Sync(uint112 reserve0, uint112 reserve1);

    function MINIMUM_LIQUIDITY() external pure returns (uint);
    function factory() external view returns (address);
    function token0() external view returns (address);
    function token1() external view returns (address);
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
    function price0CumulativeLast() external view returns (uint);
    function price1CumulativeLast() external view returns (uint);
    function kLast() external view returns (uint);

    function mint(address to) external returns (uint liquidity);
    function burn(address to) external returns (uint amount0, uint amount1);
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
    function skim(address to) external;
    function sync() external;
    function initialize(address, address) external;
}

                    
interface IUniswapV2Router02 {
    function WETH (  ) external view returns ( address );
    function addLiquidity ( address tokenA, address tokenB, uint256 amountADesired, uint256 amountBDesired, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB, uint256 liquidity );
    function addLiquidityETH ( address token, uint256 amountTokenDesired, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external payable returns ( uint256 amountToken, uint256 amountETH, uint256 liquidity );
    function factory (  ) external view returns ( address );
    function getAmountIn ( uint256 amountOut, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountIn );
    function getAmountOut ( uint256 amountIn, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountOut );
    function getAmountsIn ( uint256 amountOut, address[] memory path ) external view returns ( uint256[] memory amounts );
    function getAmountsOut ( uint256 amountIn, address[] memory path ) external view returns ( uint256[] memory amounts );
    function quote ( uint256 amountA, uint256 reserveA, uint256 reserveB ) external pure returns ( uint256 amountB );
    function removeLiquidity ( address tokenA, address tokenB, uint256 liquidity, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB );
    function removeLiquidityETH ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountToken, uint256 amountETH );
    function removeLiquidityETHSupportingFeeOnTransferTokens ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountETH );
    function removeLiquidityETHWithPermit ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s ) external returns ( uint256 amountToken, uint256 amountETH );
    function removeLiquidityETHWithPermitSupportingFeeOnTransferTokens ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s ) external returns ( uint256 amountETH );
    function removeLiquidityWithPermit ( address tokenA, address tokenB, uint256 liquidity, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline, bool approveMax, uint8 v, bytes32 r, bytes32 s ) external returns ( uint256 amountA, uint256 amountB );
    function swapETHForExactTokens ( uint256 amountOut, address[] memory path, address to, uint256 deadline ) external payable returns ( uint256[] memory amounts );
    function swapExactETHForTokens ( uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external payable returns ( uint256[] memory amounts );
    function swapExactETHForTokensSupportingFeeOnTransferTokens ( uint256 amountOutMin, address[] memory path, address to, uint256 deadline) external;
    function swapExactTokensForETH ( uint256 amountIn, uint256 amountOutMin, address[] memory path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
    function swapExactTokensForETHSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] memory path, address to, uint256 deadline ) external;
    function swapExactTokensForTokens ( uint256 amountIn, uint256 amountOutMin, address[] memory path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
    function swapExactTokensForTokensSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] memory path, address to, uint256 deadline ) external;
    function swapTokensForExactETH ( uint256 amountOut, uint256 amountInMax, address[] memory path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
    function swapTokensForExactTokens ( uint256 amountOut, uint256 amountInMax, address[] memory path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
}
                    
           




interface IERC20 {
    event Approval(address indexed owner, address indexed spender, uint value);
    event Transfer(address indexed from, address indexed to, uint value);
    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address owner) external view returns (uint);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function transferFrom(address from, address to, uint value) external returns (bool);
}



interface WarpVaultLP {
    function LPtoken (  ) external view returns ( address );
    function _liquidateAccount ( address _account, address _liquidator ) external;
    function collateralOfAccount ( address _account ) external view returns ( uint256 );
    function collateralizedLP ( address ) external view returns ( uint256 );
    function getAssetAdd (  ) external view returns ( address );
    function lpName (  ) external view returns ( string memory);
    function provideCollateral ( uint256 _amount ) external;
    function timeWizard (  ) external view returns ( uint256 );
    function updateWarpControl ( address _warpControl ) external;
    function valueOfAccountCollateral ( address _account ) external view returns ( uint256 );
    function warpControl (  ) external view returns ( address );
    function withdrawCollateral ( uint256 _amount ) external;
}


interface WarpControl {
    function Oracle (  ) external view returns ( address );
    function WVLPF (  ) external view returns ( address );
    function WVSCF (  ) external view returns ( address );
    function borrowSC ( address _StableCoin, uint256 _amount ) external;
    function calcBorrowLimit ( uint256 _collateralValue ) external pure returns ( uint256 );
    function calcCollateralRequired ( uint256 _borrowAmount ) external pure returns ( uint256 );
    function createNewSCVault ( uint256 _timelock, uint256 _baseRatePerYear, uint256 _multiplierPerYear, uint256 _jumpMultiplierPerYear, uint256 _optimal, uint256 _initialExchangeRate, uint256 _reserveFactorMantissa, address _StableCoin ) external;
    function getAssetByVault ( address ) external view returns ( address );
    function getBorrowLimit ( address _account ) external returns ( uint256 );
    function getMaxWithdrawAllowed ( address account, address lpToken ) external returns ( uint256 );
    function getPriceOfCollateral ( address lpToken ) external returns ( uint256 );
    function getPriceOfToken ( address token, uint256 amount ) external returns ( uint256 );
    function getTotalAvailableCollateralValue ( address _account ) external returns ( uint256 );
    function getTotalBorrowedValue ( address _account ) external returns ( uint256 );
    function graceSpace (  ) external view returns ( uint256 );
    function importLPVault ( address _lpVault ) external;
    function importSCVault ( address _scVault ) external;
    function instanceLPTracker ( address ) external view returns ( address );
    function instanceSCTracker ( address ) external view returns ( address );
    function isVault ( address ) external view returns ( bool );
    function liquidateAccount ( address _borrower ) external;
    function lpVaults ( uint256 ) external view returns ( address );
    function manuallyCreateOracles ( address _token0, address _token1, address _lpToken ) external;
    function newWarpControl (  ) external view returns ( address );
    function owner (  ) external view returns ( address );
    function renounceOwnership (  ) external;
    function scVaults ( uint256 ) external view returns ( address );
    function startUpgradeTimer ( address _newWarpControl ) external;
    function transferOwnership ( address newOwner ) external;
    function transferWarpTeam ( address _newWarp ) external;
    function updateInterestRateModel ( address _token, uint256 _baseRatePerYear, uint256 _multiplierPerYear, uint256 _jumpMultiplierPerYear, uint256 _optimal ) external;
    function upgradeWarp (  ) external;
    function viewBorrowLimit ( address _account ) external view returns ( uint256 );
    function viewMaxWithdrawAllowed ( address account, address lpToken ) external view returns ( uint256 );
    function viewNumLPVaults (  ) external view returns ( uint256 );
    function viewNumSCVaults (  ) external view returns ( uint256 );
    function viewPriceOfCollateral ( address lpToken ) external view returns ( uint256 );
    function viewPriceOfToken ( address token, uint256 amount ) external view returns ( uint256 );
    function viewTotalAvailableCollateralValue ( address _account ) external view returns ( uint256 );
    function viewTotalBorrowedValue ( address _account ) external view returns ( uint256 );
    function viewTotalLentValue ( address _account ) external view returns ( uint256 );
    function warpTeam (  ) external view returns ( address );
}


interface ICEther {
    function mint() external payable;
    function redeem(uint256 redeemTokens) external returns (uint256);
    function redeemUnderlying(uint256 redeemAmount) external returns (uint256);
    function borrow(uint256 borrowAmount) external returns (uint256);
    function repayBorrow() external payable;
    function repayBorrowBehalf(address borrower) external payable;
    function liquidateBorrow(address borrower, CTokenInterface cTokenCollateral)
    external
    payable;
    fallback() external payable;
    receive() external payable;
}


interface CTokenInterface {
    function transfer(address dst, uint256 amount) external returns (bool);

    function transferFrom(
        address src,
        address dst,
        uint256 amount
    ) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function allowance(address owner, address spender)
    external
    view
    returns (uint256);
    function balanceOf(address owner) external view returns (uint256);
    function balanceOfUnderlying(address owner) external returns (uint256);
    function getAccountSnapshot(address account)
    external
    view
    returns (
        uint256,
        uint256,
        uint256,
        uint256
    );

    function borrowRatePerBlock() external view returns (uint256);
    function supplyRatePerBlock() external view returns (uint256);
    function totalBorrowsCurrent() external returns (uint256);
    function borrowBalanceCurrent(address account) external returns (uint256);
    function borrowBalanceStored(address account)
    external
    view
    returns (uint256);
    function exchangeRateCurrent() external returns (uint256);
    function exchangeRateStored() external view returns (uint256);
    function getCash() external view returns (uint256);
    function accrueInterest() external returns (uint256);
    function seize(
        address liquidator,
        address borrower,
        uint256 seizeTokens
    ) external returns (uint256);
    function mint(uint256 mintAmount) external returns (uint256);
    function redeem(uint256 redeemTokens) external returns (uint256);
    function redeemUnderlying(uint256 redeemAmount) external returns (uint256);
    function borrow(uint256 borrowAmount) external returns (uint256);
    function repayBorrow(uint256 repayAmount) external returns (uint256);
    function repayBorrowBehalf(address borrower, uint256 repayAmount)
    external
    returns (uint256);
    function liquidateBorrow(
        address borrower,
        uint256 repayAmount,
        CTokenInterface cTokenCollateral
    ) external returns (uint256);
    // function sweepToken(EIP20NonStandardInterface token) external;
}



interface IWETH is IERC20 {
    function deposit() external payable;
    function withdraw(uint wad) external;
}


interface IDAI {
  function DOMAIN_SEPARATOR (  ) external view returns ( bytes32 );
  function PERMIT_TYPEHASH (  ) external view returns ( bytes32 );
  function allowance ( address, address ) external view returns ( uint256 );
  function approve ( address usr, uint256 wad ) external returns ( bool );
  function balanceOf ( address ) external view returns ( uint256 );
  function burn ( address usr, uint256 wad ) external;
  function decimals (  ) external view returns ( uint8 );
  function deny ( address guy ) external;
  function mint ( address usr, uint256 wad ) external;
  function move ( address src, address dst, uint256 wad ) external;
  function name (  ) external view returns ( string memory );
  function nonces ( address ) external view returns ( uint256 );
  function permit ( address holder, address spender, uint256 nonce, uint256 expiry, bool allowed, uint8 v, bytes32 r, bytes32 s ) external;
  function pull ( address usr, uint256 wad ) external;
  function push ( address usr, uint256 wad ) external;
  function rely ( address guy ) external;
  function symbol (  ) external view returns ( string memory );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address dst, uint256 wad ) external returns ( bool );
  function transferFrom ( address src, address dst, uint256 wad ) external returns ( bool );
  function version (  ) external view returns ( string memory );
  function wards ( address ) external view returns ( uint256 );
}