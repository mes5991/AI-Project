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
        self.visitedCells = []
        self.location = [0,0]
        self.goal = [0,0]
        self.goals = q.LifoQueue()
        self.goalsList = []
        self.goalsPut = []
        self.currentPath = q.Queue()

    def updateMap(self, worldLocation, envMatrix):
        worldNeighbors = self.getWorldNeighbors(worldLocation)
        neighborValues = []
        for neighbor in worldNeighbors:
            neighborI = neighbor[0]
            neighborJ = neighbor[1]
            neighborValue = envMatrix[neighborI][neighborJ]
            if neighborValue == 2:
                neighborValue = 0
            neighborValues.append(neighborValue)
        iBump = 0
        jBump = 0
        self.updateNorth(neighborValues[0])
        self.updateEast(neighborValues[1])
        self.updateSouth(neighborValues[2])
        self.updateWest(neighborValues[3])
        # return (iBump, jBump)

    def updateNorth(self, neighborValue):
        bumpCount = 0
        if self.location[0] == 0: #if local location is at top of matrix
            self.localMap = np.insert(self.localMap, 0, 3, axis = 0) #add a row in above location
            self.location[0] += 1 #Bump robots location down the matrix by 1
            self.goal[0] += 1 #Bump current goal down the matrix by 1
            tempPath = []
            tempGoals = []
            #If the current path to the current goal is not an empty queue,
            #bump each i value up by one
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            for i in tempPath:
                self.currentPath.put([i[0] + 1, i[1]])
            #Bump the i value up by one for every goal in the list of goals
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][0] += 1
            # while not self.goals.empty():
            #     tempGoals.append(self.goals().get())
            # for i in tempGoals:
            #     self.goals.put([i[0] + 1, i[1]])
            # bumpCount += 1
        self.localMap[self.location[0] - 1][self.location[1]] = neighborValue
        #If the cell above the robot is the top of the matrix, and that value is 0
        if (self.location[0] - 1 == 0) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, 0, 3, axis = 0) #Add a new row on top
            self.goal[0] += 1 #Bump goal
            self.location[0] += 1 #Bump location
            tempPath = []
            #If the current path to the current goal is not an empty queue,
            #bump each i value up by one
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            tempPath.reverse()
            for i in tempPath:
                self.currentPath.put([i[0] + 1, i[1]])
            #Bump the i value up by one for every goal in the list of goals
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][0] += 1

    def updateEast(self, neighborValue):
        if self.location[1] == self.localMap.shape[1] - 1:
            self.localMap = np.insert(self.localMap, self.localMap.shape[1], 3, axis = 1)
        self.localMap[self.location[0]][self.location[1] + 1] = neighborValue
        if (self.location[1] + 1 == self.localMap.shape[1] - 1) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, self.localMap.shape[1], 3, axis = 1)

    def updateSouth(self, neighborValue):
        if self.location[0] == self.localMap.shape[0] - 1:
            self.localMap = np.insert(self.localMap, self.localMap.shape[0], 3, axis = 0)
        self.localMap[self.location[0] + 1][self.location[1]] = neighborValue
        if (self.location[0] + 1 == self.localMap.shape[0] - 1) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, self.localMap.shape[0], 3, axis = 0)

    def updateWest(self, neighborValue):
        bumpCount = 0
        if self.location[1] == 0:
            self.localMap = np.insert(self.localMap, 0, 3, axis = 1)
            self.location[1] += 1
            self.goal[1] += 1
            tempPath = []
            tempGoals = []
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            for i in tempPath:
                self.currentPath.put([i[0], i[1] + 1])
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][1] += 1
            # while not self.goals.empty():
            #     tempGoals.append(self.goals().get())
            # for i in tempGoals:
            #     self.goals.put([i[0], i[1] + 1])
            # bumpCount += 1
        self.localMap[self.location[0]][self.location[1] - 1] = neighborValue
        if (self.location[1] - 1 == 0) and (neighborValue == 0):
            self.localMap = np.insert(self.localMap, 0, 3, axis = 1)
            self.location[1] += 1
            self.goal[1] += 1
            tempPath = []
            while not self.currentPath.empty():
                tempPath.append(self.currentPath.get())
            tempPath.reverse()
            for i in tempPath:
                self.currentPath.put([i[0], i[1] + 1])
            for i in range(0, len(self.goalsList)):
                self.goalsList[i][1] += 1
        #     bumpCount += 1
        # return bumpCount

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

    def getGoals(self):
        #Get neighbors of current location
        # print(self.localMap)
        # input("in get goals")
        neighbors = [[self.location[0] - 1, self.location[1]],
                     [self.location[0], self.location[1] + 1],
                     [self.location[0] + 1, self.location[1]],
                     [self.location[0], self.location[1] - 1]]

        for neighbor in neighbors:
            #Check if neighbor is within map range and not in visited cells
            iRange = (neighbor[0] >= 0) and (neighbor[0] <= (self.localMap.shape[0] - 1))
            jRange = (neighbor[1] >= 0) and (neighbor[1] <= (self.localMap.shape[1] - 1))
            if (iRange) and (jRange):
                #Check if neighbor value is 0 which ensures a path to the potential goal
                if (self.localMap[neighbor[0]][neighbor[1]] == 0):
                    #Get neighbors of the current neighbor
                    neighborsOfNeighbors = [[neighbor[0] - 1, neighbor[1]],
                                            [neighbor[0], neighbor[1] + 1],
                                            [neighbor[0] + 1, neighbor[1]],
                                            [neighbor[0], neighbor[1] - 1]]
                    # print(neighborsOfNeighbors)
                    # input('for loop')
                    for neighborNeighbor in neighborsOfNeighbors:

                        #Check if neighbor of neighbor is within map range
                        iRange = (neighborNeighbor[0] >= 0) and (neighborNeighbor[0] <= (self.localMap.shape[0] - 1))
                        jRange = (neighborNeighbor[1] >= 0) and (neighborNeighbor[1] <= (self.localMap.shape[1] - 1))
                        if (iRange) and (jRange):
                            #Check if neighbor of neighbor is of value 3 ensuring that it has not been discovered yet
                            # if (self.localMap[neighborNeighbor[0]][neighborNeighbor[1]] == 3) and (neighborNeighbor not in self.goalsPut):
                            if (self.localMap[neighborNeighbor[0]][neighborNeighbor[1]] == 3) and (neighborNeighbor not in self.goalsList):
                                # print(neighborNeighbor)
                                # input('adding goal')
                                self.goalsList.append(neighborNeighbor)
                                #Add neighbor of neighbor and path to goals queue
                                # self.goalsPut.append(neighborNeighbor)
                                # self.goals.put(neighborNeighbor)


    def getNextGoal(self):
        #Initilize temporary manhattan distance and goal selection
        manhattan = None
        currentGoal = None
        #Use manhattan distance to select the closest goal
        for goal in self.goalsList:
            di = abs(goal[0] - self.location[0])
            dj = abs(goal[1] - self.location[1])
            if (manhattan == None) or (di + dj < manhattan):
                manhattan = di+dj
                currentGoal = goal
        #Remove the selected goal from the goals list
        self.goalsList.remove(currentGoal)
        return currentGoal


    def getClosestUnknown(self):
            state = self.location[:]
            nextState = q.Queue()
            visitedCells = []
            while True:
                neighbors = [[state[0] - 1, state[1]],
                             [state[0], state[1] + 1],
                             [state[0] + 1, state[1]],
                             [state[0], state[1] - 1]]
                # print("local map\n", self.localMap)
                # print("State:", state)
                # print("neighbors:", neighbors)
                # input("waiting before filter...")
                for neighbor in neighbors:
                    if neighbor not in visitedCells:
                        visitedCells.append(neighbor)
                        if (neighbor[0] >= 0) and (neighbor[0] <= (self.localMap.shape[0] - 1)) and (neighbor[1] >= 0) and (neighbor[1] <= (self.localMap.shape[1] - 1)):
                            # print("neighbors after filter", neighbors)
                            # input("waiting after filter...")
                            if (self.localMap[neighbor[0]][neighbor[1]] == 3):
                                search0 = searchAStar(self.location, neighbor, self.localMap)
                                solution = search0.solve()
                                # print("neighbor", neighbor)
                                # print("solution", solution)
                                if solution != None:
                                    self.goal = neighbor
                                    return solution
                            nextState.put(neighbor)
                if not nextState.empty():
                    state = nextState.get()
                else:
                    return None

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
                return None
            self.pathCostAccumulated[str(self.state)] = self.pathCostAccumulated[str(self.cameFrom[str(self.state)])] + 1

    def getPath(self):
        reversePath = []
        path = []
        while self.cameFrom[str(self.state)] != 0:
            reversePath.append(self.state)
            self.state = self.cameFrom[str(self.state)]
        for i in reversed(reversePath):
            path.append(i)
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
