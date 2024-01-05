// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;


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



interface yTokenInterface {
    function allowance ( address owner, address spender ) external view returns ( uint256 );
    function approve ( address spender, uint256 amount ) external returns ( bool );
    function available (  ) external view returns ( uint256 );
    function balance (  ) external view returns ( uint256 );
    function balanceOf ( address account ) external view returns ( uint256 );
    function controller (  ) external view returns ( address );
    function decimals (  ) external view returns ( uint8 );
    function decreaseAllowance ( address spender, uint256 subtractedValue ) external returns ( bool );
    function deposit ( uint256 _amount ) external;
    function depositAll (  ) external;
    function earn (  ) external;
    function getPricePerFullShare (  ) external view returns ( uint256 );
    function governance (  ) external view returns ( address );
    function harvest ( address reserve, uint256 amount ) external;
    function increaseAllowance ( address spender, uint256 addedValue ) external returns ( bool );
    function max (  ) external view returns ( uint256 );
    function min (  ) external view returns ( uint256 );
    function name (  ) external view returns ( string memory );
    function setController ( address _controller ) external;
    function setGovernance ( address _governance ) external;
    function setMin ( uint256 _min ) external;
    function symbol (  ) external view returns ( string memory );
    function token (  ) external view returns ( address );
    function totalSupply (  ) external view returns ( uint256 );
    function transfer ( address recipient, uint256 amount ) external returns ( bool );
    function transferFrom ( address sender, address recipient, uint256 amount ) external returns ( bool );
    function withdraw ( uint256 _shares ) external;
    function withdrawAll (  ) external;
}



interface ICurveFi {
    function A (  ) external view returns ( uint256 );
    function get_virtual_price (  ) external view returns ( uint256 );
    function calc_token_amount ( uint256[3] calldata amounts, bool deposit ) external view returns ( uint256 );
    function add_liquidity ( uint256[3] calldata amounts, uint256 min_mint_amount ) external;
    function get_dy ( int128 i, int128 j, uint256 dx ) external view returns ( uint256 );
    function get_dy_underlying ( int128 i, int128 j, uint256 dx ) external view returns ( uint256 );
    function exchange ( int128 i, int128 j, uint256 dx, uint256 min_dy ) external;
    function remove_liquidity ( uint256 _amount, uint256[3] calldata min_amounts ) external;
    function remove_liquidity_imbalance ( uint256[3] calldata amounts, uint256 max_burn_amount ) external;
    function calc_withdraw_one_coin ( uint256 _token_amount, int128 i ) external view returns ( uint256 );
    function remove_liquidity_one_coin ( uint256 _token_amount, int128 i, uint256 min_amount ) external;
    function ramp_A ( uint256 _future_A, uint256 _future_time ) external;
    function stop_ramp_A (  ) external;
    function commit_new_fee ( uint256 new_fee, uint256 new_admin_fee ) external;
    function apply_new_fee (  ) external;
    function revert_new_parameters (  ) external;
    function commit_transfer_ownership ( address _owner ) external;
    function apply_transfer_ownership (  ) external;
    function revert_transfer_ownership (  ) external;
    function admin_balances ( uint256 i ) external view returns ( uint256 );
    function withdraw_admin_fees (  ) external;
    function donate_admin_fees (  ) external;
    function kill_me (  ) external;
    function unkill_me (  ) external;
    function coins ( uint256 arg0 ) external view returns ( address );
    function balances ( uint256 arg0 ) external view returns ( uint256 );
    function fee (  ) external view returns ( uint256 );
    function admin_fee (  ) external view returns ( uint256 );
    function owner (  ) external view returns ( address );
    function initial_A (  ) external view returns ( uint256 );
    function future_A (  ) external view returns ( uint256 );
    function initial_A_time (  ) external view returns ( uint256 );
    function future_A_time (  ) external view returns ( uint256 );
    function admin_actions_deadline (  ) external view returns ( uint256 );
    function transfer_ownership_deadline (  ) external view returns ( uint256 );
    function future_fee (  ) external view returns ( uint256 );
    function future_admin_fee (  ) external view returns ( uint256 );
    function future_owner (  ) external view returns ( address );
}



interface StandardToken {
    function approve(address _spender, uint _value) external;
}



