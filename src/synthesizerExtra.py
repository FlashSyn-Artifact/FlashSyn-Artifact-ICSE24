from collections import deque
from queue import Empty
from re import L 
import time
import config
from heapq import heappush, heappop
from threading import Thread
import multiprocessing
from multiprocessing import Process, Queue, Lock



from Partial import *

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from ActionsExtra.bZx1 import *

from ActionsExtra.Harvest_USDC import Harvest_USDCAction as Harvest_USDCActionExtra, Curve_USDC2USDT as Curve_USDC2USDT_Harvest_USDCExtra, \
                             Curve_USDT2USDC as Curve_USDT2USDC_Harvest_USDCExtra, Curve_DAI2USDC as Curve_DAI2USDC_Harvest_USDCExtra, \
                             Curve_USDC2DAI as Curve_USDC2DAI_Harvest_USDCExtra, Curve_TUSD2USDC as Curve_TUSD2USDC_Harvest_USDCExtra, \
                                Curve_USDC2TUSD as Curve_USDC2TUSD_Harvest_USDCExtra, Curve_TUSD2USDT as Curve_TUSD2USDT_Harvest_USDCExtra, \
                                    Curve_USDT2TUSD as Curve_USDT2TUSD_Harvest_USDCExtra, Curve_DAI2USDT as Curve_DAI2USDT_Harvest_USDCExtra, \
                                        Curve_USDT2DAI as Curve_USDT2DAI_Harvest_USDCExtra, Curve_DAI2TUSD as Curve_DAI2TUSD_Harvest_USDCExtra, \
                                            Curve_TUSD2DAI as Curve_TUSD2DAI_Harvest_USDCExtra, fUSDT_deposit as fUSDT_depositExtra, \
                                                fUSDT_withdraw as fUSDT_withdrawExtra, fUSDT_depositFor as fUSDT_depositForExtra

from ActionsExtra.Harvest_USDT import Harvest_USDTAction as Harvest_USDTActionExtra, Curve_USDT2USDC as Curve_USDT2USDC_Harvest_USDTExtra, \
                            Curve_USDC2USDT as Curve_USDC2USDT_Harvest_USDTExtra, Curve_DAI2USDC as Curve_DAI2USDC_Harvest_USDTExtra, \
                                Curve_USDC2DAI as Curve_USDC2DAI_Harvest_USDTExtra, Curve_TUSD2USDC as Curve_TUSD2USDC_Harvest_USDTExtra, \
                                    Curve_USDC2TUSD as Curve_USDC2TUSD_Harvest_USDTExtra, Curve_TUSD2USDT as Curve_TUSD2USDT_Harvest_USDTExtra, \
                                        Curve_USDT2TUSD as Curve_USDT2TUSD_Harvest_USDTExtra, Curve_DAI2USDT as Curve_DAI2USDT_Harvest_USDTExtra, \
                                            Curve_USDT2DAI as Curve_USDT2DAI_Harvest_USDTExtra, Curve_DAI2TUSD as Curve_DAI2TUSD_Harvest_USDTExtra, \
                                                Curve_TUSD2DAI as Curve_TUSD2DAI_Harvest_USDTExtra, fUSDC_deposit as fUSDC_depositExtra, \
                                                    fUSDC_withdraw as fUSDC_withdrawExtra, fUSDC_depositFor as fUSDC_depositForExtra



from ActionsExtra.Novo import NovoAction as NovoActionExtra, SwapFeeWBNB2NOVO as SwapFeeWBNB2NOVOExtra, SwapFeeNovo2WBNB as SwapFeeNovo2WBNBExtra, \
                            TransferFrom as TransferFromExtra, TransferNovo as TransferNovoExtra, TransferWBNB as TransferWBNBExtra, \
                            PancakePairSync as PancakePairSyncExtra
from ActionsExtra.ApeRocket import ApeRocketAction as ApeRocketActionExtra , DepositAutoCake as DepositAutoCakeExtra, DepositAllAutoCake as DepositAllAutoCakeExtra, \
                                    TransferCAKE as TransferCAKEExtra, TransferWBNBApe as TransferWBNBApeExtra, TransferSPACE as TransferSPACEExtra, HarvestAutoCake as HarvestAutoCakeExtra, \
                                    GetRewardAutoCake as GetRewardAutoCakeExtra, WithdrawAllAutoCake as WithdrawAllAutoCakeExtra, WithdrawUnderlyingAutoCake as WithdrawUnderlyingAutoCakeExtra, SwapSpace2WBNB as SwapSpace2WBNBExtra, \
                                        SwapWBNB2Space as SwapWBNB2SpaceExtra
from ActionsExtra.OneRing import OneRingAction as OneRingActionExtra, DepositSafeOShareUSDC as DepositSafeOShareUSDCExtra, \
                                    DepositSafeOSharefUSDT as DepositSafeOSharefUSDTExtra, DepositOShareUSDC as DepositOShareUSDCExtra, \
                                    DepositOSharefUSDT as DepositOSharefUSDTExtra, WithdrawSafeOShareUSDC as WithdrawSafeOShareUSDCExtra, \
                                    WithdrawSafeOSharefUSDT as WithdrawSafeOSharefUSDTExtra, WithdrawOShareUSDC as WithdrawOShareUSDCExtra, \
                                    WithdrawOSharefUSDT as WithdrawOSharefUSDTExtra, WithdrawSafeOSharefUSDT as WithdrawSafeOSharefUSDTExtra
from ActionsExtra.Wdoge import WdogeAction as WdogeActionExtra, SwapWBNB2Wdoge as SwapWBNB2WdogeExtra, TransferWdoge as TransferWdogeExtra, \
                                    TransferWBNB_Wdoge as TransferWBNB_WdogeExtra, MintUniswap_Wdoge as MintUniswap_WdogeExtra, \
                                    PancakePairSkim as PancakePairSkimExtra, PancakePairSync2 as PancakePairSync2Extra, SwapWdoge2WBNB as SwapWdoge2WBNBExtra
