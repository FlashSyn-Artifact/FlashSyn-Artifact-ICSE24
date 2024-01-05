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


interface IValueMultiVaultBank {
    function addVaultRewardPool ( address _vault, address _rewardToken, uint256 _startBlock, uint256 _endRewardBlock, uint256 _rewardPerBlock ) external;
    function approveForSpender ( address _token, address _spender, uint256 _amount ) external;
    function calc_token_amount_deposit ( address _vault, uint256[] calldata _amounts ) external view returns ( uint256 );
    function calc_token_amount_withdraw ( address _vault, uint256 _shares, address _output ) external view returns ( uint256 );
    function cap ( address _vault ) external view returns ( uint256 );
    function chi (  ) external view returns ( address );
    function convert_rate ( address _vault, address _input, uint256 _amount ) external view returns ( uint256 );
    function deposit ( address _vault, address _input, uint256 _amount, uint256 _min_mint_amount, bool _isStake, uint8 _flag ) external;
    function depositAll ( address _vault, uint256[] calldata _amounts, uint256 _min_mint_amount, bool _isStake, uint8 _flag ) external;
    function exit ( address _vault, address _output, uint256 _min_output_amount, uint8 _flag ) external;
    function getAllRewards ( address _vault, address _account, uint8 _flag ) external;
    function getReward ( address _vault, uint8 _pid, address _account, uint8 _flag ) external;
    function governance (  ) external view returns ( address );
    function governanceRecoverUnsupported ( address _token, uint256 amount, address to ) external;
    function harvestAllStrategies ( address _vault, uint8 _flag ) external;
    function harvestStrategy ( address _vault, address _strategy, uint8 _flag ) external;
    function harvestWant ( address _vault, address _want, uint8 _flag ) external;
    function pendingReward ( address _vault, uint8 _pid, address _account ) external view returns ( uint256 _pending );
    function rewardPoolInfos ( address, uint256 ) external view returns ( address rewardToken, uint256 lastRewardBlock, uint256 endRewardBlock, uint256 rewardPerBlock, uint256 accRewardPerShare, uint256 totalPaidRewards );
    function setGovernance ( address _governance ) external;
    function setStrategist ( address _strategist ) external;
    function setVaultMaster ( address _vaultMaster ) external;
    function shares_owner ( address _vault, address _account ) external view returns ( uint256 );
    function stakeVaultShares ( address _vault, uint256 _shares ) external;
    function strategist (  ) external view returns ( address );
    function unstake ( address _vault, uint256 _amount, uint8 _flag ) external;
    function updateReward ( address _vault ) external;
    function updateRewardPool ( address _vault, uint8 _pid ) external;
    function updateRewardPool ( address _vault, uint8 _pid, uint256 _endRewardBlock, uint256 _rewardPerBlock ) external;
    function userInfo ( address, address ) external view returns ( uint256 amount );
    function valueToken (  ) external view returns ( address );
    function vaultMaster (  ) external view returns ( address );
    function withdraw ( address _vault, uint256 _shares, address _output, uint256 _min_output_amount, uint8 _flag ) external;
    function withdraw_fee ( address _vault, uint256 _shares ) external view returns ( uint256 );
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


interface IMultiStablesVault {
    function accept ( address _input ) external view returns ( bool );
    function acceptContractDepositor (  ) external view returns ( bool );
    function allowWithdrawFromOtherWant ( address ) external view returns ( bool );
    function allowance ( address owner, address spender ) external view returns ( uint256 );
    function approve ( address spender, uint256 amount ) external returns ( bool );
    function available ( address _want ) external view returns ( uint256 );
    function balance (  ) external view returns ( uint256 );
    function balanceOf ( address account ) external view returns ( uint256 );
    function balance_to_sell (  ) external view returns ( uint256 );
    function basedConverter (  ) external view returns ( address );
    function basedToken (  ) external view returns ( address );
    function calc_token_amount_deposit ( uint256[] calldata _amounts ) external view returns ( uint256 );
    function calc_token_amount_withdraw ( uint256 _shares, address _output ) external view returns ( uint256 );
    function cap (  ) external view returns ( uint256 );
    function claimInsurance (  ) external;
    function controller (  ) external view returns ( address );
    function convert_nonbased_want ( address _want, uint256 _amount ) external;
    function convert_rate ( address _input, uint256 _amount ) external view returns ( uint256 );
    function converterMap ( address ) external view returns ( address );
    function converters ( address ) external view returns ( address );
    function decimals (  ) external view returns ( uint8 );
    function decreaseAllowance ( address spender, uint256 subtractedValue ) external returns ( bool );
    function deposit ( address _input, uint256 _amount, uint256 _min_mint_amount ) external returns ( uint256 );
    function depositAll ( uint256[] calldata _amounts, uint256 _min_mint_amount ) external returns ( uint256 );
    function depositAllFor ( address _account, address _to, uint256[] calldata _amounts, uint256 _min_mint_amount ) external returns ( uint256 _mint_amount );
    function depositFor ( address _account, address _to, address _input, uint256 _amount, uint256 _min_mint_amount ) external returns ( uint256 _mint_amount );
    function earn ( address _want ) external;
    function earnExtra ( address _token ) external;
    function earnLowerlimit (  ) external view returns ( uint256 );
    function getConverter ( address _want ) external view returns ( address );
    function getPricePerFullShare (  ) external view returns ( uint256 );
    function getVaultMaster (  ) external view returns ( address );
    function get_virtual_price (  ) external view returns ( uint256 );
    function governance (  ) external view returns ( address );
    function governanceRecoverUnsupported ( address _token, uint256 amount, address to ) external;
    function harvest ( address reserve, uint256 amount ) external;
    function harvestAllStrategies (  ) external;
    function harvestStrategy ( address _strategy ) external;
    function harvestWant ( address _want ) external;
    function increaseAllowance ( address spender, uint256 addedValue ) external returns ( bool );
    function initialize ( address _basedToken, address _vaultMaster ) external;
    function input2Want ( address ) external view returns ( address );
    function inputTokenIndex ( address ) external view returns ( uint256 );
    function inputTokens ( uint256 ) external view returns ( address );
    function insurance (  ) external view returns ( uint256 );
    function max (  ) external view returns ( uint256 );
    function min (  ) external view returns ( uint256 );
    function name (  ) external view returns ( string calldata );
    function setAcceptContractDepositor ( bool _acceptContractDepositor ) external;
    function setAllowWithdrawFromOtherWant ( address _token, bool _allow ) external;
    function setCap ( uint256 _cap ) external;
    function setController ( address _controller ) external;
    function setConverter ( address _want, address _converter ) external;
    function setConverterMap ( address _token, address _converter ) external;
    function setEarnLowerlimit ( uint256 _earnLowerlimit ) external;
    function setGovernance ( address _governance ) external;
    function setInput2Want ( address _inputToken, address _wantToken ) external;
    function setInputToken ( uint256 _index, address _inputToken ) external;
    function setInputTokens ( address[] calldata _inputTokens ) external;
    function setMin ( uint256 _min ) external;
    function setShareConverter ( address _shareConverter ) external;
    function setVaultMaster ( address _vaultMaster ) external;
    function setWantTokens ( address[] calldata _wantTokens ) external;
    function shareConverter (  ) external view returns ( address );
    function symbol (  ) external view returns ( string calldata );
    function token (  ) external view returns ( address );
    function totalSupply (  ) external view returns ( uint256 );
    function transfer ( address recipient, uint256 amount ) external returns ( bool );
    function transferFrom ( address sender, address recipient, uint256 amount ) external returns ( bool );
    function unwhitelistContract ( address _contract ) external;
    function wantTokenIndex ( address ) external view returns ( uint256 );
    function wantTokens ( uint256 ) external view returns ( address );
    function whitelistContract ( address _contract ) external;
    function whitelistedContract ( address ) external view returns ( bool );
    function withdraw ( uint256 _shares, address _output, uint256 _min_output_amount ) external returns ( uint256 );
    function withdrawFor ( address _account, uint256 _shares, address _output, uint256 _min_output_amount ) external returns ( uint256 _output_amount );
    function withdraw_fee ( uint256 _shares ) external view returns ( uint256 );
}



interface StandardToken {
    function approve(address _spender, uint _value) external;
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


