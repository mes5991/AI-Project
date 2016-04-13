import numpy as np
import random
#from robot import Robot

class Environment():
    def __init__(self, envSize, desiredWallPercentage, robotCount, env = None):

        # envSize = tuple (n, m)
        # robotCount = number of robots

        self.robots = []
        self.robotsLocation = []
        if env == None:
            self.envMatrix = self.generateEnv(envSize, desiredWallPercentage, robotCount)
        else:
            self.envMatrix = env

    def updateEnvMatrix(self, robotIndex, direction):
        oldLoc = self.robotsLocation[robotIndex]
        newLoc = [oldLoc[0] + direction[0], oldLoc[1] + direction[1]]
        self.envMatrix[oldLoc[0], oldLoc[1]] = 0
        self.envMatrix[newLoc[0], newLoc[1]] = 2
        self.robotsLocation[robotIndex] = newLoc

    def generateEnv(self, envSize, desiredWallPercentage, robotCount):

        # 0 = empty space
        # 1 = wall or object
        # 2 = robot

        #create matirx of empty space
        envMatrix = np.zeros(envSize)
        colLength = envSize[0]
        rowLength = envSize[1]
        rowInd = np.arange(rowLength)
        colInd = np.arange(colLength)

        #add borders
        envMatrix[0] = 1
        envMatrix[colLength - 1] = 1
        for i in range(1, colLength - 1):
            envMatrix[i, 0] = 1
            envMatrix[i, rowLength - 1] = 1

        #add random walls
        wallCount = 0
        for i in range(0, colLength):
            for j in range(0, rowLength):
                if envMatrix[i, j] == 1:
                    wallCount += 1
        desiredWallNum = desiredWallPercentage * (envSize[0] * envSize[1])
        print("Desired Wall Number: ", desiredWallNum)
        print("Wall Count: ", wallCount)

        if wallCount < desiredWallNum:
           for x in range(0, int(desiredWallNum - wallCount)):
               i = random.choice(colInd)
               j = random.choice(rowInd)
               while envMatrix[i,j] != 0:
                   i = random.choice(colInd)
                   j = random.choice(rowInd)
               envMatrix[i, j] = 1
        else:
            envSize = envMatrix.shape
            colLength = envSize[0]
            rowLength = envSize[1]
            rowInd = np.arange(rowLength)
            colInd = np.arange(colLength)

        # #add robots
        # for robot in range(0, robotCount):
        #    i = random.choice(colInd)
        #    j = random.choice(rowInd)
        #    while envMatrix[i,j] != 0:
        #        i = random.choice(colInd)
        #        j = random.choice(rowInd)
        #    # Add robot to environment matrix
        #    envMatrix[i][j] = 2
        #    envMatrix[8][7] = 2
        #     #Store robot world location
        #    self.robotsLocation.append([i, j])
        #    self.robotsLocation.append([8, 7])
        # #Initialize robot object and append object to robots list
        #    self.robots.append(Robot())
        # return envMatrix