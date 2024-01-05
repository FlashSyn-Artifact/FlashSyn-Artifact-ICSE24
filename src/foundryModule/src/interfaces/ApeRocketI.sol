// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;


interface ICAKE {
    function DELEGATION_TYPEHASH (  ) external view returns ( bytes32 );
    function DOMAIN_TYPEHASH (  ) external view returns ( bytes32 );
    function allowance ( address, address ) external view returns ( uint256 );
    function approve ( address spender, uint256 amount ) external returns ( bool );
    function balanceOf ( address account ) external view returns ( uint256 );
    function checkpoints ( address, uint32 ) external view returns ( uint32 fromBlock, uint256 votes );
    function decimals (  ) external view returns ( uint8 );
    function decreaseAllowance ( address spender, uint256 subtractedValue ) external returns ( bool );
    function delegate ( address delegatee ) external;
    function delegateBySig ( address delegatee, uint256 nonce, uint256 expiry, uint8 v, bytes32 r, bytes32 s ) external;
    function delegates ( address delegator ) external view returns ( address );
    function getCurrentVotes ( address account ) external view returns ( uint256 );
    function getOwner (  ) external view returns ( address );
    function getPriorVotes ( address account, uint256 blockNumber ) external view returns ( uint256 );
    function increaseAllowance ( address spender, uint256 addedValue ) external returns ( bool );
    function mint ( address _to, uint256 _amount ) external;
    function mint ( uint256 amount ) external returns ( bool );
    function name (  ) external view returns ( string memory );
    function nonces ( address ) external view returns ( uint256 );
    function numCheckpoints ( address ) external view returns ( uint32 );
    function owner (  ) external view returns ( address );
    function renounceOwnership (  ) external;
    function symbol (  ) external view returns ( string memory );
    function totalSupply (  ) external view returns ( uint256 );
    function transfer ( address recipient, uint256 amount ) external returns ( bool );
    function transferFrom ( address sender, address recipient, uint256 amount ) external returns ( bool );
    function transferOwnership ( address newOwner ) external;
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


interface IAutoCake {
    function ROUTER (  ) external view returns ( address );
    function SPACE (  ) external view returns ( address );
    function balance (  ) external view returns ( uint256 );
    function balanceOf ( address account ) external view returns ( uint256 );
    function deposit ( uint256 _amount ) external;
    function depositAll (  ) external;
    function depositedAt ( address account ) external view returns ( uint256 );
    function disableWhitelist ( bool disable ) external;
    function earned ( address account ) external view returns ( uint256 );
    function getReward (  ) external;
    function harvest (  ) external;
    function initialize ( address _minter ) external;
    function isWhitelist ( address _address ) external view returns ( bool );
    function keeper (  ) external view returns ( address );
    function lastPauseTime (  ) external view returns ( uint256 );
    function minter (  ) external view returns ( address );
    function owner (  ) external view returns ( address );
    function paused (  ) external view returns ( bool );
    function pid (  ) external view returns ( uint256 );
    function poolType (  ) external view returns ( uint8 );
    function priceShare (  ) external view returns ( uint256 );
    function principalOf ( address account ) external view returns ( uint256 );
    function recoverToken ( address token, uint256 amount ) external;
    function renounceOwnership (  ) external;
    function rewardsToken (  ) external view returns ( address );
    function setKeeper ( address _keeper ) external;
    function setMinter ( address newMinter ) external;
    function setPaused ( bool _paused ) external;
    function setSpaceChef ( address newSpaceChef ) external;
    function setWhitelist ( address _address, bool _on ) external;
    function sharesOf ( address account ) external view returns ( uint256 );
    function spaceChef (  ) external view returns ( address );
    function stakingToken (  ) external view returns ( address );
    function totalShares (  ) external view returns ( uint256 );
    function totalSupply (  ) external view returns ( uint256 );
    function transferOwnership ( address newOwner ) external;
    function withdraw ( uint256 shares ) external;
    function withdrawAll (  ) external;
    function withdrawUnderlying ( uint256 _amount ) external;
    function withdrawableBalanceOf ( address account ) external view returns ( uint256 );
}




interface IApeRouter {
    function WETH (  ) external view returns ( address );
    function addLiquidity ( address tokenA, address tokenB, uint256 amountADesired, uint256 amountBDesired, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB, uint256 liquidity );
    function addLiquidityETH ( address token, uint256 amountTokenDesired, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountToken, uint256 amountETH, uint256 liquidity );
    function factory (  ) external view returns ( address );
    function getAmountIn ( uint256 amountOut, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountIn );
    function getAmountOut ( uint256 amountIn, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountOut );
    function getAmountsIn ( uint256 amountOut, address[] calldata path ) external view returns ( uint256[] memory amounts  );
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
    function swapExactTokensForETHSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata  path, address to, uint256 deadline ) external;
    function swapExactTokensForTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
    function swapExactTokensForTokensSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external;
    function swapTokensForExactETH ( uint256 amountOut, uint256 amountInMax, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
    function swapTokensForExactTokens ( uint256 amountOut, uint256 amountInMax, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
}



interface IMasterChef {
  function BONUS_MULTIPLIER (  ) external view returns ( uint256 );
  function add ( uint256 _allocPoint, address _lpToken, bool _withUpdate ) external;
  function cake (  ) external view returns ( address );
  function cakePerBlock (  ) external view returns ( uint256 );
  function deposit ( uint256 _pid, uint256 _amount ) external;
  function dev ( address _devaddr ) external;
  function devaddr (  ) external view returns ( address );
  function emergencyWithdraw ( uint256 _pid ) external;
  function enterStaking ( uint256 _amount ) external;
  function getMultiplier ( uint256 _from, uint256 _to ) external view returns ( uint256 );
  function leaveStaking ( uint256 _amount ) external;
  function massUpdatePools (  ) external;
  function migrate ( uint256 _pid ) external;
  function migrator (  ) external view returns ( address );
  function owner (  ) external view returns ( address );
  function pendingCake ( uint256 _pid, address _user ) external view returns ( uint256 );
  function poolInfo ( uint256 ) external view returns ( address lpToken, uint256 allocPoint, uint256 lastRewardBlock, uint256 accCakePerShare );
  function poolLength (  ) external view returns ( uint256 );
  function renounceOwnership (  ) external;
  function set ( uint256 _pid, uint256 _allocPoint, bool _withUpdate ) external;
  function setMigrator ( address _migrator ) external;
  function startBlock (  ) external view returns ( uint256 );
  function syrup (  ) external view returns ( address );
  function totalAllocPoint (  ) external view returns ( uint256 );
  function transferOwnership ( address newOwner ) external;
  function updateMultiplier ( uint256 multiplierNumber ) external;
  function updatePool ( uint256 _pid ) external;
  function userInfo ( uint256, address ) external view returns ( uint256 amount, uint256 rewardDebt );
  function withdraw ( uint256 _pid, uint256 _amount ) external;
}



interface IApePair {
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
    function swap ( uint256 amount0Out, uint256 amount1Out, address to, bytes memory data ) external;
    function symbol (  ) external view returns ( string memory );
    function sync (  ) external;
    function token0 (  ) external view returns ( address );
    function token1 (  ) external view returns ( address );
    function totalSupply (  ) external view returns ( uint256 );
    function transfer ( address to, uint256 value ) external returns ( bool );
    function transferFrom ( address from, address to, uint256 value ) external returns ( bool );
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


