// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;

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


interface cERC20 is IERC20 {
    function mint(uint mintAmount) external returns (uint);
    function borrow(uint borrowAmount) external returns (uint);
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



interface Comptroller {
    function _addCompMarkets ( address[] calldata cTokens ) external;
    function _become ( address unitroller ) external;
    function _borrowGuardianPaused (  ) external view returns ( bool );
    function _changeMiningRule (  ) external;
    function _dropCompMarket ( address cToken ) external;
    function _mintGuardianPaused (  ) external view returns ( bool );
    function _setBorrowPaused ( address cToken, bool state ) external returns ( bool );
    function _setCloseFactor ( uint256 newCloseFactorMantissa ) external returns ( uint256 );
    function _setCollateralFactor ( address cToken, uint256 newCollateralFactorMantissa ) external returns ( uint256 );
    function _setCompRate ( uint256 compRate_ ) external;
    function _setLiquidationIncentive ( uint256 newLiquidationIncentiveMantissa ) external returns ( uint256 );
    function _setMaxAssets ( uint256 newMaxAssets ) external returns ( uint256 );
    function _setMiningBuff ( address cToken, uint256 buff ) external;
    function _setMintPaused ( address cToken, bool state ) external returns ( bool );
    function _setPauseGuardian ( address newPauseGuardian ) external returns ( uint256 );
    function _setPriceOracle ( address newOracle ) external returns ( uint256 );
    function _setSeizePaused ( bool state ) external returns ( bool );
    function _setTransferPaused ( bool state ) external returns ( bool );
    function _supportMarket ( address cToken ) external returns ( uint256 );
    function accountAssets ( address, uint256 ) external view returns ( address );
    function admin (  ) external view returns ( address );
    function allMarkets ( uint256 ) external view returns ( address );
    function borrowAllowed ( address cToken, address borrower, uint256 borrowAmount ) external returns ( uint256 );
    function borrowGuardianPaused ( address ) external view returns ( bool );
    function borrowVerify ( address cToken, address borrower, uint256 borrowAmount ) external;
    function checkMembership ( address account, address cToken ) external view returns ( bool );
    function claimComp ( address holder, address[] calldata cTokens ) external;
    function claimComp ( address[] calldata holders, address[] calldata cTokens, bool borrowers, bool suppliers ) external;
    function claimComp ( address holder ) external;
    function closeFactorMantissa (  ) external view returns ( uint256 );
    function compAccrued ( address ) external view returns ( uint256 );
    function compBorrowState ( address ) external view returns ( uint224 index, uint32 block2 );
    function compBorrowerIndex ( address, address ) external view returns ( uint256 );
    function compClaimThreshold (  ) external view returns ( uint256 );
    function compInitialIndex (  ) external view returns ( uint224 );
    function compRate (  ) external view returns ( uint256 );
    function compSpeeds ( address ) external view returns ( uint256 );
    function compSupplierIndex ( address, address ) external view returns ( uint256 );
    function compSupplyState ( address ) external view returns ( uint224 index, uint32 block3 );
    function comptrollerImplementation (  ) external view returns ( address );
    function enterMarkets ( address[] calldata cTokens ) external returns ( uint256[] memory );
    function exitMarket ( address cTokenAddress ) external returns ( uint256 );
    function getAccountLiquidity ( address account ) external view returns ( uint256, uint256, uint256 );
    function getAllMarkets (  ) external view returns ( address[] memory );
    function getAssetsIn ( address account ) external view returns ( address[] memory);
    function getBlockNumber (  ) external view returns ( uint256 );
    function getCheeseAddress (  ) external view returns ( address );
    function getHypotheticalAccountLiquidity ( address account, address cTokenModify, uint256 redeemTokens, uint256 borrowAmount ) external view returns ( uint256, uint256, uint256 );
    function isComptroller (  ) external view returns ( bool );
    function liquidateBorrowAllowed ( address cTokenBorrowed, address cTokenCollateral, address liquidator, address borrower, uint256 repayAmount ) external returns ( uint256 );
    function liquidateBorrowVerify ( address cTokenBorrowed, address cTokenCollateral, address liquidator, address borrower, uint256 actualRepayAmount, uint256 seizeTokens ) external;
    function liquidateCalculateSeizeTokens ( address cTokenBorrowed, address cTokenCollateral, uint256 actualRepayAmount ) external view returns ( uint256, uint256 );
    function liquidationIncentiveMantissa (  ) external view returns ( uint256 );
    function markets ( address ) external view returns ( bool isListed, uint256 collateralFactorMantissa, bool isComped );
    function maxAssets (  ) external view returns ( uint256 );
    function miningBuff ( address ) external view returns ( uint256 );
    function miningRule (  ) external view returns ( uint256 );
    function mintAllowed ( address cToken, address minter, uint256 mintAmount ) external returns ( uint256 );
    function mintGuardianPaused ( address ) external view returns ( bool );
    function mintVerify ( address cToken, address minter, uint256 actualMintAmount, uint256 mintTokens ) external;
    function oracle (  ) external view returns ( address );
    function pauseGuardian (  ) external view returns ( address );
    function pendingAdmin (  ) external view returns ( address );
    function pendingComptrollerImplementation (  ) external view returns ( address );
    function redeemAllowed ( address cToken, address redeemer, uint256 redeemTokens ) external returns ( uint256 );
    function redeemVerify ( address cToken, address redeemer, uint256 redeemAmount, uint256 redeemTokens ) external;
    function refreshCompSpeeds (  ) external;
    function repayBorrowAllowed ( address cToken, address payer, address borrower, uint256 repayAmount ) external returns ( uint256 );
    function repayBorrowVerify ( address cToken, address payer, address borrower, uint256 actualRepayAmount, uint256 borrowerIndex ) external;
    function seizeAllowed ( address cTokenCollateral, address cTokenBorrowed, address liquidator, address borrower, uint256 seizeTokens ) external returns ( uint256 );
    function seizeGuardianPaused (  ) external view returns ( bool );
    function seizeVerify ( address cTokenCollateral, address cTokenBorrowed, address liquidator, address borrower, uint256 seizeTokens ) external;
    function transferAllowed ( address cToken, address src, address dst, uint256 transferTokens ) external returns ( uint256 );
    function transferGuardianPaused (  ) external view returns ( bool );
    function transferVerify ( address cToken, address src, address dst, uint256 transferTokens ) external;
}




interface ComptrollerInterface {
    function isComptroller() external view returns (bool);