interface Curve3CrvToken {
    function set_minter ( address _minter ) external;
    function set_name ( string calldata _name, string calldata _symbol ) external;
    function totalSupply (  ) external view returns ( uint256 );
    function allowance ( address _owner, address _spender ) external view returns ( uint256 );
    function transfer ( address _to, uint256 _value ) external returns ( bool );
    function transferFrom ( address _from, address _to, uint256 _value ) external returns ( bool );
    function approve ( address _spender, uint256 _value ) external returns ( bool );
    function mint ( address _to, uint256 _value ) external returns ( bool );
    function burnFrom ( address _to, uint256 _value ) external returns ( bool );
    function name (  ) external view returns ( string memory );
    function symbol (  ) external view returns ( string memory );
    function decimals (  ) external view returns ( uint256 );
    function balanceOf ( address arg0 ) external view returns ( uint256 );
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


interface IUSDC {
    // only for Fantom
    function Swapin(
        bytes32 txhash,
        address account,
        uint256 amount
    ) external returns (bool);

  
  function APPROVE_WITH_AUTHORIZATION_TYPEHASH (  ) external view returns ( bytes32 );
  function CANCEL_AUTHORIZATION_TYPEHASH (  ) external view returns ( bytes32 );
  function DECREASE_ALLOWANCE_WITH_AUTHORIZATION_TYPEHASH (  ) external view returns ( bytes32 );
  function DOMAIN_SEPARATOR (  ) external view returns ( bytes32 );
  function INCREASE_ALLOWANCE_WITH_AUTHORIZATION_TYPEHASH (  ) external view returns ( bytes32 );
  function PERMIT_TYPEHASH (  ) external view returns ( bytes32 );
  function TRANSFER_WITH_AUTHORIZATION_TYPEHASH (  ) external view returns ( bytes32 );
  function allowance ( address owner, address spender ) external view returns ( uint256 );
  function approve ( address spender, uint256 value ) external returns ( bool );
  function approveWithAuthorization ( address owner, address spender, uint256 value, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s ) external;
  function authorizationState ( address authorizer, bytes32 nonce ) external view returns ( uint8 );
  function balanceOf ( address account ) external view returns ( uint256 );
  function blacklist ( address _account ) external;
  function blacklister (  ) external view returns ( address );
  function burn ( uint256 _amount ) external;
  function cancelAuthorization ( address authorizer, bytes32 nonce, uint8 v, bytes32 r, bytes32 s ) external;
  function configureMinter ( address minter, uint256 minterAllowedAmount ) external returns ( bool );
  function currency (  ) external view returns ( string memory );
  function decimals (  ) external view returns ( uint8 );
  function decreaseAllowance ( address spender, uint256 decrement ) external returns ( bool );
  function decreaseAllowanceWithAuthorization ( address owner, address spender, uint256 decrement, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s ) external;
  function increaseAllowance ( address spender, uint256 increment ) external returns ( bool );
  function increaseAllowanceWithAuthorization ( address owner, address spender, uint256 increment, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s ) external;
  function initialize ( string calldata tokenName, string calldata tokenSymbol, string calldata tokenCurrency, uint8 tokenDecimals, address newMasterMinter, address newPauser, address newBlacklister, address newOwner ) external;
  function initializeV2 ( string calldata newName ) external;
  function isBlacklisted ( address _account ) external view returns ( bool );
  function isMinter ( address account ) external view returns ( bool );
  function masterMinter (  ) external view returns ( address );
  function mint ( address _to, uint256 _amount ) external returns ( bool );
  function minterAllowance ( address minter ) external view returns ( uint256 );
  function name (  ) external view returns ( string memory );
  function nonces ( address owner ) external view returns ( uint256 );
  function owner (  ) external view returns ( address );
  function pause (  ) external;
  function paused (  ) external view returns ( bool );
  function pauser (  ) external view returns ( address );
  function permit ( address owner, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s ) external;
  function removeMinter ( address minter ) external returns ( bool );
  function rescueERC20 ( address tokenContract, address to, uint256 amount ) external;
  function rescuer (  ) external view returns ( address );
  function symbol (  ) external view returns ( string memory );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address to, uint256 value ) external returns ( bool );
  function transferFrom ( address from, address to, uint256 value ) external returns ( bool );
  function transferOwnership ( address newOwner ) external;
  function transferWithAuthorization ( address from, address to, uint256 value, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s ) external;
  function unBlacklist ( address _account ) external;
  function unpause (  ) external;
  function updateBlacklister ( address _newBlacklister ) external;
  function updateMasterMinter ( address _newMasterMinter ) external;
  function updatePauser ( address _newPauser ) external;
  function updateRescuer ( address newRescuer ) external;
}