from ActionsExtra.Warp import WarpAction as WarpActionExtra, MintLPUniswapV2 as MintLPUniswapV2Extra, SwapUniswapWETH2DAI as SwapUniswapWETH2DAIExtra, \
                                    SwapUniswapDAI2WETH as SwapUniswapDAI2WETHExtra, LP2BorrowLimit as LP2BorrowLimitExtra, BorrowLimit2LP as BorrowLimit2LPExtra, \
                                    BorrowSC_USDC as BorrowSC_USDCExtra, BorrowSC_DAI as BorrowSC_DAIExtra, BorrowSC_USDT as BorrowSC_USDTExtra

from Actions.bZx1 import *
from Actions.bEarnFi import *
from Actions.Eminence import *
from Actions.ValueDeFi import ValueDeFiAction, VaultBankDeposit, Curve_DAI2USDC as Curve_DAI2USDC_ValueDeFi, ValueWithdrawFor, \
                            Curve_USDT2USDC as Curve_USDT2USDC_ValueDeFi, Curve_USDC2USDT as Curve_USDC2USDT_ValueDeFi, Curve_USDC2DAI as Curve_USDC2DAI_ValueDeFi 




import gc



Q = Queue()
manager = multiprocessing.Manager()
list0 = manager.list()
list1 = manager.list()
list2 = manager.list()
list3 = manager.list()
list4 = manager.list()
list5 = manager.list()
list6 = manager.list()
list7 = manager.list()
lock = manager.Lock()


class PartialObject:
    def __init__(self, Actions, currentStrength):
        self.Actions = Actions
        self.currentStrength = currentStrength


class AnswerObject:
    def __init__(self, Actions, parameters):
        self.Actions = Actions
        self.parameters = parameters

    def __str__(self):
        temp = ""
        action_list = self.Actions
        for ii in range(len(action_list)):
            if ii != len(action_list) - 1:
                temp += action_list[ii].string() + ", "
            else:
                temp += action_list[ii].string()
        temp += ("   Parameters: " + str(self.parameters))
        return temp


class PriorityQueue(object):
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
  
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
  
    # for inserting an element in the queue
    def insert(self, key, data):
        heappush(self.queue, ((-1) * key, id(data), data))

    # for popping an element based on Priority
    def pop(self):
        (key, _, data) = heappop(self.queue)
        return (-1) * key, data

    # fr clearing the queue
    def clear(self):
        self.queue.clear()




