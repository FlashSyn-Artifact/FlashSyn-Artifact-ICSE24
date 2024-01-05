def f(paras, ActionWrapper, Action_list):
    ActionWrapper.resetBalances()
    para_index = 0
    for Action in Action_list:
        if Action.numInputs == 0:
            Action.transit()
        elif Action.numInputs == 1:
            Action.transit(paras[para_index])
            para_index += 1
        elif Action.numInputs == 2:
            Action.transit(paras[para_index], paras[para_index + 1])
            para_index += 2
    return (-1) * ActionWrapper.calcProfit2()
    
def f_display(paras, ActionWrapper, Action_list, isSim = False):
    ActionWrapper.resetBalances()
    para_index = 0
    for Action in Action_list:
        isSimulate = isSim
        # print("globalStates: ", ActionWrapper.globalStates)
        if not hasattr(Action, 'simulate'):
            isSimulate = False
        if isSimulate:
            print(Action.string())
        if Action.numInputs == 0:
            if isSimulate:
                print(Action.simulate())
            Action.transit()
        elif Action.numInputs == 1:
            if isSimulate:
                print(Action.simulate(paras[para_index]))
            Action.transit(paras[para_index])
            para_index += 1
        elif Action.numInputs == 2:
            if isSimulate:
                print(Action.simulate(paras[para_index], paras[para_index + 1]))
            Action.transit(paras[para_index], paras[para_index + 1])
            para_index += 2
    if isSim:
        print(ActionWrapper.currentBalances)
    return (-1) * ActionWrapper.calcProfit2()


def getF(ActionWrapper, action_list, bnds = None, Scale=1):
    def F(paras):
        if F.bnds is not None:
            paras = (F.bnds[:, 0] + paras * (F.bnds[:, 1] - F.bnds[:, 0])) / Scale  # Rescaled parameters
        ActionWrapper = F.ActionWrapper
        Action_list = F.Action_list
        ActionWrapper.resetBalances()
        para_index = 0
        for Action in Action_list:
            if Action.numInputs == 0:
                Action.transit()
            elif Action.numInputs == 1:
                Action.transit(paras[para_index])
                para_index += 1
            elif Action.numInputs == 2:
                Action.transit(paras[para_index], paras[para_index + 1])
                para_index += 2
        return (-1) * ActionWrapper.calcProfit2()
    F.ActionWrapper = ActionWrapper
    F.Action_list = action_list
    F.bnds = bnds
    return F

def c(paras, ActionWrapper, Action_list):
    ActionWrapper.resetBalances()
    para_index = 0
    for Action in Action_list:
        if Action.numInputs == 0:
            Action.transit()
        elif Action.numInputs == 1:
            Action.transit(paras[para_index])
            para_index += 1
        elif Action.numInputs == 2:
            Action.transit(paras[para_index], paras[para_index + 1])
            para_index += 2
    minBalance = min(ActionWrapper.currentBalances.values())
    minstates = min(ActionWrapper.globalStates)
    return min(minBalance, minstates)

def c_global(paras, ActionWrapper, Action_list, verbose=False):
    ActionWrapper.resetBalances()
    para_index = 0
    minValue = 0
    for Action in Action_list:
        if Action.numInputs == 0:
            Action.transit()
            minValue = min(minValue, min(
                ActionWrapper.currentBalances.values()))
            if verbose:
                print("minValue=", minValue)
        elif Action.numInputs == 1:
            Action.transit(paras[para_index])
            para_index += 1
            minValue = min(minValue, min(
                ActionWrapper.currentBalances.values()))
            if verbose:
                print("minValue=", minValue)
        elif Action.numInputs == 2:
            Action.transit(paras[para_index], paras[para_index + 1])
            para_index += 2
            minValue = min(minValue, min(
                ActionWrapper.currentBalances.values()))
            if verbose:
                print("minValue=", minValue)
        # if minValue < 0:
        #     return minValue
    return minValue

def c_display(paras, ActionWrapper, Action_list):
    ActionWrapper.resetBalances()
    para_index = 0
    for Action in Action_list:
        if Action.numInputs == 0:
            Action.transit()
        elif Action.numInputs == 1:
            Action.transit(paras[para_index])
            para_index += 1
        elif Action.numInputs == 2:
            Action.transit(paras[para_index], paras[para_index + 1])
            para_index += 2
    return ActionWrapper.currentBalances.values()

def getBnds(action_list):
    bnds = []
    for action in action_list:
        if action.numInputs == 1:
            bnds.append((action.range[0] + 1, action.range[1]))
        elif action.numInputs == 2:
            bnds.append((action.range[0] + 1, action.range[1]))
            bnds.append((action.range2[0] + 1, action.range2[1]))
    return bnds


