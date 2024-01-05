// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;





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


interface IPancakeRouter {
    function WETH() external view returns (address);

    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    )
    external
    returns (
        uint256 amountA,
        uint256 amountB,
        uint256 liquidity
    );

    function addLiquidityETH(
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    )
    external
    payable
    returns (
        uint256 amountToken,
        uint256 amountETH,
        uint256 liquidity
    );

    function factory() external view returns (address);

    function getAmountIn(
        uint256 amountOut,
        uint256 reserveIn,
        uint256 reserveOut
    ) external pure returns (uint256 amountIn);

    function getAmountOut(
        uint256 amountIn,
        uint256 reserveIn,
        uint256 reserveOut
    ) external pure returns (uint256 amountOut);

    function getAmountsIn(uint256 amountOut, address[] memory path)
    external
    view
    returns (uint256[] memory amounts);

    function getAmountsOut(uint256 amountIn, address[] memory path)
    external
    view
    returns (uint256[] memory amounts);

    function quote(
        uint256 amountA,
        uint256 reserveA,
        uint256 reserveB
    ) external pure returns (uint256 amountB);

    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountA, uint256 amountB);

    function removeLiquidityETH(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountToken, uint256 amountETH);

    function removeLiquidityETHSupportingFeeOnTransferTokens(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountETH);

    function removeLiquidityETHWithPermit(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline,
        bool approveMax,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (uint256 amountToken, uint256 amountETH);

    function removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline,
        bool approveMax,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (uint256 amountETH);

    function removeLiquidityWithPermit(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline,
        bool approveMax,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (uint256 amountA, uint256 amountB);

    function swapETHForExactTokens(
        uint256 amountOut,
        address[] memory path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts);

    function swapExactETHForTokens(
        uint256 amountOutMin,
        address[] memory path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts);

    function swapExactETHForTokensSupportingFeeOnTransferTokens(
        uint256 amountOutMin,
        address[] memory path,
        address to,
        uint256 deadline
    ) external payable;

    function swapExactTokensForETH(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] memory path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapExactTokensForETHSupportingFeeOnTransferTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] memory path,
        address to,
        uint256 deadline
    ) external;

    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] memory path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapExactTokensForTokensSupportingFeeOnTransferTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] memory path,
        address to,
        uint256 deadline
    ) external;

    function swapTokensForExactETH(
        uint256 amountOut,
        uint256 amountInMax,
        address[] memory path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] memory path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    receive() external payable;
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



interface IBUSD {
  function _decimals (  ) external view returns ( uint8 );
  function _name (  ) external view returns ( string memory );
  function _symbol (  ) external view returns ( string memory );
  function allowance ( address owner, address spender ) external view returns ( uint256 );
  function approve ( address spender, uint256 amount ) external returns ( bool );
  function balanceOf ( address account ) external view returns ( uint256 );
  function burn ( uint256 amount ) external returns ( bool );
  function decimals (  ) external view returns ( uint8 );
  function decreaseAllowance ( address spender, uint256 subtractedValue ) external returns ( bool );
  function getOwner (  ) external view returns ( address );
  function increaseAllowance ( address spender, uint256 addedValue ) external returns ( bool );
  function mint ( uint256 amount ) external returns ( bool );
  function name (  ) external view returns ( string memory );
  function owner (  ) external view returns ( address );
  function renounceOwnership (  ) external;
  function symbol (  ) external view returns ( string memory );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address recipient, uint256 amount ) external returns ( bool );
  function transferFrom ( address sender, address recipient, uint256 amount ) external returns ( bool );
  function transferOwnership ( address newOwner ) external;
}


