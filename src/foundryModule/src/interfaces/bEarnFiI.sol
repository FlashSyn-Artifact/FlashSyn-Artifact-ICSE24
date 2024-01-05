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


interface IBvaultsbank {
    function add ( uint256 _allocPoint, address _want, bool _withUpdate, address _strategy ) external;
    function addRewardPool ( address _rewardToken, uint256 _rewardPerBlock ) external;
    function deposit ( uint256 _pid, uint256 _wantAmt ) external;
    function emergencyWithdraw ( uint256 _pid ) external;
    //function executeTransaction ( address target, uint256 value, string signature, bytes data ) external returns ( bytes );
    function getMultiplier ( uint256 _from, uint256 _to ) external pure returns ( uint256 );
    function inCaseTokensGetStuck ( address _token, uint256 _amount, address _to ) external;
    function initialize ( uint256 _startBlock, address _bfi, uint256 _bfiRewardRate, address _bdo, uint256 _bdoRewardRate ) external;
    function initialized (  ) external view returns ( bool );
    function massUpdatePools (  ) external;
    function migrateStrategy ( uint256 _pid, address _newStrategy ) external;
    function operator (  ) external view returns ( address );
    function pausePool ( uint256 ) external view returns ( bool );
    function pendingReward ( uint256 _pid, uint256 _rewardPid, address _user ) external view returns ( uint256 );
    function poolInfo ( uint256 ) external view returns ( address want, uint256 allocPoint, uint256 lastRewardBlock, address strategy );
    function poolLength (  ) external view returns ( uint256 );
    function resetStrategy ( uint256 _pid, address _strategy ) external;
    function rewardPoolInfo ( uint256 ) external view returns ( address rewardToken, uint256 rewardPerBlock, uint256 totalPaidRewards );
    function rewardPoolLength (  ) external view returns ( uint256 );
    function set ( uint256 _pid, uint256 _allocPoint ) external;
    function setPausePool ( uint256 _pid, bool _pausePool ) external;
    function setStopRewardPool ( uint256 _pid, bool _stopRewardPool ) external;
    function setTimelock ( address _timelock ) external;
    function setUnstakingFrozenTime ( uint256 _unstakingFrozenTime ) external;
    function setWhitelisted ( address _account, bool _whitelisted ) external;
    function stakedWantTokens ( uint256 _pid, address _user ) external view returns ( uint256 );
    function startBlock (  ) external view returns ( uint256 );
    function stopRewardPool ( uint256 ) external view returns ( bool );
    function timelock (  ) external view returns ( address );
    function totalAllocPoint (  ) external view returns ( uint256 );
    function unfrozenStakeTime ( uint256 _pid, address _account ) external view returns ( uint256 );
    function unstakingFrozenTime (  ) external view returns ( uint256 );
    function updatePool ( uint256 _pid ) external;
    function updateRewardPerBlock ( uint256 _rewardPid, uint256 _rewardPerBlock ) external;
    function updateRewardToken ( uint256 _rewardPid, address _rewardToken, uint256 _rewardPerBlock ) external;
    function userInfo ( uint256, address ) external view returns ( uint256 shares, uint256 lastStakeTime );
    function whitelisted ( address ) external view returns ( bool );
    function withdraw ( uint256 _pid, uint256 _wantAmt ) external;
    function withdrawAll ( uint256 _pid ) external;
}



interface IFairlaunch {
    function addPool ( uint256 _allocPoint, address _stakeToken, bool _withUpdate ) external;
    function alpaca (  ) external view returns ( address );
    function alpacaPerBlock (  ) external view returns ( uint256 );
    function bonusEndBlock (  ) external view returns ( uint256 );
    function bonusLockUpBps (  ) external view returns ( uint256 );
    function bonusMultiplier (  ) external view returns ( uint256 );
    function deposit ( address _for, uint256 _pid, uint256 _amount ) external;
    function devaddr (  ) external view returns ( address );
    function emergencyWithdraw ( uint256 _pid ) external;
    function getMultiplier ( uint256 _lastRewardBlock, uint256 _currentBlock ) external view returns ( uint256 );
    function harvest ( uint256 _pid ) external;
    function isDuplicatedPool ( address _stakeToken ) external view returns ( bool );
    function manualMint ( address _to, uint256 _amount ) external;
    function massUpdatePools (  ) external;
    function owner (  ) external view returns ( address );
    function pendingAlpaca ( uint256 _pid, address _user ) external view returns ( uint256 );
    function poolInfo ( uint256 ) external view returns ( address stakeToken, uint256 allocPoint, uint256 lastRewardBlock, uint256 accAlpacaPerShare, uint256 accAlpacaPerShareTilBonusEnd );
    function poolLength (  ) external view returns ( uint256 );
    function renounceOwnership (  ) external;
    function setAlpacaPerBlock ( uint256 _alpacaPerBlock ) external;
    function setBonus ( uint256 _bonusMultiplier, uint256 _bonusEndBlock, uint256 _bonusLockUpBps ) external;
    function setDev ( address _devaddr ) external;
    function setPool ( uint256 _pid, uint256 _allocPoint, bool _withUpdate ) external;
    function startBlock (  ) external view returns ( uint256 );
    function totalAllocPoint (  ) external view returns ( uint256 );
    function transferOwnership ( address newOwner ) external;
    function updatePool ( uint256 _pid ) external;
    function userInfo ( uint256, address ) external view returns ( uint256 amount, uint256 rewardDebt, uint256 bonusDebt, address fundedBy );
    function withdraw ( address _for, uint256 _pid, uint256 _amount ) external;
    function withdrawAll ( address _for, uint256 _pid ) external;
}