class synthesizer():

    def __init__(self, actions, actionWrapper, processNum):
        self.actions = actions
        self.worklist = deque()
        self.actionWrapper = actionWrapper
        self.processNum = processNum
        self.lock = multiprocessing.Lock()
        self.CounterExampleLoop = False

        self.isPrune = True

        self.priorityworklist = PriorityQueue() # Sequences of Actions ranked by priorities
        self.mapAnswers = {} # Profitable Attack Vectors

        # Collected during synthesis
        self.concreteAttackVectorsCandidates = [[], [], []] # concreteAttackVectorsCandidates[0] = [action_list1, action_list2]
                                                  # concreteAttackVectorsCandidates[1] = [[paras1, paras2], [paras1, paras2]]
                                                  # concreteAttackVectorsCandidates[2] = [[estimated_profit1, estimated_profit2], [estimated_profit1, estimated_profit2]]
        # Collected when fetching from the priority queue
        self.concreteAttackVectorsStrengths = []  
        self.concreteAttackVectorsLastProfit = []
        self.concreteAttackNumOfPositives = []

        # Collected during counter-example driven approximation refinement
        self.counterExamples = [[], []] # same as concreteAttackVectorsCandidates
        self.start = time.time()

        Partial.setPossibleActions(actions)
                
    def resetWorklist(self):
        self.worklist.clear()
        for action in self.actions:
            newPartial = Partial([action])
            self.worklist.append(newPartial)

    def refreshTransitFormula(self):
        for action in self.actions:
            op = getattr(action, "refreshTransitFormula", None)
            if op == None:
                continue
            op = getattr(action, "hasNewDataPoints", None)
            if op == None:
                continue
            if action.hasNewDataPoints:
                action.refreshTransitFormula()
        gc.collect()

    def clearCache(self):
        self.counterExamples = [[], []]
        self.concreteAttackVectorsCandidates = [[], [], []]
        self.concreteAttackVectorsStrengths = []
        self.concreteAttackVectorsLastProfit = []
        self.concreteAttackNumOfPositives = []

    def synthesis(self, maxLen: int, Pruning: bool, CounterExampleLoop: bool):
        start = time.time() # uint: seconds
        self.start = start
        self.Pruning = Pruning
        self.CounterExampleLoop = CounterExampleLoop 

        self.refreshTransitFormula()
        self.showDataPointsStats()

        global_best_profit = 0
        
        # First round 
        self.resetWorklist()
        self._synthesis(maxLen)
        actual_best_profit = self.checkProfit(0)
        print(" ================================================================================= ")
        print(" =========== Strength 0 - round 0 of concrete attack vector verification finishes ================ ")
        print(" =========== Best Global Profit: " + str(actual_best_profit) + " ================================= ")
        print(" ================================================================================= ")

        # Round 0 should not use Counterexample driven loops
        # if CounterExampleLoop:
        #     self.executeAndAddCounterExamples()
        #     print(" ================================================================================= ")
        #     print(" ================================================================================= ")
        #     print(" =========== Strength 0 - round 0 of counter-example driven loop finishes ================ ")
        #     print(" ================================================================================= ")
        #     print(" ================================================================================= ")
        self.clearCache()
        self.showDataPointsStats()
        if actual_best_profit > global_best_profit:
            global_best_profit = actual_best_profit
        
        # Following rounds
        for ii in range(20):
            gc.collect()
            self._synthesis2()
            actual_best_profit = self.checkProfit(ii + 1)
            print(" ================================================================================= ")
            print(" =========== round ",ii + 1," of concrete attack vector verification finishes ================ ")
            print(" =========== Best Global Profit: " + str(actual_best_profit) + " ================================= ")
            print(" ================================================================================= ")
            if CounterExampleLoop: # and ii != 0:
                self.executeAndAddCounterExamples()
                print(" ================================================================================= ")
                print(" ================================================================================= ")
                print(" =========== round ",ii + 1," of counter-example driven loop finishes ================ ")
                print(" ================================================================================= ")
                print(" ================================================================================= ")
            self.clearCache()
            self.showDataPointsStats()
            if actual_best_profit > global_best_profit:
                global_best_profit = actual_best_profit
            if self.priorityworklist.isEmpty():
                break
        print(" ================================================================================= ")
        print(" ======================= End of Synthesis, time in total:  " + str(time.time() - self.start) +" s ============== ")      
        print(" ================================================================================= ")
        print(" ======================= Now shows the answers: ======================================== ")
        for key, value in self.mapAnswers.items():
            if len(value[1]) == 0:
                continue
            print("For Symbolic Attack Vector: ", key)
            print("Best Profit: ", value[0],  "  Parameters: ", value[1])
        print(" ======================= End of Answers    ===================================== ")
        print(" =================== Best Profit ", global_best_profit, " ============================ ")
        
    def showDataPointsStats(self):
        for action in self.actions:
            print(action.string(), "number of points: ")
            op = getattr(action, "points", None)
            if op == None:
                print(" skip")
                continue
            print(len(action.points))

    def ToString(self,action_list):
        temp = ""
        for ii in range(len(action_list)):
            if ii != len(action_list) - 1:
                temp += action_list[ii].string() + ", "
            else:
                temp += action_list[ii].string()
        return temp

    # Counter-example driven approximation refinement
    def executeAndAddCounterExamples(self):
        # inputs:
        # self.counterExamples[0] = [action_list1, action_list2]
        # self.counterExamples[1] = [[paras1, paras2], [paras1, paras2]]
        # len(self.counterExamples[0]) == len(self.counterExamples[1])
        action_lists = self.counterExamples[0]
        paras = self.counterExamples[1]
        data_map = executeAndGetStats(action_lists, paras, self.actionWrapper)
        # data_map: {'Curve_USDC2USDT, fUSDT_deposit, Curve_USDT2USDC, fUSDT_withdraw': 
        # [
        #   []
        #   [[10554172, 49972546, 10564726, 51543725], [101201658, 57456951, 162518858, 50882231, 57456951, 110975133, 50319426]], 
        #   [[10554172, 49972546, 10564726, 51543726], [101201658, 57456951, 162518858, 50882230, 57456951, 110975132, 50319427]]],
        # ] 
        total = 0
        for ii in range(len(action_lists)):
            action_list = action_lists[ii]
            para_product = paras[ii]
            if len(para_product) == 0:
                continue
            for jj in range( len(action_list )):
                pp = action_list[0 : len(action_list) - jj]

                op = getattr(pp[-1], "collectorStr", None)
                if op is None:
                    continue

                stats = data_map[self.ToString(pp)]
                num = checkAndAddDatapoints(pp, self.actionWrapper, stats)
                total += num
        print(" ================================================================================= ")
        print(" ================ in total ", total ," number of new data points added ===========")
        print(" ================================================================================= ")

        self.refreshTransitFormula()

    def checkProfit(self, roundNum):
        # counterExamples initialized
        self.counterExamples[0] = self.concreteAttackVectorsCandidates[0]
        for ii in range(len(self.concreteAttackVectorsCandidates[0])):
            self.counterExamples[1].append([])
        # end of initialization

        profits = testRealProfit_Batch(self.concreteAttackVectorsCandidates[0], self.concreteAttackVectorsCandidates[1], self.actionWrapper)
        globalBestProfit = 0
        for ii in range(len(self.concreteAttackVectorsCandidates[0])):
            paras = self.concreteAttackVectorsCandidates[1][ii]
            estimated_profits = self.concreteAttackVectorsCandidates[2][ii]
            NumPositives = self.concreteAttackNumOfPositives[ii]  # Count the number of positive estimated profits
            bestProfit = 0.1 * NumPositives
            bestXls = []
            Actions = self.concreteAttackVectorsCandidates[0][ii]
            print("For Symbolic Attack Vector: ", self.ToString(Actions))
            
            for jj in range(len(paras)):
                para = paras[jj]
                print("\t", para)
                estimated_profit = estimated_profits[jj]
                actual_profit = profits[ii][jj]
                print("\tEstimated Profit", estimated_profit, " \t Actual Profit", actual_profit)
                if actual_profit > bestProfit:
                    bestProfit = actual_profit
                    bestXls = para
                
                # counterExamples to be checked
                if actual_profit != None and actual_profit != 0:
                            # the error rate is smaller than 10%(previous 5%)
                    if abs(actual_profit - estimated_profit) > max( 0.05 * (abs(actual_profit) + abs(estimated_profit)), 10):
                        self.counterExamples[1][ii].append(para)
                # end of counterExamples to be checked

            currStrength = self.concreteAttackVectorsStrengths[ii]
            lastProfit = self.concreteAttackVectorsLastProfit[ii]
            print(" ===== Best Profit: ", bestProfit,  " Best Paras: ", bestXls, ",   time: ", time.time() - self.start)
            print(" ===== Strength: ", currStrength, " Last Profit: ", lastProfit, "  ===== ")

            # Insert into Answer priority queues
            if bestProfit >= 1:
                ActionStr = self.ToString(Actions)
                if ActionStr in self.mapAnswers:
                    if bestProfit > self.mapAnswers[ActionStr][0]:
                        self.mapAnswers[ActionStr] = (bestProfit, bestXls)
                else:
                    self.mapAnswers[ActionStr] = (bestProfit, bestXls)


            # For Y_noloop, only run optimizer(strength==2) once
            if (not self.CounterExampleLoop) and (currStrength == 2):
                pass
            else:
                if not self.isPrune:
                    if bestProfit > lastProfit:
                        self.priorityworklist.insert(bestProfit, PartialObject(Actions, currStrength))
                    elif currStrength <= 1:
                        self.priorityworklist.insert(bestProfit, PartialObject(Actions, currStrength + 1))

                elif bestProfit >= 0.2 or lastProfit >= 0.2: # The optimizer returns at least two solutions which yield positive profit
                    # Add "good" symbolic attack vectors to back to priority worklist
                    # Filter out those "bad" ones
                    if bestProfit > lastProfit:
                        self.priorityworklist.insert(bestProfit, PartialObject(Actions, currStrength))
                    elif currStrength <= 1:
                        self.priorityworklist.insert(lastProfit, PartialObject(Actions, currStrength + 1))



            if bestProfit > globalBestProfit:
                globalBestProfit = bestProfit
            print("Now global best profit is, ", globalBestProfit)
        

        total = 0
        for ii in range(len(self.concreteAttackVectorsCandidates[0])):
            total += len(self.concreteAttackVectorsCandidates[1][ii])
        
        print("===== in total ", total, " concrete attack vectors are checked ======")

        num_actual_profit = 0
        for aa in profits:
            for bb in aa:
                if bb != 0 and bb != -1:
                    num_actual_profit += 1
        print("==== in total ", num_actual_profit, " executions succeed")

        print("===== Next round we have ", len(self.priorityworklist.queue), " symbolic attack vectors to check: " )



        # Just leave <maxCandidates> most possible traces
        # if the best profit is much larger
        maxCandidates = 100
        if len(self.priorityworklist.queue) > maxCandidates and self.isPrune:  
            temp = PriorityQueue()
            candidates = 0
            while not self.priorityworklist.isEmpty():
                key, value = self.priorityworklist.pop()
                temp.insert(key, value)
                candidates += 1
                if candidates + 1 > maxCandidates:
                    break
            self.priorityworklist = temp
            print("===== Pruning 1 choose the best ", maxCandidates, "trace candidates")
            print("===== Next round we have ", len(self.priorityworklist.queue), " symbolic attack vectors to check: " )

        # if roundNum >= 7, we need to fast converge, prune traces whose profit is much smaller than the globalBestProfit
        if roundNum >= 7 and globalBestProfit > 1000 and self.isPrune:
            temp = PriorityQueue()
            while not self.priorityworklist.isEmpty():
                key, value = self.priorityworklist.pop()
                if key >= globalBestProfit * 0.001:
                    temp.insert(key, value)
            self.priorityworklist = temp
            print("===== Pruning 2 because the profit is much smaller than globalBestProfit ")
            print("===== Next round we have ", len(self.priorityworklist.queue), " symbolic attack vectors to check: " )


        return globalBestProfit




    def OptimizeMultiTraceSingleProcess(self, c_arr, strength_arr):
        for i in range(len(c_arr)):
            c = c_arr[i]
            strength = strength_arr[i]
            xls, funls, NumPositives = optimizeMiniMumOnce(c.Actions, self.actionWrapper, strength, self.start)
            self.concreteAttackVectorsCandidates[0].append(c.Actions)
            self.concreteAttackVectorsCandidates[1].append(xls)
            self.concreteAttackVectorsCandidates[2].append(funls)
            self.concreteAttackVectorsStrengths.append(0)
            self.concreteAttackVectorsLastProfit.append(0)
            self.concreteAttackNumOfPositives.append(NumPositives)    

    def OptimizeMultiTrace(self, c_arr, strength_arr):
        arr0 = []
        arr1 = []
        arr2 = []
        arr3 = []
        arr4 = []
        arr5 = []
        global list0, list1, list2, list3, list4, list5
        for i in range(len(c_arr)):
            c = c_arr[i]
            strength = strength_arr[i]
            xls, funls, NumPositives = optimizeMiniMumOnce(c.Actions, self.actionWrapper, strength, self.start)
            arr0.append(c.Actions)
            arr1.append(xls)
            arr2.append(funls)
            arr3.append(0)
            arr4.append(0)
            arr5.append(NumPositives)
        lock.acquire()
        list0 += arr0
        list1 += arr1
        list2 += arr2
        list3 += arr3
        list4 += arr4
        list5 += arr5
        lock.release()

    def _synthesis(self, maxLen: int, strength = 0):
        alltraces = []
        allstrengths = []
        while len(self.worklist) != 0:
            currPartial = self.worklist.popleft()
            if currPartial.size() < maxLen:
                expandList = currPartial.expandPartial() 
                for p in expandList:
                    if checkifFeasible2(self.actionWrapper, p.Actions, True): 
                        # print("New Partial:     \t", end="")
                        # print(p.string())
                        self.worklist.append(p)

            expandContract = currPartial.expandContract()
            for c in expandContract:
                if checkifFeasible2(self.actionWrapper, c.Actions, False): 
                    alltraces.append(c)
                    allstrengths.append(strength)


        if len(alltraces) < 50 or not self.Pruning:
            self.isPrune = False

        # Add parallelism for polynomial approx
        if self.processNum <= 1 or len(alltraces) <= self.processNum:
            self.OptimizeMultiTraceSingleProcess(alltraces, allstrengths)
        else:
            all_traces = []
            all_strengths = []
            for i in range(self.processNum):
                all_traces.append([])
                all_strengths.append([])

            for i in range(len(alltraces)):
                for j in range(self.processNum):
                    if i % self.processNum == j:
                        all_traces[j].append(alltraces[i])
                        all_strengths[j].append(allstrengths[i])

            all_processes = []
            for i in range(self.processNum):
                process = multiprocessing.Process(target=self.OptimizeMultiTrace, args=(all_traces[i], \
                    all_strengths[i]))
                process.start()
                all_processes.append(process)
            
            for process in all_processes:
                process.join()

            self.concreteAttackVectorsCandidates[0] = list(list0)
            self.concreteAttackVectorsCandidates[1] = list(list1)
            self.concreteAttackVectorsCandidates[2] = list(list2)
            self.concreteAttackVectorsStrengths = list(list3)
            self.concreteAttackVectorsLastProfit = list(list4)
            self.concreteAttackNumOfPositives = list(list5)
            list0[:], list1[:], list2[:], list3[:], list4[:], list5[:] = [], [], [], [], [], []
            
    def OptimizeMultiTraceSingleProcess2(self, actions_arr, profit_arr, strength_arr):
        for i in range(len(actions_arr)):
            actions = actions_arr[i]
            profit = profit_arr[i]
            strength = strength_arr[i]
            xls, funls, NumPositives = optimizeMiniMumOnce(actions, self.actionWrapper, strength, self.start, profit)
            self.concreteAttackVectorsCandidates[0].append(actions)
            self.concreteAttackVectorsCandidates[1].append(xls)
            self.concreteAttackVectorsCandidates[2].append(funls)
            self.concreteAttackVectorsStrengths.append(strength)
            self.concreteAttackVectorsLastProfit.append(profit)
            self.concreteAttackNumOfPositives.append(NumPositives)    

    def OptimizeMultiTrace2(self, actions_arr, profit_arr, strength_arr):
        arr0 = []
        arr1 = []
        arr2 = []
        arr3 = []
        arr4 = []
        arr5 = []
        global list0, list1, list2, list3, list4, list5
        for i in range(len(actions_arr)):
            actions = actions_arr[i]
            profit = profit_arr[i]
            strength = strength_arr[i]
            xls, funls, NumPositives = optimizeMiniMumOnce(actions, self.actionWrapper, strength, self.start, profit)
            arr0.append(actions)
            arr1.append(xls)
            arr2.append(funls)
            arr3.append(strength)
            arr4.append(profit)
            arr5.append(NumPositives)
        lock.acquire()
        list0 += arr0
        list1 += arr1
        list2 += arr2
        list3 += arr3
        list4 += arr4
        list5 += arr5
        lock.release()


    def _synthesis2(self):
        allTraces = []
        allStrengths = []
        allLastProfits = []
        while not self.priorityworklist.isEmpty():
            profit, pObject = self.priorityworklist.pop()
            allTraces.append(pObject.Actions)
            allStrengths.append(pObject.currentStrength)
            allLastProfits.append(profit)

        if len(allTraces) < 50  or not self.Pruning:
            self.isPrune = False

        # Add parallelism for polynomial approx
        if self.processNum <= 1 or len(allTraces) <= self.processNum:
            self.OptimizeMultiTraceSingleProcess2(allTraces, allLastProfits, allStrengths)
        else:
            all_traces = []
            all_lastProfits = []
            all_strengths = []
            for i in range(self.processNum):
                all_traces.append([])
                all_lastProfits.append([])
                all_strengths.append([])

            for i in range(len(allTraces)):
                for j in range(self.processNum):
                    if i % self.processNum == j:
                        all_traces[j].append(allTraces[i])
                        all_lastProfits[j].append(allLastProfits[i])
                        all_strengths[j].append(allStrengths[i])

            all_processes = []
            for i in range(self.processNum):
                process = multiprocessing.Process(target=self.OptimizeMultiTrace2, args=(all_traces[i], \
                    all_lastProfits[i], all_strengths[i]))
                process.start()
                all_processes.append(process)


            for process in all_processes:
                process.join()

            self.concreteAttackVectorsCandidates[0] = list(list0)
            self.concreteAttackVectorsCandidates[1] = list(list1)
            self.concreteAttackVectorsCandidates[2] = list(list2)
            self.concreteAttackVectorsStrengths = list(list3)
            self.concreteAttackVectorsLastProfit = list(list4)
            self.concreteAttackNumOfPositives = list(list5)
            list0[:], list1[:], list2[:], list3[:], list4[:], list5[:] = [], [], [], [], [], []




