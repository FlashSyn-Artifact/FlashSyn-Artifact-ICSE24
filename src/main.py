import sys
import os
import config
from synthesizer import *

import src.Actions.datapoints200 as dp200
import src.Actions.datapoints500 as dp500
import src.Actions.datapoints1000 as dp1000
import src.Actions.datapoints2000 as dp2000

import cProfile


def main():
    Pruning = True
    ExtraActions = True

    # argv[0]
    config.benchmarkName = 'bZx1'
    # argv[1]
    config.method = 0 # method 0 for nearest interpolation
    # method 1 for polynomial approximation
    
    # argv[2]
    CounterExampleLoop = True
    # argv[3]
    config.dataPointUpperLimit = 2000

    if len(sys.argv) == 5:
        config.benchmarkName = sys.argv[1]
        config.method = int(sys.argv[2])    
        if int(sys.argv[3]) == 1:
            CounterExampleLoop = True
        else:
            CounterExampleLoop = False
        config.dataPointUpperLimit = int(sys.argv[4])
        

    elif len(sys.argv) == 4:
        config.benchmarkName = sys.argv[1]
        config.method = int(sys.argv[2])    
        if int(sys.argv[3]) == 1:
            CounterExampleLoop = True
        else:
            CounterExampleLoop = False

    elif len(sys.argv) == 3:
        config.benchmarkName = sys.argv[1]
        config.method = int(sys.argv[2])
    elif len(sys.argv) == 2:
        config.benchmarkName = sys.argv[1]

    config.processNum = 1
    if config.method == 0:
        config.processNum = 1

    maxSynthesisLen = 0
    actions = []

    _, actions, actionWrapper, maxSynthesisLen = getActionsFromContractName(ExtraActions)
    
    if hasattr(actionWrapper, 'runinitialPass'):
        actionWrapper.runinitialPass()
    
    if config.dataPointUpperLimit == 200:
        dp200.initialPass(actionWrapper)
    elif config.dataPointUpperLimit == 500:
        dp500.initialPass(actionWrapper)
    elif config.dataPointUpperLimit == 1000:
        dp1000.initialPass(actionWrapper)
    elif config.dataPointUpperLimit == 2000:
        dp2000.initialPass(actionWrapper)
    
    Synthesizer = synthesizer(actions, actionWrapper, config.processNum)
    Synthesizer.synthesis(maxSynthesisLen, Pruning, CounterExampleLoop)


if __name__ == '__main__':
    # cProfile.run("main()", sort="cumtime")
    main()
