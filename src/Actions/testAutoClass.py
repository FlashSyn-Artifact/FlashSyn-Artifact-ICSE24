def getBrackets(num):
    action = "["
    for _ in range(num):
        action += "[], "
    action = action[:-2] + "]"
    return action

def getFunction(num):
    action = ''
    for i in range(num):
        action += "    approximator" + str(i) + " = None\n"
    return action

def getValues2(n2, n3):
    # values[5], values[6], values[7], values[8], values[9], values[10], values[11]
    action = ""
    for i in range(n3):
        action += '''values[''' + str(n2 + i) + '''], '''
    action = action[:-2]
    return action

def getValues1(n1, n2):
    action = ""
    for i in range(n2):
        action += '''values[''' + str(i) + '''], '''
    inputStr = ""
    for i in range(n1):
        inputStr = '''inputs[''' + str(-1 - i) + '''], ''' + inputStr
    action += inputStr
    action = action[:-2]
    return action

def getVs(n3):
    action = "        "
    for i in range(n3):
        action += "v" + str(i) + ", "
    action = action[:-2]
    action += " = cls.aliquotValues(values) \n"
    for i in range(n3):
        action += "        cls.values[" + str(i) + "].append(v" + str(i) + ")  # \n"
    return action

def getReFresh(n3):
    action = ""
    for i in range(n3):
        action += "        cls.approximator" + str(i) + " = NumericalApproximator(cls.points, cls.values[" + str(i) + "])"  + "\n"
    return action

def getOutPut(n3):
    action = ""
    for i in range(n3):
        action += "        output" + str(i) + " = None\n"
    return action

def getInputs(n1, n2):
    action = "        inputs = ["
    for i in range(n2):
        action += "cls.globalStates[" + str(i) + "], "
    if n1 == 0:
        action = action[:-2] + "]"
    elif n1 == 1:
        action += " input]"
    elif n1 == 2:
        action += " input1, input2]"
    action += "\n"
    return action


def getEvaluation(n3): 
    action = ""
    for i in range(n3):
        action += "        output" + str(i) + " = cls.approximator" + str(i) + "(inputs)\n"
    return action

def getOutputs(n3):

    # output0, output1, output2, output3, output4, output5, output6
    action = ""
    for i in range(n3):
        action += "output" + str(i) + ", "
    action = action[:-2]
    return action

# action_name: Action name
# name: ActionWrapper name
# n1: Number of inputs
# n2: Number of prestates
# n3: Number of poststates + outputs
def getClass(action_name, name, n1, n2, n3):
    action = '''
class ''' + action_name + '''('''+ name +'''):
    points = []
    values = ''' + getBrackets(n3) + '''

    hasNewDataPoints = True
'''

    action += getFunction(n3)

    action += '''
    # Action Specific Variables
    numInputs = ''' + str(n1) 
    
    action += '''
    # TODO: Add tokens and ranges here
    tokensIn = []
    tokensOut = []
    range = [] 

    # TODO: Add actionStr and CollectorStr
    @classmethod
    def actionStr(cls):
        action = "      // Action: " + cls.__name__ + "\\n"
        action += "\\n"
        return action

    @classmethod
    def collectorStr(cls):
        action = "      // Collect: " + cls.__name__ + "\\n"
        action += "\\n"
        return action

    @classmethod
    def aliquotValues(cls, values):
        # print(values)
        return ''' + getValues2(n2, n3) 
        
    action += '''

    @classmethod
    def add1PointValue(cls, inputs, values):
        # input = inputs[-1]
        if values == None or len(values) != ''' + str(n2 + n3) +''':
            return -1

        point = [''' + getValues1(n1, n2) + ''']
        if point in cls.points:
            return -2

        cls.points.append(point)

''' 
    action += getVs(n3) + '''
        return 1


    @classmethod
    def refreshTransitFormula(cls):
''' 
    action += getReFresh(n3) 
    action +='''
        cls.hasNewDataPoints = False

    @classmethod
''' 

    if n1 == 0:
        action += '''    def simulate(cls):
''' 
    elif n1 == 1:
        action += '''    def simulate(cls, input):
''' 
    elif n1 == 2:
        action += '''    def simulate(cls, input1, input2):
'''

    action +=  getInputs(n1, n2) + getEvaluation(n3)
    
    if n1 == 0:
        action += '''
    @classmethod
    def transit(cls):  # Assume input is a value'''
    else:
        action += '''
    @classmethod
    def transit(cls, '''
        if n1 == 0: 
            action += ""
        elif n1 == 1:
            action += "input"
        elif n1 == 2:
            action += "input1, input2"
        
        action += '''):  # Assume input is a value'''        
    
    action += \
    '''
        if cls.hasNewDataPoints:
            cls.refreshTransitFormula()
        ''' + getOutputs(n3) 

    if n1 == 0:    
        action += ''' = cls.simulate() '''
    elif n1 == 1:
        action += ''' = cls.simulate(input) '''
    elif n1 == 2:
        action += ''' = cls.simulate(input1, input2) '''


    action += '''

        # TODOs: how to use the outputs?
        return

    @classmethod
    def string(cls):
        return cls.__name__
    
    '''
    return action



if __name__ == '__main__':
    print(getClass("ExchangeDOLA2CRV", "InverseFiAction", 1, 2, 3))

# action_name: Action name
# name: ActionWrapper name
# n1: Number of inputs
# n2: Number of prestates
# n3: Number of poststates + outputs
# def getClass(action_name, name, n1, n2, n3):