def getActionsFromContractName():
    maxSynthesisLen = 0
    actions = []
    actionWrapper = None
    config.ETHorBSCorDVDorFantom = 0

    ExtraActions = True


    if config.benchmarkName == 'Harvest_USDC':
        config.initialEther = 500000
        config.blockNum = 11129500
        config.contract_name = "Harvest_USDC_attack"
        config.ETHorBSCorDVDorFantom = 0
        maxSynthesisLen = 4  # 4
        action1 = Curve_USDC2USDT_Harvest_USDCExtra
        action2 = Curve_USDT2USDC_Harvest_USDCExtra
        action3 = Curve_DAI2USDC_Harvest_USDCExtra
        action4 = Curve_USDC2DAI_Harvest_USDCExtra
        action5 = Curve_DAI2TUSD_Harvest_USDCExtra
        action6 = Curve_TUSD2DAI_Harvest_USDCExtra
        action7 = Curve_DAI2USDT_Harvest_USDCExtra
        action8 = Curve_USDT2DAI_Harvest_USDCExtra
        action9 = Curve_USDC2TUSD_Harvest_USDCExtra
        action10 = Curve_TUSD2USDC_Harvest_USDCExtra
        action11 = Curve_USDT2TUSD_Harvest_USDCExtra
        action12 = Curve_TUSD2USDT_Harvest_USDCExtra
        action13 = fUSDT_depositExtra
        action14 = fUSDT_withdrawExtra
        action15 = fUSDT_depositForExtra

        actions = [action1, action2, action3, action4, action5, action6, action7, action8, \
                     action9, action10, action11, action12, action13, action14, action15]
        
        actionWrapper = Harvest_USDCActionExtra
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/eth/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 11129499"
        groundtruthSeq = [Curve_USDC2USDT_Harvest_USDCExtra, fUSDT_depositExtra, Curve_USDT2USDC_Harvest_USDCExtra, fUSDT_withdrawExtra]

    elif config.benchmarkName == 'Harvest_USDT':
        config.initialEther = 200000
        config.blockNum = 11129474
        config.contract_name = "Harvest_USDT_attack"
        config.ETHorBSCorDVDorFantom = 0
        maxSynthesisLen = 4  # 4
        action1 = Curve_USDT2USDC_Harvest_USDTExtra
        action2 = Curve_USDC2USDT_Harvest_USDTExtra
        action3 = Curve_DAI2USDC_Harvest_USDTExtra
        action4 = Curve_USDC2DAI_Harvest_USDTExtra
        action5 = Curve_DAI2TUSD_Harvest_USDTExtra
        action6 = Curve_TUSD2DAI_Harvest_USDTExtra
        action7 = Curve_DAI2USDT_Harvest_USDTExtra
        action8 = Curve_USDT2DAI_Harvest_USDTExtra
        action9 = Curve_USDC2TUSD_Harvest_USDTExtra
        action10 = Curve_TUSD2USDC_Harvest_USDTExtra
        action11 = Curve_USDT2TUSD_Harvest_USDTExtra
        action12 = Curve_TUSD2USDT_Harvest_USDTExtra
        action13 = fUSDC_depositExtra
        action14 = fUSDC_withdrawExtra
        action15 = fUSDC_depositForExtra

        actions = [action1, action2, action3, action4, action5, action6, action7, action8, \
                     action9, action10, action11, action12, action13, action14, action15]
        actionWrapper = Harvest_USDTActionExtra
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/eth/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 11129473"    
        groundtruthSeq = [Curve_USDT2USDC_Harvest_USDTExtra, fUSDC_depositExtra, Curve_USDC2USDT_Harvest_USDTExtra, fUSDC_withdrawExtra]
    
    # elif config.benchmarkName == 'InverseFi':
    #     config.ETHorBSCorDVDorFantom = 0
    #     config.initialEther = 0
    #     config.blockNum = 14972419
    #     config.contract_name = "InverseFi_attack"
    #     maxSynthesisLen = 6  # 6
    #     action1 = AddLiquidityUSDTWBTCWETHPool
    #     action2 = DeposityvCurve3Crypto
    #     action3 = MintanYvcrvCrypto
    #     action4 = ExchangeWBTC2USDT
    #     action5 = BorrowInverseFinance
    #     action6 = ExchangeUSDT2WBTC
    #     actions = [action1, action2, action3, action4, action5, action6]
    #     actionWrapper = InverseFiAction
    #     groundtruthSeq = actions

    elif config.benchmarkName == 'Wdoge':
        config.ETHorBSCorDVDorFantom = 1
        config.initialEther = 3000
        config.blockNum = 17248706
        config.contract_name = "Wdoge_attack"
        maxSynthesisLen = 5  # 5
        action1 = SwapWBNB2WdogeExtra
        action2 = TransferWdogeExtra
        action3 = TransferWBNB_WdogeExtra
        action4 = MintUniswap_WdogeExtra
        action5 = PancakePairSkimExtra
        action6 = PancakePairSync2Extra
        action7 = SwapWdoge2WBNBExtra

        actions = [action1, action2, action3, action4, \
                   action5, action6, action7]
        actionWrapper = WdogeActionExtra
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/bsc/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 17248705"
        groundtruthSeq = actions

    elif config.benchmarkName == 'ApeRocket':
        config.initialEther = 0
        config.ETHorBSCorDVDorFantom = 1
        config.blockNum = 9139708
        config.contract_name = "ApeRocket_attack"
        maxSynthesisLen = 6  # 6
        action1 = DepositAutoCakeExtra # 
        action2 = TransferCAKEExtra
        action3 = HarvestAutoCakeExtra 
        action4 = GetRewardAutoCakeExtra # 
        action5 = WithdrawAllAutoCakeExtra #
        action6 = SwapSpace2WBNBExtra
        action7 = SwapWBNB2SpaceExtra
        action8 = TransferWBNBApeExtra
        action9 = TransferSPACEExtra
        action10 = WithdrawUnderlyingAutoCakeExtra #
        action11 = DepositAllAutoCakeExtra #
        actions = [action1, action2, action3, action4, action5, action6, \
                   action7, action8, action9, action10, action11]
        actionWrapper = ApeRocketActionExtra
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/bsc/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 9139707"
        groundtruthSeq = None


    # elif config.benchmarkName == "AutoShark":
    #     maxSynthesisLen = 8 # 8
    #     config.ETHorBSCorDVDorFantom = 1
    #     config.initialEther = 100001
    #     config.blockNum = 7698696
    #     config.contract_name = "AutoShark_attack"

    #     action1 = SwapPancakeWBNB2LP
    #     action2 = DepositStrategy
    #     action3 = TransferLPStrategy
    #     action4 = SwapPancakeWBNB2SHARK
    #     action5 = TransferWBNBStrategy
    #     action6 = TransferSHARKStrategy
    #     action7 = GetRewardStrategy
    #     action8 = SwapPancakeSHARK2WBNB
    #     actions = [action1, action2, action3, action4, action5, action6, action7, action8]
    #     actionWrapper = AutoSharkAction
    #     groundtruthSeq = actions



    elif config.benchmarkName == 'Novo':
        config.initialEther = 20
        config.ETHorBSCorDVDorFantom = 1
        config.blockNum = 18225002
        config.contract_name = "Novo_attack"
        maxSynthesisLen = 4  # 4
        action1 = SwapFeeWBNB2NOVOExtra
        action2 = TransferFromExtra
        action3 = PancakePairSyncExtra
        action4 = SwapFeeNovo2WBNBExtra
        action5 = TransferNovoExtra
        action6 = TransferWBNBExtra
        actions = [action1, action2, action3, action4, action5, action6]
        actionWrapper = NovoActionExtra
        groundtruthSeq = actions
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/bsc/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 18225001"



    elif config.benchmarkName == 'OneRing':
        config.initialEther = None
        config.ETHorBSCorDVDorFantom = 3
        config.blockNum = 34041498
        config.contract_name = "OneRing_attack"
        maxSynthesisLen = 2  # 2
        action1 = DepositSafeOShareUSDCExtra
        action2 = DepositSafeOSharefUSDTExtra
        action3 = DepositOShareUSDCExtra
        action4 = DepositOSharefUSDTExtra
        action5 = WithdrawOShareUSDCExtra
        action6 = WithdrawOSharefUSDTExtra
        action7 = WithdrawSafeOShareUSDCExtra
        action8 = WithdrawSafeOSharefUSDTExtra

        actions = [action1, action2, action3, action4, \
                   action5, action6, action7, action8]
        actionWrapper = OneRingActionExtra
        groundtruthSeq = actions
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/fantom/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 34041497"


    # elif config.benchmarkName == 'Yearn':
    #     config.initialEther = 217000
    #     config.blockNum = 11792260
    #     config.contract_name = "Yearn_attack"
    #     maxSynthesisLen = 7  # 7
    #     action1 = AddLiquidityDAIUSDC
    #     action2 = RemoveImbalance
    #     action3 = DeposityDAI
    #     action4 = EarnyDAI
    #     action5 = AddLiquidityUSDT
    #     action6 = WithdrawyDAI
    #     action7 = RemoveImbalanceDAIUSDC
    #     actions = [action1, action2, action3,
    #                action4, action5, action6, action7]
    #     actionWrapper = YearnAction
    #     groundtruthSeq = actions


    elif config.benchmarkName == 'ValueDeFi':
        config.initialEther = 1000000
        config.blockNum = 11256673
        config.contract_name = "valueDeFi_attack"
        maxSynthesisLen = 6  # 6
        action1 = VaultBankDeposit
        action2 = Curve_DAI2USDC_ValueDeFi
        action3 = Curve_USDT2USDC_ValueDeFi
        action4 = ValueWithdrawFor
        action5 = Curve_USDC2USDT_ValueDeFi
        action6 = Curve_USDC2DAI_ValueDeFi
        actions = [action1, action2, action3, action4, action5, action6]
        actionWrapper = ValueDeFiAction
        groundtruthSeq = actions

        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/eth/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 11256672"


    # elif config.benchmarkName == 'CheeseBank':
    #     config.initialEther = 21000
    #     config.blockNum = 11205647
    #     config.contract_name = "cheeseBank_attack"
    #     maxSynthesisLen = 8  # 8
    #     action1 = SwapUniswapETH2LP
    #     action2 = SwapUniswapETH2Cheese
    #     action3 = RefreshCheeseBank
    #     action4 = LP2LQ
    #     action5 = BorrowCheese_USDC
    #     action6 = BorrowCheese_USDT
    #     action7 = BorrowCheese_DAI
    #     action8 = SwapUniswapCheese2ETH

    #     actions = [action1, action2, action3, action4, \
    #                action5, action6, action7, action8]
    #     actionWrapper = CheeseBankAction
    #     groundtruthSeq = actions

    # elif config.benchmarkName == 'Puppet':
    #     config.ETHorBSCorDVDorFantom = 2
    #     maxSynthesisLen = 2  # 2
    #     action1 = SwapUniswapDVT2ETH
    #     action2 = PoolBorrow
    #     actions = [action1, action2]
    #     actionWrapper = puppetAction
    #     groundtruthSeq = [action1, action2]
    #     if ExtraActions:
    #         action3 = SwapUniswapETH2DVT
    #         actions = [action1, action2, action3]

    # elif config.benchmarkName == 'PuppetV2':
    #     config.ETHorBSCorDVDorFantom = 2
    #     maxSynthesisLen = 3  # 3
    #     action1 = SwapUniswapDVT2ETH_V2
    #     action2 = WrapETH
    #     action3 = PoolBorrow_V2
    #     actions = [action1, action2, action3]
    #     actionWrapper = puppetV2Action
    #     groundtruthSeq = [action1, action2, action3]

    #     if ExtraActions:
    #         action4 = SwapUniswapETH2DVT_V2
    #         actions = [action1, action2, action3, action4]



    elif config.benchmarkName == 'bZx1':
        config.initialEther = 12500
        config.blockNum = 9484680
        config.contract_name = "bZx1_attack"
        config.ETHorBSCorDVDorFantom = 0
        maxSynthesisLen = 2  # 2
        action1 = SwapUniswapWBTC2ETH
        action2 = MarginShort
        actions = [action1, action2]
        actionWrapper = bZx1Action
        groundtruthSeq = [action2, action1]
    
        if ExtraActions:
            action3 = SwapUniswapETH2WBTC
            actions = [action1, action2, action3]
        
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/eth/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 9484680"


    elif config.benchmarkName == 'bEarnFi':
        config.initialEther = 14000
        config.blockNum = 7457125
        config.contract_name = "bEarnFi_attack"
        config.ETHorBSCorDVDorFantom = 1
        maxSynthesisLen = 4  # 2n
        action1 = Deposit
        action2 = EmergencyWithdraw
        actions = [action1, action2]
        actionWrapper = bEarnFiAction
        groundtruthSeq = [action1, action2, action1, action2]

        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/bsc/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 7457125"


    # elif config.benchmarkName == 'ElevenFi':
    #     config.initialEther = 500
    #     config.blockNum = 8534790
    #     config.contract_name = "ElevenFi_attack"
    #     config.ETHorBSCorDVDorFantom = 1
    #     maxSynthesisLen = 5  # 5
    #     action1 = AddLiquidity
    #     action2 = ElevenFi_Deposit
    #     action3 = EmergencyBurn
    #     action4 = Withdraw
    #     action5 = RemoveLiquidity
    #     actions = [action1, action2, action3, action4, action5]
    #     actionWrapper = ElevenFiAction

    #     groundtruthSeq = actions




    elif config.benchmarkName == 'Eminence':
        config.initialEther = 140000
        config.blockNum = 10954411
        config.contract_name = "Eminence_attack"
        config.ETHorBSCorDVDorFantom = 0
        maxSynthesisLen = 5  # 5
        action1 = EminenceBuy
        action2 = EminenceSell
        action3 = eAAVEBuy
        action4 = eAAVESell
        actions = [action1, action2, action3, action4]
        actionWrapper = EminenceAction

        groundtruthSeq = [EminenceBuy, eAAVEBuy, EminenceSell, eAAVESell, EminenceSell]
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/eth/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 10954410"


    elif config.benchmarkName == 'Warp':
        config.initialEther = 518000
        config.blockNum = 11473330
        maxSynthesisLen = 7  # 6

        config.contract_name = "Warp_attack"
        config.ETHorBSCorDVDorFantom = 0
        action1 = MintLPUniswapV2Extra
        action2 = SwapUniswapWETH2DAIExtra
        action3 = SwapUniswapDAI2WETHExtra
        action4 = LP2BorrowLimitExtra
        action5 = BorrowLimit2LPExtra
        action6 = BorrowSC_USDCExtra
        action7 = BorrowSC_DAIExtra
        action8 = BorrowSC_USDTExtra

        actions = [action1, action2, action3, action4, action5, action6, action7, action8]
        actionWrapper = WarpActionExtra
        config.command = "forge test --match-contract attackTester --fork-url https://rpc.ankr.com/eth/d81f3fbb1f894af172b06e04687b43b7d94d335c2331656722ede40d9888a46e --fork-block-number 11473329"

        groundtruthSeq = [MintLPUniswapV2Extra, SwapUniswapWETH2DAIExtra, LP2BorrowLimitExtra, \
           BorrowSC_USDCExtra, BorrowSC_DAIExtra, SwapUniswapDAI2WETHExtra]

    return groundtruthSeq, actions, actionWrapper, maxSynthesisLen