    function enterMarkets(address[] calldata cTokens)
    external
    returns (uint256[] memory);

    function exitMarket(address cToken) external returns (uint256);

    function mintAllowed(
        address cToken,
        address minter,
        uint256 mintAmount
    ) external returns (uint256);

    function mintVerify(
        address cToken,
        address minter,
        uint256 mintAmount,
        uint256 mintTokens
    ) external;

    function redeemAllowed(
        address cToken,
        address redeemer,
        uint256 redeemTokens
    ) external returns (uint256);

    function redeemVerify(
        address cToken,
        address redeemer,
        uint256 redeemAmount,
        uint256 redeemTokens
    ) external;

    function borrowAllowed(
        address cToken,
        address borrower,
        uint256 borrowAmount
    ) external returns (uint256);

    function borrowVerify(
        address cToken,
        address borrower,
        uint256 borrowAmount
    ) external;

    function repayBorrowAllowed(
        address cToken,
        address payer,
        address borrower,
        uint256 repayAmount
    ) external returns (uint256);

    function repayBorrowVerify(
        address cToken,
        address payer,
        address borrower,
        uint256 repayAmount,
        uint256 borrowerIndex
    ) external;

    function liquidateBorrowAllowed(
        address cTokenBorrowed,
        address cTokenCollateral,
        address liquidator,
        address borrower,
        uint256 repayAmount
    ) external returns (uint256);

    function liquidateBorrowVerify(
        address cTokenBorrowed,
        address cTokenCollateral,
        address liquidator,
        address borrower,
        uint256 repayAmount,
        uint256 seizeTokens
    ) external;

    function seizeAllowed(
        address cTokenCollateral,
        address cTokenBorrowed,
        address liquidator,
        address borrower,
        uint256 seizeTokens
    ) external returns (uint256);

    function seizeVerify(
        address cTokenCollateral,
        address cTokenBorrowed,
        address liquidator,
        address borrower,
        uint256 seizeTokens
    ) external;

    function transferAllowed(
        address cToken,
        address src,
        address dst,
        uint256 transferTokens
    ) external returns (uint256);

    function transferVerify(
        address cToken,
        address src,
        address dst,
        uint256 transferTokens
    ) external;
    /*** Liquidity/Liquidation Calculations ***/
    function liquidateCalculateSeizeTokens(
        address cTokenBorrowed,
        address cTokenCollateral,
        uint256 repayAmount
    ) external view returns (uint256, uint256);
}



interface CheesePriceOracle {
    function anchorPeriod (  ) external view returns ( uint256 );
    function ethBaseUnit (  ) external view returns ( uint256 );
    function expScale (  ) external view returns ( uint256 );
    function getUnderlyingPrice ( address sToken ) external view returns ( uint256 );
    function maxTokens (  ) external view returns ( uint256 );
    function newObservations ( bytes32 ) external view returns ( uint256 timestamp, uint256 acc );
    function numTokens (  ) external view returns ( uint256 );
    function oldObservations ( bytes32 ) external view returns ( uint256 timestamp, uint256 acc );
    function price ( string memory symbol ) external view returns ( uint256 );
    function prices ( bytes32 ) external view returns ( uint256 );
    function refresh ( string[] memory symbols ) external;
    function source ( bytes memory message, bytes memory signature ) external pure returns ( address );
}



