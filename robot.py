import random
import numpy as np
import queue as q

class Robot():

    def __init__(self):
        #Map information:
        #0 = empty space
        #1 = wall or object
        #2 = robot current location
        #3 = unknown value
        self.localMap = np.array([[2]])
        self.location = [0,0]
        self.goal = 0
        self.currentPath = []

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

    def getLegalMoves(self, state):
        relativeNeighbors = [[state[0] - 1, state[1]],
                             [state[0], state[1] + 1],
                             [state[0] + 1, state[1]],
                             [state[0], state[1] - 1]]
        legalMoves = []
        for neighbor in relativeNeighbors:
            iCheck = (neighbor[0] >= 0) and (neighbor[0] <= self.localMap.shape[0] - 1)
            jCheck = (neighbor[1] >= 0) and (neighbor[1] <= self.localMap.shape[1] - 1)
            valueCheck = self.localMap[neighbor[0]][neighbor[1]] == 0
            if iCheck and jCheck and valueCheck:
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

    def getClosestUnknown(self):
            state = self.location[:]
            nextState = q.Queue()
            visitedCells = []
            while True:
                neighbors = [[state[0] - 1, state[1]],
                             [state[0], state[1] + 1],
                             [state[0] + 1, state[1]],
                             [state[0], state[1] - 1]]
                for neighbor in neighbors:
                    if (neighbor[0] >= 0) and (neighbor[0] <= (self.localMap.shape[0] - 1)) and (neighbor[1] >= 0) and (neighbor[1] <= (self.localMap.shape[1] - 1)):
                        if self.localMap[neighbor[0]][neighbor[1]] == 3:
                            # if self.unknownLegal(neighbor)
                            return neighbor
                        nextState.put(neighbor)
                state = nextState.get()

    # def unknownLegal(self, state):
    #     neighbors = [[state[0] - 1, state[1]],
    #                  [state[0], state[1] + 1],
    #                  [state[0] + 1, state[1]],
    #                  [state[0], state[1] - 1]]
    #     bools = []
    #     for neighbor in neighbors:
    #         iCheck = (neighbor[0] >= 0) and (neighbor[0] <= self.localMap.shape[0] - 1)
    #         jCheck = (neighbor[1] >= 0) and (neighbor[1] <= self.localMap.shape[1] - 1)
    #         if (not iCheck) or (not jCheck):
    #             bools.append(False)
    #         elif (self.localMap[neighbor[0]][neighbor[1]] == 1):
    #             bools.append(False)
    #         else:
    #             bools.append(True)
    #     if True in

class searchAStar():

    def __init__(self, initialState, goalState, localMap):
        self.goalState = goalState
        self.state = initialState
        self.localMap = localMap
        self.pathCostAccumulated = {str(initialState) : 0}
        self.cameFrom = {str(initialState) : 0}
        self.frontier = q.PriorityQueue()

    def solve(self):
        while True:
            if self.state == self.goalState:
                return self.getPath()
            children = self.getLegalMoves()
            self.expandFrontier(children)
            if not self.frontier.empty():
                self.state = self.frontier.get()[1]
            else:
                return "NO SOLUTION EXISTS"
            self.pathCostAccumulated[str(self.state)] = self.pathCostAccumulated[str(self.cameFrom[str(self.state)])] + 1

    def getPath(self):
        count = 0
        reversePath = []
        path = []
        while self.cameFrom[str(self.state)] != 0:
            reversePath.append(self.state)
            self.state = self.cameFrom[str(self.state)]
        for i in reversed(reversePath):
            path.append(i)
        count += 1
        print(count)
        return path

    def getLegalMoves(self):
        relativeNeighbors = [[self.state[0] - 1, self.state[1]],
                             [self.state[0], self.state[1] + 1],
                             [self.state[0] + 1, self.state[1]],
                             [self.state[0], self.state[1] - 1]]
        legalMoves = []
        for neighbor in relativeNeighbors:
            iCheck = (neighbor[0] >= 0) and (neighbor[0] <= self.localMap.shape[0] - 1)
            jCheck = (neighbor[1] >= 0) and (neighbor[1] <= self.localMap.shape[1] - 1)
            if iCheck and jCheck:
                if (self.localMap[neighbor[0]][neighbor[1]] == 0) or (self.localMap[neighbor[0]][neighbor[1]] == 3):
                    legalMoves.append(neighbor)
        # print(self.state)
        # print(legalMoves)
        # input('waiting')
        return legalMoves

    def expandFrontier(self, children):
        for i in range(0, len(children)):
            if str(children[i]) not in self.cameFrom:
                self.cameFrom[str(children[i])] = self.state
                h = self.manhattan(children[i])
                g = self.pathCostAccumulated[str(self.state)] + 1
                self.frontier.put((h + g, children[i]))

    def manhattan(self, child):
        di = abs(self.goalState[0] - child[0])
        dj = abs(self.goalState[1] - child[1])
        return di + dj