def getLenWorklistAfterPruning(ExtraActions: bool = False):

    groundtruthSeq, actions, actionWrapper, maxLen = getActionsFromContractName(ExtraActions)

    worklist = deque()
    used_worklist = deque()

    Partial.setPossibleActions(actions)

    for action in actions:
        newPartial = Partial([action])
        worklist.append(newPartial)

    while len(worklist) != 0:
        currPartial = worklist.popleft()
        if currPartial.size() < maxLen:
            expandList = currPartial.expandPartial() 

            for p in expandList:
                if checkifFeasible2(actionWrapper, p.Actions, True): 
                    # print("New Partial:     \t", end="")
                    # print(p.string())
                    worklist.append(p)

        expandContract = currPartial.expandContract()
        for c in expandContract:
            if checkifFeasible2(actionWrapper, c.Actions, False): 
                # print("Check Contract: \t", end="")
                # print(c.string())
                used_worklist.append(c)
    numTypes = len(actions)

    isGrounTruthIn = False
    for c in used_worklist:
        if c.Actions == groundtruthSeq:
            isGrounTruthIn = True
            break

    return isGrounTruthIn, numTypes, maxLen, used_worklist




                
if __name__ == '__main__':
    # we need to test the length of worklist 
    # test checkifFeasible

    ExtraActions = True
    print(" ============================================ ")
    print(" Do we count extra actions for ApeRocket, bZx1, puppet, puppetV2? ", ExtraActions)
    print(" ============================================ ")

    benchmarkList = ['bZx1', 'Harvest_USDC','Harvest_USDT', 'Warp', \
        'ValueDeFi', 'Yearn', 'Eminence', 'CheeseBank', 'InverseFi', \
        'ElevenFi',  'bEarnFi', 'ApeRocket', 'AutoShark',  'Novo', 'Wdoge',  'OneRing',  \
        'puppet', 'puppetV2',   \
        ]
    count = 0
    for benchmark in benchmarkList:
        config.benchmarkName = benchmark
        isGrounTruthIn, numTypes, maxl, used_worklist = getLenWorklistAfterPruning(ExtraActions)
        print(benchmark, "\tgroundtruth in? ", isGrounTruthIn)
        if isGrounTruthIn:
            count += 1
        l = len(used_worklist)
        print("Attack Vector MaxLen: ", maxl, "    \t # Action Types: ", numTypes)
        print("Total # symbolic attack vectors: ", l)
        print("")
        # print("Estimated synthesis time: ", l * 1, " seconds ",  int(l * 1 / 3600), " hours")
        # for used in used_worklist:
        #     print(used.string())
    print("Groundtruth symbolic attack vector in ", count, "out of", len(benchmarkList), "benchmarks")
