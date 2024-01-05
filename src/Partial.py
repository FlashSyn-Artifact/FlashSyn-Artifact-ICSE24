from forge.forgeCollect import * 
import config
import itertools
from Actions.Utils import *


class Partial(): 
    PossibleActions = []
    def __init__(self):
        self.Actions = []
    
    def __init__(self, a):
        self.Actions = a + [Sketch()] 

    def setPossibleActions(p):
        assert isinstance(p, list)
        Partial.PossibleActions = p

    def size(self):
        return len(self.Actions)

    def expand(self, isPartial): # True for expandPartial
                                  # False for expandContract
        # TODO: Pruning 1: Token Flow Pruning
        # TODO: Pruning 2: Max Call Times
        expandlist = []
        for a in Partial.PossibleActions:
            temp = []
            temp = list(self.Actions[:-1])
            temp.append(a)

            if isPartial:
                expandlist.append(Partial(temp))
            else:
                expandlist.append(Contract(temp))

        return expandlist

    def expandPartial(self):
        return self.expand(True)


    def expandContract(self):
        return self.expand(False)


    def string(self):
        temp = ""
        for ii in range(len(self.Actions)):
            if ii != len(self.Actions) - 1:
                temp += self.Actions[ii].string() + ", "
            else:
                temp += self.Actions[ii].string()
        return temp



class Contract(Partial):
    def __init__(self, a):
        self.Actions = a
        Contract.totalPoints = 1000 * len(a)
        self.pointsPerAction = int( Contract.totalPoints ** (1/len(a)) )

    # TODO: Add DVD, change several functions
    def singleEnumerate(self, actionWrapper, para_append):
        attackContractName = config.benchmarkName + "_attack"
        para_product = list(itertools.product(*para_append))
        attackContract = actionWrapper.buildAttackContract(self.Actions)

        forge = forgedataCollectContract(attackContractName, config.initialEther, config.blockNum)
        forge.updateAttackContract(attackContract)

        for pp in para_product:
            forge.addDataCollector(pp)

        forge.updateDataCollectorContract()
        datapoints = forge.executeCollectData()
        return datapoints
    
    def multiEnumerate(self, actionWrapper, maxminRangeList):
        currentStep = []
        # initial Pass
        para_append = []
        index = 0
        for action in self.Actions:
            if action.numInputs == 0:
                continue
            maxRange = maxminRangeList[index][1]
            minRange = maxminRangeList[index][0]
            index += 1
            paras_this_action = range(minRange, maxRange + 1, max(1, (maxRange - minRange) // self.pointsPerAction) )
            currentStep.append((maxRange - minRange) // self.pointsPerAction)
            print("maxRange: ", maxRange, "  minRange", minRange, "  currentStep", (maxRange - minRange) // self.pointsPerAction)
            
            para_append.append(paras_this_action)
        datapoints = self.singleEnumerate(actionWrapper, para_append)
        # print(currentStep)
        bestProfit = 0
        bestPara = []
        for datapoint in datapoints:
            
            profit = actionWrapper.calcProfit(datapoint[1])
            if  profit > bestProfit and profit > 1:
                bestProfit = profit
                bestPara = datapoint[0]
                # print("get new higher profit: ", profit)
        
        print("Profit of initial pass: ", bestProfit)
        # loop until no higher profit
        # min step size = max(1, max // 10000)

        while len(bestPara) > 0 and True:
            para_append = []
            ParaIndex = 0
            for ii in range(len(self.Actions)):
                if self.Actions[ii].numInputs == 0:
                    continue
                maxRange = bestPara[ParaIndex] + currentStep[ParaIndex]
                minRange = max(0, bestPara[ParaIndex] - currentStep[ParaIndex])
                paras_this_action = range(minRange, maxRange + 1, max(1, (maxRange - minRange) // self.pointsPerAction) )
                currentStep[ParaIndex] = (max(1, (maxRange - minRange) // self.pointsPerAction))
                ParaIndex += 1
                para_append.append(paras_this_action)
                print("maxRange: ", maxRange, "  minRange", minRange, "  currentStep", max(1, (maxRange - minRange) // self.pointsPerAction) )

            datapoints = self.singleEnumerate(actionWrapper, para_append)
            bestProfit_this_round = 0
            bestPara_this_round = []
            for datapoint in datapoints:
                profit = actionWrapper.calcProfit(datapoint[1])
                if  profit > bestProfit_this_round:
                    bestProfit_this_round = profit
                    bestPara_this_round = datapoint[0]
            print("Profit of new pass: ", bestProfit_this_round)
            if bestProfit_this_round <= bestProfit * 1.00001:
                break
            else:
                bestProfit = bestProfit_this_round
                bestPara = bestPara_this_round

        return bestProfit
        

    def optimizeEnumerate(self, actionWrapper, definedmaxminRange = None):
        # if we get a range from other means, use that range
        if definedmaxminRange:
            return self.multiEnumerate(actionWrapper, definedmaxminRange)
        
        # otherwise, simply use the range given by actions' upper limit
        maxminRange = []
        for action in self.Actions:
            if action.numInputs == 0:
                continue
            maxminRange.append(action.range)
        return self.multiEnumerate(actionWrapper, maxminRange)


    
    def testOneContract(self, actionWrapper, paras):
        para_append = []
        for i in range(len(self.Actions)):
            if self.Actions[i].numInputs == 0:
                continue
            para_append.append( [int(paras[i] * 999 / 1000), int(paras[i]), int(paras[i] * 1001 / 1000)] )

        return self.singleEnumerate(actionWrapper, para_append)
