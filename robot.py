import random
import numpy as np

class Robot():

    def __init__(self):
        #Map information:
        #0 = empty space
        #1 = wall or object
        #2 = robot current location
        #3 = unknown value
        self.localMap = np.array([[2]])
        self.location = [0,0]

    def updateMap(self, worldLocation, envMatrix):
        worldNeighbors = self.getWorldNeighbors(worldLocation)
        northNeighbor = worldNeighbors[0]
        eastNeighbor = worldNeighbors[1]
        southNeighbor = worldNeighbors[2]
        westNeighbor = worldNeighbors[3]
        locationI = worldLocation[0]
        locationJ = worldLocation[1]
        neighborValues = []
        for neighbor in worldNeighbors:
            neighborI = neighbor[0]
            neighborJ = neighbor[1]
            neighborValue = envMatrix[neighborI][neighborJ]
            if neighborValue == 2:
                neighborValue = 0
            neighborValues.append(neighborValue)
        self.updateNorth(northNeighbor, neighborValues[0])
        self.updateEast(neighborValues[1])
        self.updateSouth(neighborValues[2])
        self.updateWest(neighborValues[3])

    def updateNorth(self, northNeighbor, neighborValue):
        if self.location[0] == 0: #if local location is at top of matrix
            self.localMap = np.insert(self.localMap, 0, 3, axis = 0) #add a row in above location
            self.location[0] += 1 #Bump location down the matrix by 1
        self.localMap[self.location[0] - 1][self.location[1]] = neighborValue

    def updateEast(self, neighborValue):
        if self.location[1] == self.localMap.shape[1] - 1:
            self.localMap = np.insert(self.localMap, self.location[1] + 1, 3, axis = 1)
        self.localMap[self.location[0]][self.location[1] + 1] = neighborValue

    def updateSouth(self, neighborValue):
        if self.location[0] == self.localMap.shape[0] - 1:
            self.localMap = np.insert(self.localMap, self.location[0] + 1, 3, axis = 0)
        self.localMap[self.location[0] + 1][self.location[1]] = neighborValue

    def updateWest(self, neighborValue):
        if self.location[1] == 0:
            self.localMap = np.insert(self.localMap, 0, 3, axis = 1)
            self.location[1] += 1
        self.localMap[self.location[0]][self.location[1] - 1] = neighborValue

    def getNeighbors(self):
        neighbors = [[self.location[0] - 1, self.location[1]],
                     [self.location[0], self.location[1] + 1],
                     [self.location[0] + 1, self.location[1]],
                     [self.location[0], self.location[1] - 1]]
        return neighbors

    def getWorldNeighbors(self, worldLocation):
        worldNeighbors = [[worldLocation[0] - 1, worldLocation[1]],
                          [worldLocation[0], worldLocation[1] + 1],
                          [worldLocation[0] + 1, worldLocation[1]],
                          [worldLocation[0], worldLocation[1] - 1]]
        return worldNeighbors

    def move(self, newLocation):
        self.localMap[self.location[0]][self.location[1]] = 0
        self.location = newLocation
        self.localMap[self.location[0]][self.location[1]] = 2

    def getLegalMoves(self):
        relativeNeighbors = [[self.location[0] - 1, self.location[1]],
                             [self.location[0], self.location[1] + 1],
                             [self.location[0] + 1, self.location[1]],
                             [self.location[0], self.location[1] - 1]]
        legalMoves = []
        for neighbor in relativeNeighbors:
            if self.localMap[neighbor[0]][neighbor[1]] == 0:
                legalMoves.append(neighbor)
        return legalMoves

    def goalCheck(self):
        unknowns = 3 in self.localMap[1:(self.localMap.shape[0] - 1), 1:(self.localMap.shape[1] - 1)]
        if unknowns:
            return False
        topRowCheck = (0 in self.localMap[0, 1:self.localMap.shape[1] - 1]) or (3 in self.localMap[0, 1:self.localMap.shape[1] - 1])
        if topRowCheck:
            return False
        bottomRowCheck = (0 in self.localMap[self.localMap.shape[0] - 1, 1:self.localMap.shape[1] - 1]) or (3 in self.localMap[self.localMap.shape[0] - 1, 1:self.localMap.shape[1] - 1])
        if bottomRowCheck:
            return False
        leftColCheck = (0 in self.localMap[1:self.localMap.shape[0] - 1, 0]) or (3 in self.localMap[1:self.localMap.shape[0] - 1, 0])
        if leftColCheck:
            return False
        rightRowCheck = (0 in self.localMap[1:self.localMap.shape[0] - 1, self.localMap.shape[1] - 1]) or (3 in self.localMap[1:self.localMap.shape[0] - 1, self.localMap.shape[1] - 1])
        if rightRowCheck:
            return False
        return True
