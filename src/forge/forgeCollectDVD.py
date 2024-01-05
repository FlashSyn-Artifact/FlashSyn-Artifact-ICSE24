import subprocess
import os
import re
import codecs
import config

dir_path = os.path.dirname(os.path.realpath(__file__))

project_path = os.path.dirname(dir_path)

project_path = os.path.dirname(project_path)


class forgedataCollectContractDVD:
    def __init__(self, ActionWrapper):

        self.ETHorBSCorDVDorFantom = 2  # 0 for ETH  1 for BSC  2 for DVD
        # block num
        self.ActionWrapper = ActionWrapper
        self.startStr = ActionWrapper.start_str  # start code of attack tester

        self.dataPoints = []  # parameters input ==> stats collected
        # list of list of list(size = 2)
        # example: [[[12], []], [[], []]]
        # index represents the data collector number !!!
        self.dataCollectorCount = 0
        self.attackContract = ""

        self.collectorContract = ""

    def addAttackContract(self, contract: str):
        self.attackContract = contract

    def updateAttackContract(self, contract: str):
        self.dataCollectorCount = 0
        self.attackContract = contract

    def addDataCollector(self, paraList):
        temp = '''
    function testExample''' + str(self.dataCollectorCount) + '''_() public {'''
        temp += self.attackContract
        temp += '''
    }   
        '''
        for para in paraList:
            temp = temp.replace('$$', str(para), 1)
        self.collectorContract += temp
        self.dataCollectorCount += 1
        self.dataPoints.append([paraList, None])
        # print(self.dataCollectorCount - 1)
        return self.dataCollectorCount - 1

    def cleanDataCollector(self):
        self.collectorContract = ""
        self.dataCollectorCount = 0

    def updateDataCollectorContract(self):
        if self.ActionWrapper.__name__ == "puppetAction":
            with open(project_path + "/src/foundryModule/src/test/Levels/puppet/attack.t.sol", "w") as solFile:
                solFile.write(self.startStr + self.collectorContract + "\n}")
        else:
            with open(project_path + "/src/foundryModule/src/test/Levels/puppet-v2/attack.t.sol", "w") as solFile:
                solFile.write(self.startStr + self.collectorContract + "\n}")

    def executeCollectData(self):
        # print(self.ActionWrapper.__name__)
        # Make sure and attack.sol and attack.t.sol are empty
        open(project_path + "/src/foundryModule/src/attack.sol", "w").close()
        open(project_path + "/src/foundryModule/src/test/attack.t.sol", "w").close()

        # self.dataCollectorCount = 0
        command = ""
        if self.ActionWrapper.__name__ == "puppetAction":
            command = "forge test --match-contract PuppetV1"
        else:
            command = "forge test --match-contract PuppetV2"

        output = subprocess.run(command, capture_output=True,
                                shell=True, cwd=project_path + "/src/foundryModule/")
        message = str(output.stdout)

        print(command)
        print(message[:150])

        # print("message: ")
        # print(repr(message))

        statsStrStart = message.find("Running")
        statsStrEnd = message.find("Encountered a total of")

        statsStr = message[statsStrStart: statsStrEnd]

        # print(statsStr)
        statsStr = codecs.getdecoder("unicode_escape")(statsStr)[0]

        # filtering out the color settings of the code snippets
        ansi_escape = re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        ''', re.VERBOSE)
        statsStr = ansi_escape.sub('', statsStr)

        # print(statsStr)

        result = re.findall('FAIL. Reason: (.*) \(gas\: ', statsStr)
        # print(result)

        # maxStatsLength does not make sense when multiple sequence of actions are running at the same time
        # maxStatsLength = 0
        # # assume when revert unexpectedly, we get fewer stats than when revert with stats
        # for ret in result:
        #     # print(ret)
        #     stats = [int(s) for s in re.findall(r'[\d]+',  ret)]
        #     # print(stats)
        #     if len(stats) > maxStatsLength:
        #         maxStatsLength = len(stats)
        # if maxStatsLength == 0:
        #     return []

        # print(" = =============")
        # print(self.dataPoints)
        # counter = 0
        for ret in result:
            stats = [int(s) for s in re.findall(r'[\d]+',  ret)]

            if len(stats) > 1:
                # if counter < 5:
                #     print(stats)
                #     counter += 1
                self.dataPoints[stats[-1]][1] = stats[:-1]

            else:
                self.dataPoints[stats[-1]][1] = None

        return self.dataPoints

        # Example: [input parameters], [output parameters]
        # [[[28000299813908753, 3412170442167358], [3917983816717, 6062616627188784794744528, 495189751117167573091345]],
        # [[27000299813908753, 3412170442167358], [3917983816717, 6162616627188784794744528, 495346173235701226433441]],
        # [[0, 0], None],
        # [[0, 3412170442167358], None]]