# max length: 10
def getCsts(action_list, ActionWrapper, bnds=None, Scale=1):
    csts = []
    if len(action_list) > 0:
        def c1(paras):
            if c1.bnds is not None:
                paras = (c1.bnds[:, 0] + paras * (c1.bnds[:, 1] - c1.bnds[:, 0])) / Scale
            
            ActionWrapper = c1.ActionWrapper
            Action_list = c1.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c1.ActionWrapper = ActionWrapper
        c1.Action_list = action_list[0:1]
        c1.bnds = bnds

        cst = {"type": "ineq", "fun": c1}
        csts.append(cst)
    else:
        return csts
    
    if len(action_list) > 1:
        def c2(paras):
            if c2.bnds is not None:
                paras = (c2.bnds[:, 0] + paras * (c2.bnds[:, 1] - c2.bnds[:, 0])) / Scale
            
            ActionWrapper = c2.ActionWrapper
            Action_list = c2.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c2.ActionWrapper = ActionWrapper
        c2.Action_list = action_list[0:2]
        c2.bnds = bnds

        cst = {"type": "ineq", "fun": c2}
        csts.append(cst)
    else:
        return csts

    if len(action_list) > 2:
        def c3(paras):
            if c3.bnds is not None:
                paras = (c3.bnds[:, 0] + paras * (c3.bnds[:, 1] - c3.bnds[:, 0])) / Scale 
            ActionWrapper = c3.ActionWrapper
            Action_list = c3.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c3.ActionWrapper = ActionWrapper
        c3.Action_list = action_list[0:3]
        c3.bnds = bnds
        cst = {"type": "ineq", "fun": c3}
        csts.append(cst)
    else:
        return csts


    if len(action_list) > 3:
        def c4(paras):
            if c4.bnds is not None:
                paras = (c4.bnds[:, 0] + paras * (c4.bnds[:, 1] - c4.bnds[:, 0])) / Scale
            ActionWrapper = c4.ActionWrapper
            Action_list = c4.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c4.ActionWrapper = ActionWrapper
        c4.Action_list = action_list[0:4]
        c4.bnds = bnds
        cst = {"type": "ineq", "fun": c4}
        csts.append(cst)
    else:
        return csts


    if len(action_list) > 4:
        def c5(paras):
            if c5.bnds is not None:
                paras = (c5.bnds[:, 0] + paras * (c5.bnds[:, 1] - c5.bnds[:, 0])) / Scale
            ActionWrapper = c5.ActionWrapper
            Action_list = c5.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c5.ActionWrapper = ActionWrapper
        c5.Action_list = action_list[0:5]
        c5.bnds = bnds
        cst = {"type": "ineq", "fun": c5}
        csts.append(cst)
    else:
        return csts

    
    if len(action_list) > 5:
        def c6(paras):
            if c6.bnds is not None:
                paras = (c6.bnds[:, 0] + paras * (c6.bnds[:, 1] - c6.bnds[:, 0])) / Scale
            
            ActionWrapper = c6.ActionWrapper
            Action_list = c6.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c6.ActionWrapper = ActionWrapper
        c6.Action_list = action_list[0:6]
        c6.bnds = bnds
        cst = {"type": "ineq", "fun": c6}
        csts.append(cst)
    else:
        return csts

    
    if len(action_list) > 6:
        def c7(paras):
            if c7.bnds is not None:
                paras = (c7.bnds[:, 0] + paras * (c7.bnds[:, 1] - c7.bnds[:, 0])) / Scale
            
            ActionWrapper = c7.ActionWrapper
            Action_list = c7.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c7.ActionWrapper = ActionWrapper
        c7.Action_list = action_list[0:7]
        c7.bnds = bnds
        cst = {"type": "ineq", "fun": c7}
        csts.append(cst)
    else:
        return csts


    if len(action_list) > 7:
        def c8(paras):
            if c8.bnds is not None:
                paras = (c8.bnds[:, 0] + paras * (c8.bnds[:, 1] - c8.bnds[:, 0])) / Scale
            
            ActionWrapper = c8.ActionWrapper
            Action_list = c8.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c8.ActionWrapper = ActionWrapper
        c8.Action_list = action_list[0:8]
        c8.bnds = bnds
        cst = {"type": "ineq", "fun": c8}
        csts.append(cst)
    else:
        return csts


    if len(action_list) > 8:
        def c9(paras):
            if c9.bnds is not None:
                paras = (c9.bnds[:, 0] + paras * (c9.bnds[:, 1] - c9.bnds[:, 0])) / Scale
            
            ActionWrapper = c9.ActionWrapper
            Action_list = c9.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c9.ActionWrapper = ActionWrapper
        c9.Action_list = action_list[0:9]
        c9.bnds = bnds
        cst = {"type": "ineq", "fun": c9}
        csts.append(cst)
    else:
        return csts


    if len(action_list) > 9:
        def c10(paras):
            if c10.bnds is not None:
                paras = (c10.bnds[:, 0] + paras * (c10.bnds[:, 1] - c10.bnds[:, 0])) / Scale
            
            ActionWrapper = c10.ActionWrapper
            Action_list = c10.Action_list
            ActionWrapper.resetBalances()
            para_index = 0
            for Action in Action_list:
                if Action.numInputs == 0:
                    Action.transit()
                elif Action.numInputs == 1:
                    Action.transit(paras[para_index])
                    para_index += 1
                elif Action.numInputs == 2:
                    Action.transit(paras[para_index], paras[para_index + 1])
                    para_index += 2
            minBalance = min(ActionWrapper.currentBalances.values())
            minstates = min(ActionWrapper.globalStates)
            return min(minBalance, minstates)
        c10.ActionWrapper = ActionWrapper
        c10.Action_list = action_list[0:10]
        c10.bnds = bnds
        cst = {"type": "ineq", "fun": c10}
        csts.append(cst)
    else:
        return csts


    return csts

