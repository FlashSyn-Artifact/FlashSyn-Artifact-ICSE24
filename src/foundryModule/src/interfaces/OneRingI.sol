// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;

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

interface IOneRingVault {
        function activeStrategy() external view returns (address);
        function allowance(address, address) external view returns (uint256);
        function approve(address spender, uint256 amount) external returns (bool);
        function balanceOf(address account) external view returns (uint256);
        function balanceWithInvested() external view returns (uint256 balance);
        function decimals() external view returns (uint8);
        function decreaseAllowance(address spender, uint256 subtractedValue) external returns (bool);
    function deposit(uint256 _amount, address _token) external;
    function depositSafe(uint256 _amount, address _token, uint256 _minAmount) external;
        function disableUnderlying(address _underlying) external;
    function doHardWork(uint256 _amount, address _token) external;
    function doHardWorkAll() external;
        function enableUnderlying(address _underlying) external;
        function getSharePrice() external view returns (uint256 _sharePrice);
        function increaseAllowance(address spender, uint256 addedValue) external returns (bool);
        function initialize(address[] calldata _underlyings) external;
    function invest(uint256 _amount, address _token) external;
        function migrateStrategy(address _oldStrategy, address _newStrategy, address _underlying, uint256 _usdAmount)
            external;
        function name() external view returns (string memory);
        function owner() external view returns (address);
        function performanceFee() external view returns (uint256);
        function performanceFeeMax() external view returns (uint256);
        function renounceOwnership() external;
        function setActiveStrategy(address _strategy) external;
        function setPerformanceFee(uint256 _performanceFee, uint256 _performanceFeeMax) external;
        function setTreasury(address _treasury) external;
        function symbol() external view returns (string memory);
        function totalSupply() external view returns (uint256);
        function transfer(address recipient, uint256 amount) external returns (bool);
        function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
        function transferOwnership(address newOwner) external;
        function treasury() external view returns (address);
        function underlyingEnabled(address) external view returns (bool);
        function underlyingLength() external view returns (uint256);
        function underlyingUnit() external view returns (uint256);
        function underlyings(uint256) external view returns (address);
    function withdraw(uint256 _amount, address _underlying) external returns (uint256);
    function withdrawAll(address _underlying) external;
    function withdrawSafe(uint256 _amount, address _underlying, uint256 _minAmount) external returns (uint256);
}



interface IfUSDT {
  function DOMAIN_SEPARATOR (  ) external view returns ( bytes32 );
  function PERMIT_TYPEHASH (  ) external view returns ( bytes32 );
  function Swapin ( bytes32 txhash, address account, uint256 amount ) external returns ( bool );
  function Swapout ( uint256 amount, address bindaddr ) external returns ( bool );
  function TRANSFER_TYPEHASH (  ) external view returns ( bytes32 );
  function allowance ( address, address ) external view returns ( uint256 );
  function approve ( address spender, uint256 value ) external returns ( bool );
  function approveAndCall ( address spender, uint256 value, bytes calldata data ) external returns ( bool );
  function balanceOf ( address ) external view returns ( uint256 );
  function burn ( address from, uint256 amount ) external returns ( bool );
  function changeMPCOwner ( address newVault ) external returns ( bool );
  function changeVault ( address newVault ) external returns ( bool );
  function decimals (  ) external view returns ( uint8 );
  function deposit ( uint256 amount, address to ) external returns ( uint256 );
  function deposit ( uint256 amount ) external returns ( uint256 );
  function deposit (  ) external returns ( uint256 );
  function depositVault ( uint256 amount, address to ) external returns ( uint256 );
  function depositWithPermit ( address target, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s, address to ) external returns ( uint256 );
  function depositWithTransferPermit ( address target, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s, address to ) external returns ( uint256 );
  function mint ( address to, uint256 amount ) external returns ( bool );
  function name (  ) external view returns ( string memory );
  function nonces ( address ) external view returns ( uint256 );
  function owner (  ) external view returns ( address );
  function permit ( address target, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s ) external;
  function symbol (  ) external view returns ( string memory );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address to, uint256 value ) external returns ( bool );
  function transferAndCall ( address to, uint256 value, bytes calldata data ) external returns ( bool );
  function transferFrom ( address from, address to, uint256 value ) external returns ( bool );
  function transferWithPermit ( address target, address to, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s ) external returns ( bool );
  function underlying (  ) external view returns ( address );
  function vault (  ) external view returns ( address );
  function withdraw ( uint256 amount, address to ) external returns ( uint256 );
  function withdraw ( uint256 amount ) external returns ( uint256 );
  function withdraw (  ) external returns ( uint256 );
  function withdrawVault ( address from, uint256 amount, address to ) external returns ( uint256 );
}




interface IDAI {
  function DOMAIN_SEPARATOR (  ) external view returns ( bytes32 );
  function PERMIT_TYPEHASH (  ) external view returns ( bytes32 );
  function Swapin ( bytes32 txhash, address account, uint256 amount ) external returns ( bool );
  function Swapout ( uint256 amount, address bindaddr ) external returns ( bool );
  function TRANSFER_TYPEHASH (  ) external view returns ( bytes32 );
  function allowance ( address, address ) external view returns ( uint256 );
  function approve ( address spender, uint256 value ) external returns ( bool );
  function approveAndCall ( address spender, uint256 value, bytes calldata data ) external returns ( bool );
  function balanceOf ( address ) external view returns ( uint256 );
  function changeDCRMOwner ( address newOwner ) external returns ( bool );
  function decimals (  ) external view returns ( uint8 );
  function name (  ) external view returns ( string memory );
  function nonces ( address ) external view returns ( uint256 );
  function owner (  ) external view returns ( address );
  function permit ( address target, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s ) external;
  function symbol (  ) external view returns ( string memory );
  function totalSupply (  ) external view returns ( uint256 );
  function transfer ( address to, uint256 value ) external returns ( bool );
  function transferAndCall ( address to, uint256 value, bytes calldata data ) external returns ( bool );
  function transferFrom ( address from, address to, uint256 value ) external returns ( bool );
  function transferWithPermit ( address target, address to, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s ) external returns ( bool );
}


