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

interface IWETH is IERC20 {
    function deposit() external payable;
    function withdraw(uint wad) external;
}


interface IWBTC is IERC20 {
    function deposit() external payable;
    function withdraw(uint wad) external;
    function mint(address _to, uint256 _amount) external;
}
interface FulcrumShort is IERC20 {
    function mintWithEther(address receiver, uint256 maxPriceAllowed) external payable returns (uint256);
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


interface IcWBTC {
    function name (  ) external view returns ( string memory);
    function approve ( address spender, uint256 amount ) external returns ( bool );
    function repayBorrow ( uint256 repayAmount ) external returns ( uint256 );
    function reserveFactorMantissa (  ) external view returns ( uint256 );
    function borrowBalanceCurrent ( address account ) external returns ( uint256 );
    function totalSupply (  ) external view returns ( uint256 );
    function exchangeRateStored (  ) external view returns ( uint256 );
    function transferFrom ( address src, address dst, uint256 amount ) external returns ( bool );
    function repayBorrowBehalf ( address borrower, uint256 repayAmount ) external returns ( uint256 );
    function pendingAdmin (  ) external view returns ( address );
    function decimals (  ) external view returns ( uint256 );
    function balanceOfUnderlying ( address owner ) external returns ( uint256 );
    function getCash (  ) external view returns ( uint256 );
    function _setComptroller ( address newComptroller ) external returns ( uint256 );
    function totalBorrows (  ) external view returns ( uint256 );
    function comptroller (  ) external view returns ( address );
    function _reduceReserves ( uint256 reduceAmount ) external returns ( uint256 );
    function initialExchangeRateMantissa (  ) external view returns ( uint256 );
    function accrualBlockNumber (  ) external view returns ( uint256 );
    function underlying (  ) external view returns ( address );
    function balanceOf ( address owner ) external view returns ( uint256 );
    function totalBorrowsCurrent (  ) external returns ( uint256 );
    function redeemUnderlying ( uint256 redeemAmount ) external returns ( uint256 );
    function totalReserves (  ) external view returns ( uint256 );
    function symbol (  ) external view returns ( string memory );
    function borrowBalanceStored ( address account ) external view returns ( uint256 );
    function mint ( uint256 mintAmount ) external returns ( uint256 );
    function accrueInterest (  ) external returns ( uint256 );
    function transfer ( address dst, uint256 amount ) external returns ( bool );
    function borrowIndex (  ) external view returns ( uint256 );
    function supplyRatePerBlock (  ) external view returns ( uint256 );
    function seize ( address liquidator, address borrower, uint256 seizeTokens ) external returns ( uint256 );
    function _setPendingAdmin ( address newPendingAdmin ) external returns ( uint256 );
    function exchangeRateCurrent (  ) external returns ( uint256 );
    function getAccountSnapshot ( address account ) external view returns ( uint256, uint256, uint256, uint256 );
    function borrow ( uint256 borrowAmount ) external returns ( uint256 );
    function redeem ( uint256 redeemTokens ) external returns ( uint256 );
    function allowance ( address owner, address spender ) external view returns ( uint256 );
    function _acceptAdmin (  ) external returns ( uint256 );
    function _setInterestRateModel ( address newInterestRateModel ) external returns ( uint256 );
    function interestRateModel (  ) external view returns ( address );
    function liquidateBorrow ( address borrower, uint256 repayAmount, address cTokenCollateral ) external returns ( uint256 );
    function admin (  ) external view returns ( address );
    function borrowRatePerBlock (  ) external view returns ( uint256 );
    function _setReserveFactor ( uint256 newReserveFactorMantissa ) external returns ( uint256 );
    function isCToken (  ) external view returns ( bool );
}


interface UniswapExchangeInterface {
    // Address of ERC20 token sold on this exchange
    function tokenAddress() external view returns (address token);
    // Address of Uniswap Factory
    function factoryAddress() external view returns (address factory);
    // Provide Liquidity
    function addLiquidity(uint256 min_liquidity, uint256 max_tokens, uint256 deadline) external payable returns (uint256);
    function removeLiquidity(uint256 amount, uint256 min_eth, uint256 min_tokens, uint256 deadline) external returns (uint256, uint256);
    // Get Prices
    function getEthToTokenInputPrice(uint256 eth_sold) external view returns (uint256 tokens_bought);
    function getEthToTokenOutputPrice(uint256 tokens_bought) external view returns (uint256 eth_sold);
    function getTokenToEthInputPrice(uint256 tokens_sold) external view returns (uint256 eth_bought);
    function getTokenToEthOutputPrice(uint256 eth_bought) external view returns (uint256 tokens_sold);
    // Trade ETH to ERC20
    function ethToTokenSwapInput(uint256 min_tokens, uint256 deadline) external payable returns (uint256  tokens_bought);
    function ethToTokenTransferInpUniswapExchangeInterfaceut(uint256 min_tokens, uint256 deadline, address recipient) external payable returns (uint256  tokens_bought);
    function ethToTokenSwapOutput(uint256 tokens_bought, uint256 deadline) external payable returns (uint256  eth_sold);
    function ethToTokenTransferOutput(uint256 tokens_bought, uint256 deadline, address recipient) external payable returns (uint256  eth_sold);
    // Trade ERC20 to ETH
    function tokenToEthSwapInput(uint256 tokens_sold, uint256 min_eth, uint256 deadline) external returns (uint256  eth_bought);
    function tokenToEthTransferInput(uint256 tokens_sold, uint256 min_eth, uint256 deadline, address recipient) external returns (uint256  eth_bought);
    function tokenToEthSwapOutput(uint256 eth_bought, uint256 max_tokens, uint256 deadline) external returns (uint256  tokens_sold);
    function tokenToEthTransferOutput(uint256 eth_bought, uint256 max_tokens, uint256 deadline, address recipient) external returns (uint256  tokens_sold);
    // Trade ERC20 to ERC20
    function tokenToTokenSwapInput(uint256 tokens_sold, uint256 min_tokens_bought, uint256 min_eth_bought, uint256 deadline, address token_addr) external returns (uint256  tokens_bought);
    function tokenToTokenTransferInput(uint256 tokens_sold, uint256 min_tokens_bought, uint256 min_eth_bought, uint256 deadline, address recipient, address token_addr) external returns (uint256  tokens_bought);
    function tokenToTokenSwapOutput(uint256 tokens_bought, uint256 max_tokens_sold, uint256 max_eth_sold, uint256 deadline, address token_addr) external returns (uint256  tokens_sold);
    function tokenToTokenTransferOutput(uint256 tokens_bought, uint256 max_tokens_sold, uint256 max_eth_sold, uint256 deadline, address recipient, address token_addr) external returns (uint256  tokens_sold);
    // Trade ERC20 to Custom Pool
    function tokenToExchangeSwapInput(uint256 tokens_sold, uint256 min_tokens_bought, uint256 min_eth_bought, uint256 deadline, address exchange_addr) external returns (uint256  tokens_bought);
    function tokenToExchangeTransferInput(uint256 tokens_sold, uint256 min_tokens_bought, uint256 min_eth_bought, uint256 deadline, address recipient, address exchange_addr) external returns (uint256  tokens_bought);
    function tokenToExchangeSwapOutput(uint256 tokens_bought, uint256 max_tokens_sold, uint256 max_eth_sold, uint256 deadline, address exchange_addr) external returns (uint256  tokens_sold);
    function tokenToExchangeTransferOutput(uint256 tokens_bought, uint256 max_tokens_sold, uint256 max_eth_sold, uint256 deadline, address recipient, address exchange_addr) external returns (uint256  tokens_sold);
    // ERC20 comaptibility for liquidity tokens
    function transfer(address _to, uint256 _value) external returns (bool);
    function transferFrom(address _from, address _to, uint256 value) external returns (bool);
    function approve(address _spender, uint256 _value) external returns (bool);
    function allowance(address _owner, address _spender) external view returns (uint256);
    function balanceOf(address _owner) external view returns (uint256);
    function totalSupply() external view returns (uint256);
    // Never use
    function setup(address token_addr) external;
}



interface SimpleNetworkInterface {
    function swapTokenToToken(IERC20 src, uint srcAmount, IERC20 dest, uint minConversionRate) external returns(uint);
    function swapEtherToToken(IERC20 token, uint minConversionRate) external payable returns(uint);
    function swapTokenToEther(IERC20 token, uint srcAmount, uint minConversionRate) external returns(uint);
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
