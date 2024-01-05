import sys
import os
import time
import config
import subprocess
import json
import re
from web3 import Web3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append(os.path.dirname(os.path.dirname(SCRIPT_DIR)))




dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(dir_path)



class Action():
    def __init__(self, funcName):
        self.funcName = funcName
        self.relatedAddresses = []
        self.readMap = {}
        self.writeMap = {}

    def accessesString(self):
        returnStr = ""
        # remove duplicates
        self.relatedAddresses = list(set(self.relatedAddresses))
        for address in self.relatedAddresses:
            returnStr += "        vm.accesses(address({}));\n".format(address)
        return returnStr
    
    def addReadAccess(self, address, storage):
        if address not in self.readMap:
            self.readMap[address] = []
        self.readMap[address].append(storage)

    def addWriteAccess(self, address, storage):
        if address not in self.writeMap:
            self.writeMap[address] = []
        self.writeMap[address].append(storage)
    


def hasAddress(string, addresses):
    for address in addresses:
        if address in string:
            return address
    return None


# def parseExecutionTrace(trace, address, functionName)::


def executeAndParseRelevantAddresses(command: str):
    # execute command under src/foundryModule
    # parse the output
    # get a list of relevant addresses
    outputActions = []

    output = subprocess.run(command, capture_output=True,
                            shell=True, cwd=project_path + "/src/foundryModule/")
    
    message = str(output.stdout)
    separator = ": =================== Separator =================="
    messages = message.split(separator)

    # only needd messages[1], messages[3], messages[5], messages[7], ...
    messages = messages[1::2]
    # print(len(messages))
    for message in messages:
        # print(message)
        # print("\n=====================================================\n")
        start = "x1b[0m::\\x1b[32m"
        end = "\\x1b[0m("

        startPos = message.find(start)

        endPos = message[startPos:].find(end) + startPos

        # find funcName between first start and first end
        funcName = message[startPos + len(start) :  endPos]

        thisAction = Action(funcName)
        print("funcName: ", funcName)

        # print(funcName)
        # find related addresses
        # find all locations of "] \x1b[32m0x"
        
        # print(message)
        start = "x1b\[32m0x"
        res = [i.start() for i in re.finditer(start, message)]

        for r in res:
            address = message[r + len(start) - 3: r + len(start) + 39]
            # print(address)
            thisAction.relatedAddresses.append(address)
        outputActions.append(thisAction)
        # print("\n ========================= \n")
        # 0xEb91861f8A4e1C12333F42DCE8fB0Ecdc28dA716
    return outputActions



def modifyAttackTestFile(ActionLists):
    # read content and intert new lines

    newlines = []
    lines = None
    with open(project_path + "/src/foundryModule/src/test/attack.t.sol", "r") as f:
        lines = f.readlines()

    ActionListIndex = 0

    counter = 0
    for line in lines:

        if line == None:
            continue
        
        if "=================== Separator ==================" in line and "//" not in line:
            counter += 1
            if counter % 2 == 1:
                newlines.append(line)
                newlines.append("        vm.record();\n")
            else:
                newlines.append(ActionLists[ActionListIndex].accessesString())
                newlines.append(line)
                ActionListIndex += 1
        else:
            newlines.append(line)
    
    with open(project_path + "/src/foundryModule/src/test/attack.t.sol", "w") as f:
        f.writelines(newlines)



def getStorage(string: str) -> list:
    # separator is , or ] or [ or space or \n
    # return a list of storage
    # string is like " [0x0000000000000000000000000000000000000000000000000000000000000000, 0x1c125f7eba8fbca5a7c3b009aee58c491bd0dbfad8a4957e31c7af6a8621c71c]"
    # return 0x0000000000000000000000000000000000000000000000000000000000000000, 0x1c125f7eba8fbca5a7c3b009aee58c491bd0dbfad8a4957e31c7af6a8621c71c

    storages = []
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.replace(" ", "")
    string = string.replace("\n", "")
    string = string.replace(",", "")
    string = string.replace(".", "")

    separator = "0x"
    res = [i.start() for i in re.finditer(separator, string)]
    for r in res:
        storage = string[r: r + 66]
        storages.append(storage)

    # check if storages are valid
    # except for first two digits, other digits should be 0-9 or a-f
    for storage in storages:
        for ii in range(2, len(storage)):
            if not storage[ii].isalnum():
                sys.exit("dependencyCheck Error: storage {} is not valid".format(storage[ii] ))
    return storages



