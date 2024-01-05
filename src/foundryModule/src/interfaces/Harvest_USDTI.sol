// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;

interface IUSDT {
    function name() external view returns (string memory);
    function deprecate(address _upgradedAddress) external;
    function approve(address _spender, uint256 _value) external;
    function deprecated() external view returns (bool);
    function addBlackList(address _evilUser) external;
    function totalSupply() external view returns (uint256);
    function transferFrom(address _from, address _to, uint256 _value) external;
    function upgradedAddress() external view returns (address);
    function balances(address) external view returns (uint256);
    function decimals() external view returns (uint256);
    function maximumFee() external view returns (uint256);
    function _totalSupply() external view returns (uint256);
    function unpause() external;
    function getBlackListStatus(address _maker) external view returns (bool);
    function allowed(address, address) external view returns (uint256);
    function paused() external view returns (bool);
    function balanceOf(address who) external view returns (uint256);
    function pause() external;
    function getOwner() external view returns (address);
    function owner() external view returns (address);
    function symbol() external view returns (string memory);
    function transfer(address _to, uint256 _value) external;
    function setParams(uint256 newBasisPoints, uint256 newMaxFee) external;
    function issue(uint256 amount) external;
    function redeem(uint256 amount) external;
    function allowance(address _owner, address _spender) external view returns (uint256 remaining);
    function basisPointsRate() external view returns (uint256);
    function isBlackListed(address) external view returns (bool);
    function removeBlackList(address _clearedUser) external;
    function MAX_UINT() external view returns (uint256);
    function transferOwnership(address newOwner) external;
    function destroyBlackFunds(address _blackListedUser) external;
}

interface IUSDC {
    // only for Fantom
    function Swapin(bytes32 txhash, address account, uint256 amount) external returns (bool);