interface IBvaultsStrategy {
    function balanceInPool (  ) external view returns ( uint256 );
    function busdAddress (  ) external view returns ( address );
    function buyBackAddress1 (  ) external view returns ( address );
    function buyBackAddress2 (  ) external view returns ( address );
    function buyBackRate1 (  ) external view returns ( uint256 );
    function buyBackRate2 (  ) external view returns ( uint256 );
    function buyBackRateMax (  ) external view returns ( uint256 );
    function buyBackRateUL (  ) external view returns ( uint256 );
    function buyBackToken1 (  ) external view returns ( address );
    function buyBackToken2 (  ) external view returns ( address );
    function checkForUnlockReward (  ) external view returns ( bool );
    function controllerFee (  ) external view returns ( uint256 );
    function controllerFeeMax (  ) external view returns ( uint256 );
    function controllerFeeUL (  ) external view returns ( uint256 );
    function convertDustToEarned (  ) external;
    function deposit ( address, uint256 _wantAmt ) external returns ( uint256 );
    function earn (  ) external;
    function earnedAddress (  ) external view returns ( address );
    function emergencyWithraw (  ) external;
    function entranceFeeFactor (  ) external view returns ( uint256 );
    function entranceFeeFactorLL (  ) external view returns ( uint256 );
    function entranceFeeFactorMax (  ) external view returns ( uint256 );
    function executeTransaction ( address target, uint256 value, string calldata signature, bytes calldata data ) external returns ( bytes memory);
    function farm (  ) external;
    function farmContractAddress (  ) external view returns ( address );
    function inCaseTokensGetStuck ( address _token, uint256 _amount, address _to ) external;
    function isAuthorised ( address _account ) external view returns ( bool );
    function isAutoComp (  ) external view returns ( bool );
    function lastEarnBlock (  ) external view returns ( uint256 );
    function notPublic (  ) external view returns ( bool );
    function operator (  ) external view returns ( address );
    function owner (  ) external view returns ( address );
    function paths ( address, address, uint256 ) external view returns ( address );
    function pause (  ) external;
    function paused (  ) external view returns ( bool );
    function pendingHarvest (  ) external view returns ( uint256 );
    function pendingHarvestDollarValue (  ) external view returns ( uint256 );
    function pid (  ) external view returns ( uint256 );
    function renounceOwnership (  ) external;
    function resumeStrategy (  ) external;
    function setBuyBackAddress1 ( address _buyBackAddress1 ) external;
    function setBuyBackAddress2 ( address _buyBackAddress2 ) external;
    function setBuyBackRate1 ( uint256 _buyBackRate1 ) external;
    function setBuyBackRate2 ( uint256 _buyBackRate2 ) external;
    function setCheckForUnlockReward ( bool _checkForUnlockReward ) external;
    function setControllerFee ( uint256 _controllerFee ) external;
    function setEntranceFeeFactor ( uint256 _entranceFeeFactor ) external;
    function setMainPaths ( address[] calldata _earnedToBuyBackToken1Path, address[] calldata _earnedToBuyBackToken2Path, address[] calldata _earnedToWantPath, address[] calldata _earnedToBusdPath, address[] calldata _wantToEarnedPath ) external;
    function setNotPublic ( bool _notPublic ) external;
    function setOperator ( address _operator ) external;
    function setPath ( address _inputToken, address _outputToken, address[] calldata _path ) external;
    function setStrategist ( address _strategist ) external;
    function setTimelock ( address _timelock ) external;
    function sharesTotal (  ) external view returns ( uint256 );
    function strategist (  ) external view returns ( address );
    function strategyStopped (  ) external view returns ( bool );
    function timelock (  ) external view returns ( address );
    function transferOwnership ( address newOwner ) external;
    function uniExchangeRate ( uint256 _tokenAmount, address[] calldata _path ) external view returns ( uint256 );
    function uniRouterAddress (  ) external view returns ( address );
    function unpause (  ) external;
    function vaultContractAddress (  ) external view returns ( address );
    function wantAddress (  ) external view returns ( address );
    function wantLockedTotal (  ) external view returns ( uint256 );
    function wbnbAddress (  ) external view returns ( address );
    function withdraw ( address, uint256 _wantAmt ) external returns ( uint256 );
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