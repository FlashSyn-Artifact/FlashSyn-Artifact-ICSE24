import os
import sys
import config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Actions.SingleApprox.SingleApprox import single_round_approx, predict
from Actions.Utils import *


class NumericalApproximator():
    def __init__(self, points, values, indexes=None):
        self.interpolator = None
        self.polynomial = None
        self.polynomial_name = None
        self.score = None
        self.is1D = False
        self.method = config.method # matches config.method
        self.method2 = -1 

        newpoints = None
        if indexes is None:
            newpoints = points
        else:
            newpoints = getPointsFromIndexes(points, indexes)
        
        if self.method == 0:
            isND = any(isinstance(el, list) for el in newpoints)
            if not isND: # means it is 1D
                self.is1D = True
                self.interpolator = interp1d(newpoints, values, kind='linear', fill_value='extrapolate')
            else:
                self.interpolator = BarebonesNearestNDInterpolator(newpoints, values, rescale=False)

        elif self.method == 1:
            self.polynomial, self.polynomial_name, self.score = single_round_approx(newpoints, values, rate=0.1)
            # print("polynomial coef_: ", self.polynomial.coef_)
            # print("polynomial intercept_: ", self.polynomial.intercept_)
            # print("polynomial_name: ", self.polynomial_name)

        elif self.method == 2:
            self.polynomial, self.polynomial_name, self.score = single_round_approx(newpoints, values, rate=0.1)
            
            if self.score == 0:
                self.method2 = 1
            else:
                self.method2 = 0
                isND = any(isinstance(el, list) for el in newpoints)
                if not isND: # means it is 1D
                    self.is1D = True
                    self.interpolator = interp1d(newpoints, values, kind='linear', fill_value='extrapolate')
                else:
                    self.interpolator = BarebonesNearestNDInterpolator(newpoints, values, rescale=False)
            


    def __call__(self, inputs):
        if self.method == 0 or self.method2 == 0:
            if self.is1D:
                # return predict(self.polynomial, self.polynomial_name, [inputs])        

                return self.interpolator(inputs)[0]
            else:
                return self.interpolator([inputs])[0]
                    

        elif self.method == 1 or self.method2 == 1:
            return predict(self.polynomial, self.polynomial_name, [inputs])        





def getActualProfit(initial_guess, ActionWrapper, action_list):
    datapoints = singleCollect(action_list, ActionWrapper, [initial_guess])
    profit = ActionWrapper.calcProfit(datapoints[0][1])
    return profit


def getEstimatedProfit(initial_guess, ActionWrapper, action_list):
    for action in action_list:
        action.hasNewDataPoints = True
    return (-1) * f(initial_guess, ActionWrapper, action_list)

def getEstimatedProfit_precise_display(initial_guess, ActionWrapper, action_list, isdisplay = False):
    return (-1) * f_display(initial_guess, ActionWrapper, action_list, isdisplay)


def printIntePolyEstimatedProfit(initial_guess, ActionWrapper, action_list):
    config.method = 0
    for action in action_list:
        if hasattr(action, 'refreshTransitFormula'):
            action.refreshTransitFormula()
    estimate1 =  (-1) * f_display(initial_guess, ActionWrapper, action_list)
    print("estimated profit for interpolation: ", estimate1)
    
    config.method = 1
    for action in action_list:
        if hasattr(action, 'refreshTransitFormula'):
            action.refreshTransitFormula()
    estimate2 =  (-1) * f_display(initial_guess, ActionWrapper, action_list)
    print("estimated profit for polynormial: ", estimate2)
    return estimate1, estimate2

    
def testCounterExampleDrivenApprox(initial_guess, ActionWrapper, action_list):
    estimate1, estimate2 =  printIntePolyEstimatedProfit(initial_guess, ActionWrapper, action_list)
    print("add datapoints based on groundtruth concrete attack vector")
    executeAndAddDataPoints(action_list, ActionWrapper, [initial_guess], False)
    estimate3, estimate4 = printIntePolyEstimatedProfit(initial_guess, ActionWrapper, action_list)
    return estimate1, estimate2, estimate3, estimate4


def testSpeed(initial_guess, ActionWrapper, action_list):
    start = time.time()
    for _ in range(10000):
        ret = f(initial_guess, ActionWrapper, action_list)
    end = time.time() - start
    print("estimated profit: ", (-1) * ret)
    print("run 10000 loops takes ", end, " (s)")


def testOptimize(action_list, ActionWrapper):
    Optimize(action_list, ActionWrapper)