    function APPROVE_WITH_AUTHORIZATION_TYPEHASH() external view returns (bytes32);
    function CANCEL_AUTHORIZATION_TYPEHASH() external view returns (bytes32);
    function DECREASE_ALLOWANCE_WITH_AUTHORIZATION_TYPEHASH() external view returns (bytes32);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
    function INCREASE_ALLOWANCE_WITH_AUTHORIZATION_TYPEHASH() external view returns (bytes32);
    function PERMIT_TYPEHASH() external view returns (bytes32);
    function TRANSFER_WITH_AUTHORIZATION_TYPEHASH() external view returns (bytes32);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 value) external returns (bool);
    function approveWithAuthorization(
        address owner,
        address spender,
        uint256 value,
        uint256 validAfter,
        uint256 validBefore,
        bytes32 nonce,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;
    function authorizationState(address authorizer, bytes32 nonce) external view returns (uint8);
    function balanceOf(address account) external view returns (uint256);
    function blacklist(address _account) external;
    function blacklister() external view returns (address);
    function burn(uint256 _amount) external;
    function cancelAuthorization(address authorizer, bytes32 nonce, uint8 v, bytes32 r, bytes32 s) external;
    function configureMinter(address minter, uint256 minterAllowedAmount) external returns (bool);
    function currency() external view returns (string memory);
    function decimals() external view returns (uint8);
    function decreaseAllowance(address spender, uint256 decrement) external returns (bool);
    function decreaseAllowanceWithAuthorization(
        address owner,
        address spender,
        uint256 decrement,
        uint256 validAfter,
        uint256 validBefore,
        bytes32 nonce,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;
    function increaseAllowance(address spender, uint256 increment) external returns (bool);
    function increaseAllowanceWithAuthorization(
        address owner,
        address spender,
        uint256 increment,
        uint256 validAfter,
        uint256 validBefore,
        bytes32 nonce,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;
    function initialize(
        string calldata tokenName,
        string calldata tokenSymbol,
        string calldata tokenCurrency,
        uint8 tokenDecimals,
        address newMasterMinter,
        address newPauser,
        address newBlacklister,
        address newOwner
    ) external;
    function initializeV2(string calldata newName) external;
    function isBlacklisted(address _account) external view returns (bool);
    function isMinter(address account) external view returns (bool);
    function masterMinter() external view returns (address);
    function mint(address _to, uint256 _amount) external returns (bool);
    function minterAllowance(address minter) external view returns (uint256);
    function name() external view returns (string memory);
    function nonces(address owner) external view returns (uint256);
    function owner() external view returns (address);
    function pause() external;
    function paused() external view returns (bool);
    function pauser() external view returns (address);
    function permit(address owner, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s)
        external;
    function removeMinter(address minter) external returns (bool);
    function rescueERC20(address tokenContract, address to, uint256 amount) external;
    function rescuer() external view returns (address);
    function symbol() external view returns (string memory);
    function totalSupply() external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function transferOwnership(address newOwner) external;
    function transferWithAuthorization(
        address from,
        address to,
        uint256 value,
        uint256 validAfter,
        uint256 validBefore,
        bytes32 nonce,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;
    function unBlacklist(address _account) external;
    function unpause() external;
    function updateBlacklister(address _newBlacklister) external;
    function updateMasterMinter(address _newMasterMinter) external;
    function updatePauser(address _newPauser) external;
    function updateRescuer(address newRescuer) external;
}

interface yUSDC {
    function approveToken() external;
    function balance() external view returns (uint256);
    function balanceAave() external view returns (uint256);
    function balanceCompound() external view returns (uint256);
    function balanceCompoundInToken() external view returns (uint256);
    function balanceDydx() external view returns (uint256);
    function balanceFulcrum() external view returns (uint256);
    function balanceFulcrumInToken() external view returns (uint256);
    function calcPoolValueInToken() external view returns (uint256);
    function deposit(uint256 _amount) external;
    function getAave() external view returns (address);
    function getPricePerFullShare() external view returns (uint256);
    function invest(uint256 _amount) external;
    function rebalance() external;
    function recommend() external view returns (uint8);
    function redeem(uint256 _shares) external;
    function supplyAave(uint256 amount) external;
    function supplyDydx(uint256 amount) external returns (uint256);
    function supplyFulcrum(uint256 amount) external;
    function withdraw(uint256 _shares) external;
}

interface yERC20 {
    function get_virtual_price() external returns (uint256 out);
    //   function calc_token_amount ( uint256[4] amounts, bool deposit ) external returns ( uint256 out );
    //   function add_liquidity ( uint256[4] amounts, uint256 min_mint_amount ) external;
    function get_dy(int128 i, int128 j, uint256 dx) external returns (uint256 out);
    function get_dx(int128 i, int128 j, uint256 dy) external returns (uint256 out);
    function get_dy_underlying(int128 i, int128 j, uint256 dx) external returns (uint256 out);
    function get_dx_underlying(int128 i, int128 j, uint256 dy) external returns (uint256 out);
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external;
    function exchange_underlying(int128 i, int128 j, uint256 dx, uint256 min_dy) external;
    //   function remove_liquidity ( uint256 _amount, uint256[4] min_amounts ) external;
    //   function remove_liquidity_imbalance ( uint256[4] amounts, uint256 max_burn_amount ) external;
    function commit_new_parameters(uint256 amplification, uint256 new_fee, uint256 new_admin_fee) external;
    function apply_new_parameters() external;
    function revert_new_parameters() external;
    function commit_transfer_ownership(address _owner) external;
    function apply_transfer_ownership() external;
    function revert_transfer_ownership() external;
    function withdraw_admin_fees() external;
    function kill_me() external;
    function unkill_me() external;
    function coins(int128 arg0) external returns (address out);
    function underlying_coins(int128 arg0) external returns (address out);
    function balances(int128 arg0) external returns (uint256 out);
    function A() external returns (uint256 out);
    function fee() external returns (uint256 out);
    function admin_fee() external returns (uint256 out);
    function owner() external returns (address out);
    function admin_actions_deadline() external returns (uint256 out);
    function transfer_ownership_deadline() external returns (uint256 out);
    function future_A() external returns (uint256 out);
    function future_fee() external returns (uint256 out);
    function future_admin_fee() external returns (uint256 out);
    function future_owner() external returns (address out);
}

interface IERC20 {
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Transfer(address indexed from, address indexed to, uint256 value);

    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
    function totalSupply() external view returns (uint256);
    function balanceOf(address owner) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 value) external returns (bool);
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

interface IfUSDC {
    function allowance(address owner, address spender) external view returns (uint256);
    function announceStrategyUpdate(address _strategy) external;
    function approve(address spender, uint256 amount) external returns (bool);
    function availableToInvestOut() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function canUpdateStrategy(address _strategy) external view returns (bool);
    function controller() external view returns (address);
    function decimals() external view returns (uint8);
    function decreaseAllowance(address spender, uint256 subtractedValue) external returns (bool);
    function deposit(uint256 amount) external;
    function depositFor(uint256 amount, address holder) external;
    function doHardWork() external;
    function finalizeStrategyUpdate() external;
    function finalizeUpgrade() external;
    function futureStrategy() external view returns (address);
    function getPricePerFullShare() external view returns (uint256);
    function governance() external view returns (address);
    function increaseAllowance(address spender, uint256 addedValue) external returns (bool);
    //function initialize ( string calldata name, string calldata symbol, uint8 decimals ) external;
    function initialize(
        address _underlying,
        uint256 _toInvestNumerator,
        uint256 _toInvestDenominator,
        uint256 _underlyingUnit,
        uint256 _implementationChangeDelay,
        uint256 _strategyChangeDelay
    ) external;
    function initialize(address _storage) external;
    function initializeVault(
        address _storage,
        address _underlying,
        uint256 _toInvestNumerator,
        uint256 _toInvestDenominator
    ) external;
    function name() external view returns (string memory);
    function nextImplementation() external view returns (address);
    function nextImplementationDelay() external view returns (uint256);
    function nextImplementationTimestamp() external view returns (uint256);
    function rebalance() external;
    function scheduleUpgrade(address impl) external;
    function setStorage(address _store) external;
    function setStrategy(address _strategy) external;
    function setVaultFractionToInvest(uint256 numerator, uint256 denominator) external;
    function shouldUpgrade() external view returns (bool, address);
    function strategy() external view returns (address);
    function strategyTimeLock() external view returns (uint256);
    function strategyUpdateTime() external view returns (uint256);
    function symbol() external view returns (string memory);
    function totalSupply() external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function underlying() external view returns (address);
    function underlyingBalanceInVault() external view returns (uint256); // here is the important one
    function underlyingBalanceWithInvestment() external view returns (uint256); // here is the important one
    function underlyingBalanceWithInvestmentForHolder(address holder) external view returns (uint256);
    function underlyingUnit() external view returns (uint256);
    function vaultFractionToInvestDenominator() external view returns (uint256);
    function vaultFractionToInvestNumerator() external view returns (uint256);
    function withdraw(uint256 numberOfShares) external;
    function withdrawAll() external;
}

interface IStrategy {
    function __curve() external view returns (address);
    function __ycrv() external view returns (address);
    function arbTolerance() external view returns (uint256);
    function controller() external view returns (address);
    function convertor() external view returns (address);
    function curve() external view returns (address);
    function curvePriceCheckpoint() external view returns (uint256);
    function dai() external view returns (address);
    function depositArbCheck() external view returns (bool);
    function doHardWork() external;
    function governance() external view returns (address);
    function investActivated() external view returns (bool);
    function investedUnderlyingBalance() external view returns (uint256); // important
    function salvage(address recipient, address token, uint256 amount) external;
    function setArbTolerance(uint256 tolerance) external;
    function setConvertor(address _convertor) external;
    function setInvestActivated(bool _investActivated) external;
    function setStorage(address _store) external;
    function store() external view returns (address);
    function tusd() external view returns (address);
    function underlying() external view returns (address);
    function underlyingValueFromYCrv(uint256 ycrvBalance) external view returns (uint256);
    function unsalvagableTokens(address) external view returns (bool);
    function usdc() external view returns (address);
    function usdt() external view returns (address);
    function vault() external view returns (address);
    function withdrawAllToVault() external;
    function withdrawPartialYCRVShares(uint256 shares) external;
    function withdrawToVault(uint256 amountUnderlying) external;
    function yTokenValueFromUnderlying(uint256 amountUnderlying) external view returns (uint256);
    function yTokenValueFromYCrv(uint256 ycrvBalance) external view returns (uint256);
    function yVault() external view returns (address);
    function yVaults(address) external view returns (address);
    function ycrv() external view returns (address);
    function ycrvUnit() external view returns (uint256);
    function ycrvVault() external view returns (address);
    function ydai() external view returns (address);
    function ytusd() external view returns (address);
    function yusdc() external view returns (address);
    function yusdt() external view returns (address);
}

interface StandardToken {
    function approve(address _spender, uint256 _value) external;
}


interface IDAI {
    function DOMAIN_SEPARATOR() external view returns (bytes32);
    function PERMIT_TYPEHASH() external view returns (bytes32);
    function allowance(address, address) external view returns (uint256);
    function approve(address usr, uint256 wad) external returns (bool);
    function balanceOf(address) external view returns (uint256);
    function burn(address usr, uint256 wad) external;
    function decimals() external view returns (uint8);
    function deny(address guy) external;
    function mint(address usr, uint256 wad) external;
    function move(address src, address dst, uint256 wad) external;
    function name() external view returns (string memory);
    function nonces(address) external view returns (uint256);
    function permit(
        address holder,
        address spender,
        uint256 nonce,
        uint256 expiry,
        bool allowed,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;
    function pull(address usr, uint256 wad) external;
    function push(address usr, uint256 wad) external;
    function rely(address guy) external;
    function symbol() external view returns (string memory);
    function totalSupply() external view returns (uint256);
    function transfer(address dst, uint256 wad) external returns (bool);
    function transferFrom(address src, address dst, uint256 wad) external returns (bool);
    function version() external view returns (string memory);
    function wards(address) external view returns (uint256);
}


interface ITUSD {
  function allowance ( address owner, address spender ) external view returns ( uint256 );
  function approve ( address spender, uint256 amount ) external returns ( bool );
  function balanceOf ( address account ) external view returns ( uint256 );
  function burn ( uint256 amount ) external;
  function burnMax (  ) external view returns ( uint256 );
  function burnMin (  ) external view returns ( uint256 );
  function canBurn ( address ) external view returns ( bool );
  function chainReserveFeed (  ) external view returns ( address );
  function chainReserveHeartbeat (  ) external view returns ( uint256 );
  function claimOwnership (  ) external;
  function decimals (  ) external pure returns ( uint8 );
  function decreaseAllowance ( address spender, uint256 subtractedValue ) external returns ( bool );
  function disableProofOfReserve (  ) external;
  function enableProofOfReserve (  ) external;
  function increaseAllowance ( address spender, uint256 addedValue ) external returns ( bool );
  function mint ( address account, uint256 amount ) external;
  function name (  ) external pure returns ( string memory );
  function owner (  ) external view returns ( address );
  function pendingOwner (  ) external view returns ( address );
  function proofOfReserveEnabled (  ) external view returns ( bool );
  function reclaimEther ( address _to ) external;
  function reclaimToken ( address token, address _to ) external;
  function rounding (  ) external pure returns ( uint8 );
  function setBlacklisted ( address account, bool _isBlacklisted ) external;
  function setBurnBounds ( uint256 _min, uint256 _max ) external;
  function setCanBurn ( address account, bool _canBurn ) external;
  function setChainReserveFeed ( address newFeed ) external;
  function setChainReserveHeartbeat ( uint256 newHeartbeat ) external;
  function symbol (  ) external pure returns ( string memory );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address recipient, uint256 amount ) external returns ( bool );
  function transferFrom ( address sender, address recipient, uint256 amount ) external returns ( bool );
  function transferOwnership ( address newOwner ) external;
}