def collectAccessInfo(command, ActionLists):
    output = subprocess.run(command, capture_output=True,
                            shell=True, cwd=project_path + "/src/foundryModule/")
    
    message = str(output.stdout)
    separator = ": =================== Separator =================="
    messages = message.split(separator)

    # only needd messages[1], messages[3], messages[5], messages[7], ...
    messages = messages[1::2]
    # print(len(messages))

    assert len(messages) == len(ActionLists)

    ActionListsIndex = 0

    for ii in range(len(messages)):

        message = messages[ii]
        # print(message)
        lines = message.split("\\n")
        for ii in range(len(lines)):
            line = lines[ii]
            if "34maccesses" in line:
                address = hasAddress(line, ActionLists[ActionListsIndex].relatedAddresses)
                if address == None:
                    sys.exit("dependencyCheck Error: address not found")
                line = lines[ii + 1]
                if "[], []" in line:
                    ActionLists[ActionListsIndex].addReadAccess(address, [])
                    ActionLists[ActionListsIndex].addWriteAccess(address, [])
                    continue
                # line is a string like "[addressA, addressB, addressC], [addressD, addressE, addressF]"
                # return [addressA, addressB, addressC], [addressD, addressE, addressF]

                readList = line[line.find("0m[0x") + 3: line.find("], ")]
                writeList = line[line.find(", [0x", line.find("], ")) + 1: ]

                readstorages = getStorage(readList)
                ActionLists[ActionListsIndex].addReadAccess(address, readstorages)
                # print(readstorages)

                writestorages = getStorage(writeList)
                ActionLists[ActionListsIndex].addWriteAccess(address, writestorages)
                # print(writestorages)
                
                ## check if writestorages is a subset of readstorages
                for storage in writestorages:
                    if storage not in readstorages:
                        sys.exit("dependencyCheck Error: write storage {} is not in read storage".format(storage))
                
                
                ii += 1
                
        ActionListsIndex += 1

    return ActionLists


def findReadWriteDependency(ActionList, verbose = True):
    Dependencies = []
    for ii in range(0, len(ActionList)):
        Dependencies.append([])
        for jj in range(0, len(ActionList)):
            if ii == jj:
                continue
            keyAddresses = []
            for address in ActionList[ii].relatedAddresses:
                if address in ActionList[jj].relatedAddresses:
                    for storage in ActionList[ii].readMap[address]:
                        if storage in ActionList[jj].writeMap[address]:
                            keyAddresses.append(address)
                            break
            if len(keyAddresses) != 0:
                Dependencies[ii].append( (ActionList[jj], keyAddresses ) )
    
    for ii in range(len(Dependencies)):
        if len(Dependencies[ii]) == 0:
            print("Action {} has no dependency".format( ActionList[ii].funcName ))
        else:
            print("Action {} has {} relevant actions: ".format( ActionList[ii].funcName, len(Dependencies[ii])), end="")
            for jj in range(len(Dependencies[ii])):
                print(Dependencies[ii][jj][0].funcName, end=" ")
            print("")
            

        # if verbose:
        #     print("Action {} depends on Action {}".format(ii, Dependencies[ii][0].actionID))
        #     print("key addresses: {}".format(Dependencies[ii][1]))
        #     print("")
            





if __name__ == "__main__":

    command = "./run.sh Novo -vvv"
    outputActions = executeAndParseRelevantAddresses(command)

    modifyAttackTestFile(outputActions)

    ActionList = collectAccessInfo(command, outputActions)

    findReadWriteDependency(ActionList)


