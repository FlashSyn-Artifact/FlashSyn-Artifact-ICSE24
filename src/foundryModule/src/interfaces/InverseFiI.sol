// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;


interface VyperContract {
    function add_liquidity(uint256[3] calldata amounts, uint256 min_mint_amount) external;
    function balanceOf(address account) external view returns (uint256);
    function mint (address account, uint256 value) external ;
    function approve (address spender, uint256 value) external ;
    function transferUnderlyingTo(address target, uint256 amount) external returns (uint256);
    function deposit (uint amounts, address recipient) external returns (uint256);
    function exchange(address _pool, address _from, address _to, uint256 _amount, uint256 _expected, address _receiver ) external returns (uint256);
    function remove_liquidity_one_coin(uint256 _token_amount, int128 i, uint256 min_amount) external;
    
    function totalSupply() external view returns (uint);

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



interface IWBTC is IERC20 {
    function deposit() external payable;
    function withdraw(uint wad) external;
    function mint(address _to, uint256 _amount) external;
}
interface IUSDT {
  function name (  ) external view returns ( string memory );
  function deprecate ( address _upgradedAddress ) external;
  function approve ( address _spender, uint256 _value ) external;
  function deprecated (  ) external view returns ( bool );
  function addBlackList ( address _evilUser ) external;
  function totalSupply (  ) external view returns ( uint256 );
  function transferFrom ( address _from, address _to, uint256 _value ) external;
  function upgradedAddress (  ) external view returns ( address );
  function balances ( address ) external view returns ( uint256 );
  function decimals (  ) external view returns ( uint256 );
  function maximumFee (  ) external view returns ( uint256 );
  function _totalSupply (  ) external view returns ( uint256 );
  function unpause (  ) external;
  function getBlackListStatus ( address _maker ) external view returns ( bool );
  function allowed ( address, address ) external view returns ( uint256 );
  function paused (  ) external view returns ( bool );
  function balanceOf ( address who ) external view returns ( uint256 );
  function pause (  ) external;
  function getOwner (  ) external view returns ( address );
  function owner (  ) external view returns ( address );
  function symbol (  ) external view returns ( string memory );
  function transfer ( address _to, uint256 _value ) external;
  function setParams ( uint256 newBasisPoints, uint256 newMaxFee ) external;
  function issue ( uint256 amount ) external;
  function redeem ( uint256 amount ) external;
  function allowance ( address _owner, address _spender ) external view returns ( uint256 remaining );
  function basisPointsRate (  ) external view returns ( uint256 );
  function isBlackListed ( address ) external view returns ( bool );
  function removeBlackList ( address _clearedUser ) external;
  function MAX_UINT (  ) external view returns ( uint256 );
  function transferOwnership ( address newOwner ) external;
  function destroyBlackFunds ( address _blackListedUser ) external;
}


interface CErc20Interface {
   function mint(uint mintAmount) external returns (uint);
   function balanceOf(address account) external view returns (uint256);
   function borrow(uint borrowAmount) external returns (uint);
}


interface ICurvePool {
    function A() external view returns (uint256 out);
    function add_liquidity(uint256[2] memory amounts, uint256 min_mint_amount) external;
    function add_liquidity(uint256[3] memory amounts, uint256 min_mint_amount) external;
    function add_liquidity(uint256[4] memory amounts, uint256 min_mint_amount) external;
    function admin_fee() external view returns (uint256 out);
    function balances(uint256 arg0) external view returns (uint256 out);
    function calc_token_amount(uint256[] memory amounts, bool is_deposit) external view returns (uint256 lp_tokens);
    /// @dev vyper upgrade changed this on us
    function coins(int128 arg0) external view returns (address out);
    /// @dev vyper upgrade changed this on us
    function coins(uint256 arg0) external view returns (address out);
    /// @dev vyper upgrade changed this on us
    function underlying_coins(int128 arg0) external view returns (address out);
    /// @dev vyper upgrade changed this on us
    function underlying_coins(uint256 arg0) external view returns (address out);
    function exchange(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external;
    // newer pools have this improved version of exchange_underlying
    function exchange(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy,
        address receiver
    ) external returns (uint256);
    function exchange_underlying(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external;
    function fee() external view returns (uint256 out);
    function future_A() external view returns (uint256 out);
    function future_fee() external view returns (uint256 out);
    function future_admin_fee() external view returns (uint256 out);
    function get_dy(
        int128 i,
        int128 j,
        uint256 dx
    ) external view returns (uint256);
    function get_dy_underlying(
        int128 i,
        int128 j,
        uint256 dx
    ) external view returns (uint256);
    function get_virtual_price() external view returns (uint256 out);
    function remove_liquidity(uint256 token_amount, uint256[3] memory min_amounts) external returns (uint256[3] memory);
    function remove_liquidity_imbalance(uint256[3] memory amounts, uint256 max_burn_amount) external;
    function remove_liquidity_one_coin(
        uint256 token_amount,
        int128 i,
        uint256 min_amount
    ) external;

}



interface IUnitroller {
    function enterMarkets(address[] memory cTokens)
    external
    returns (uint256[] memory);
    function exitMarket(address cTokenAddress) external returns (uint256);
    function cTokensByUnderlying(address) external view returns (address);
    function getAccountLiquidity(address account)
        external
        view
        returns (
            uint256,
            uint256,
            uint256
        );
    function borrowCaps(address) external view returns (uint256);
}


interface IAggregator {
    function latestAnswer() external view returns (int256 answer);
}




