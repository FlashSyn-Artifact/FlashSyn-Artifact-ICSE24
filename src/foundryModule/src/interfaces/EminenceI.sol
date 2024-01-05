// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;



interface EminenceCurrency {
    function CURVE() external view returns (address);

    function DAI() external view returns (address);

    function addGM(address _gm) external;

    function addNPC(address _npc) external;

    function allowance(address owner, address spender)
    external
    view
    returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function award(address _to, uint256 _amount) external;

    function balanceOf(address account) external view returns (uint256);

    function buy(uint256 _amount, uint256 _min)
    external
    returns (uint256 _bought);

    function calculateContinuousBurnReturn(uint256 _amount)
    external
    view
    returns (uint256 burnAmount);

    function calculateContinuousMintReturn(uint256 _amount)
    external
    view
    returns (uint256 mintAmount);

    function claim(address _from, uint256 _amount) external;

    function decimals() external view returns (uint8);

    function decreaseAllowance(address spender, uint256 subtractedValue)
    external
    returns (bool);

    function gamemasters(address) external view returns (bool);

    function increaseAllowance(address spender, uint256 addedValue)
    external
    returns (bool);

    function name() external view returns (string memory);

    function npcs(address) external view returns (bool);

    function reserveBalance() external view returns (uint256);

    function reserveRatio() external view returns (uint32);

    function revokeGM(address _gm) external;

    function revokeNPC(address _npc) external;

    function scale() external view returns (uint256);

    function sell(uint256 _amount, uint256 _min)
    external
    returns (uint256 _bought);

    function symbol() external view returns (string memory);

    function totalSupply() external view returns (uint256);

    function transfer(address recipient, uint256 amount)
    external
    returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);
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
