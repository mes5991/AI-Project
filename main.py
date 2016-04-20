from environment import Environment
from robot import searchAStar
import random
import queue as q
import numpy as np
from sharemap_Matt import shareMap
import copy
import pygame

np.set_printoptions(threshold = np.nan, suppress = True, linewidth = 300)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 25, 250)
RED = (255, 0, 0)
PURPLE = (160, 32, 240)

"""Code below this line is code for multi-robot search"""

robotCount = 2
newInfo = []
stuck = []
chosenLocations = False
done = False

pygame.init()
M = robotCount*500
size = (M, 300)  # Set the width and height of the screen [width, height]
screen1 = pygame.display.set_mode(size)
screen1.fill(WHITE)
pygame.display.set_caption("World Map")
z = M / 200  # set the scaling factor based on screen size

#Initilize environment (SIZE, Wall%, # of Robots)
World = Environment((50,50), .1, robotCount, chosenLocations)
print("World Map:\n", World.envMatrix)
for i in range(robotCount):
    World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix, i)
    World.robots[i].getGoals()
    newInfo.append(False)
    stuck.append(False)
    print("Local Map", i,"\n", World.robots[i].localMap)
# input('top')

def renderMap(mapMatrix,k=None):
    r, c = np.shape(mapMatrix)

    for i in range(r):
        for j in range(c):
            m = i * z
            n = j * z
            if k != None:
                m+=z*20+k*z*20

            if mapMatrix[i, j] == 1.0:
                pygame.draw.rect(screen1, BLACK, [m, n, z, z])
            elif mapMatrix[i, j] == 2.0:
                pygame.draw.rect(screen1, PURPLE, [m, n, z, z])
            elif mapMatrix[i, j] == 3.0:
                pygame.draw.rect(screen1, BLUE, [m, n, z, z])
            else:
                pygame.draw.rect(screen1, WHITE, [m, n, z, z])
    pygame.display.flip()
    # --- Limit to frames per second
    clock = pygame.time.Clock()
    clock.tick(50)

trace = False
count = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop Run loop while any robots are not stuck
    #Run loop while any robots are not stuck
    while (False in stuck):
        for i in range(robotCount):

            """Goals Update"""
            #If the current goal is no longer unknown, get new goal. Goal initializes as origin.
            if (World.robots[i].localMap[World.robots[i].goal[0]][World.robots[i].goal[1]] != 3) or newInfo[i]:
                legalGoal = False
                while not legalGoal and not stuck[i]:
                    #Are there any remaining goals?
                    if len(World.robots[i].goalsList) > 0:
                        #Do we have new info but havnt reached the current goal?
                        if not newInfo[i]:
                            #Get new goal from goals list
                            World.robots[i].goal = World.robots[i].getNextGoal()
                        newInfo[i] = False
                        #Is the current goal still unknown?
                        if World.robots[i].localMap[World.robots[i].goal[0]][World.robots[i].goal[1]] == 3:
                            #A* search to get path to goal
                            Search0 = searchAStar(World.robots[i].location, World.robots[i].goal, World.robots[i].localMap)
                            solution = Search0.solve()
                            World.robots[i].currentPath = q.Queue()
                            for step in solution:
                                World.robots[i].currentPath.put(step)
                                legalGoal = True
                        # else:
                        #     print("Removing goal: {}".format(World.robots[i].goal))
                    else:
                        #If no remaining goals, consider the robot stuck
                        stuck[i] = True

            """Movement update"""
            if not stuck[i]:
                #Get the next move from the current path
                nextMove = World.robots[i].currentPath.get()
                #Only move to the next location if it is empty
                if World.robots[i].localMap[nextMove[0]][nextMove[1]] == 0:
                    #Get direction of movement [0,1], [0,-1], [1,0], [-1,0]
                    direction = [nextMove[0] - World.robots[i].location[0], nextMove[1] - World.robots[i].location[1]]
                    #Move in local map
                    World.robots[i].move(nextMove)
                    #Move in world map
                    World.updateEnvMatrix(i, direction)
                    #Update local map with new sensor information
                    # print("Robot Number", i)
                    # print("Goals List", World.robots[i].goalsList)
                    # input("I like turtles")
                    World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix, i)
                    # print("Robot Number", i)
                    # print("Goals List", World.robots[i].goalsList)
                    # input("I like turtles")
                    """Share Map Functions"""
                    for botNeighbor in World.robots[i].botNeighbors:
                        # print("Current Local Map\n", World.robots[i].localMap)
                        # print("Current location:", World.robots[i].location)
                        #get direction of neighbor bot wrt current bot
                        direction = [botNeighbor[0] - World.robotsLocation[i][0], botNeighbor[1] - World.robotsLocation[i][1]]
                        #get neighbor bot index and local map for sharing
                        (neighborMap, neighborIndex) = World.getSharingInfo(i, direction)
                        # print("neighborMap\n", World.robots[neighborIndex].localMap)
                        # print("neighbor location:", World.robots[neighborIndex].location)
                        # print("World Map\n", World.envMatrix)
                        #Store old relative locations
                        oldBotLocalLocation = World.robots[i].location
                        oldNeighborLocalLocation = World.robots[neighborIndex].location
                        #Share map information. Directly modify robot maps and locations if necessary
                        (World.robots[i].localMap, World.robots[neighborIndex].localMap, World.robots[i].location, World.robots[neighborIndex].location) = shareMap(World.robots[i].localMap, neighborMap, direction)
                        # print("New Current bot map\n", World.robots[i].localMap)
                        # print("New neighbor map\n", World.robots[neighborIndex].localMap)
                        # print("Current location:", World.robots[i].location)
                        # print("neighbor location:", World.robots[neighborIndex].location)
                        # print(np.subtract(World.robots[i].localMap, World.robots[neighborIndex].localMap))
                        # input("Waiting...")
                        #Get change in location from before map sharing to after map sharing
                        (bot_di, bot_dj) = (abs(oldBotLocalLocation[0] - World.robots[i].location[0]), abs(oldBotLocalLocation[1] - World.robots[i].location[1]))
                        (neighbor_di, neighbor_dj) = (abs(oldNeighborLocalLocation[0] - World.robots[neighborIndex].location[0]), abs(oldNeighborLocalLocation[1] - World.robots[neighborIndex].location[1]))
                        #Update goal, goals list, and current path according to the change in location
                        World.robots[i].updateRelativeData(bot_di, bot_dj)
                        World.robots[neighborIndex].updateRelativeData(neighbor_di, neighbor_dj)
                        #Combine goals list into one mutual goal list
                        mutualGoalList = []
                        for goal in World.robots[i].goalsList:
                            if goal not in mutualGoalList:
                                mutualGoalList.append(goal)
                        for goal in World.robots[neighborIndex].goalsList:
                            if goal not in mutualGoalList:
                                mutualGoalList.append(goal)
                        World.robots[i].goalsList = copy.deepcopy(mutualGoalList)
                        World.robots[neighborIndex].goalsList = copy.deepcopy(mutualGoalList)
                    #Get new goals based on the previous movement
                    World.robots[i].getGoals()
                    renderMap(World.robots[i].localMap, i)
                else:
                    #If the next move is not empty, ignore the above code, and run A* again.
                    newInfo[i] = True
        if trace:
            print("World Map:\n", World.envMatrix)
            for i in range(robotCount):
                print("Local Map", i,"\n", World.robots[i].localMap)
            input('waiting')
        renderMap(World.envMatrix, i)
print("World Map:\n", World.envMatrix)
for i in range(robotCount):
    print("Local Map", i,"\n", World.robots[i].localMap)



"""Code below this line works for one robot only"""
"""#Initilize environment (SIZE, Wall%, # of Robots)
Env1 = Environment((96, 96), .2, 1)
Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
Env1.robots[0].getGoals()

print("World Map:\n", Env1.envMatrix)
print("Local Map:\n", Env1.robots[0].localMap)

trace = False
newInfo = False
stuck = False
while not stuck: #Loop until robot has no unknown locations


    #If the current goal is no longer unknown, get new goal. Goal initializes as origin.
    if (Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] != 3) or newInfo:
        legalGoal = False
        while not legalGoal and not stuck:
            if len(Env1.robots[0].goalsList) > 0:
                if not newInfo:
                    Env1.robots[0].goal = Env1.robots[0].getNextGoal()
                newInfo = False
                if Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3:
                    Search0 = searchAStar(Env1.robots[0].location, Env1.robots[0].goal, Env1.robots[0].localMap)
                    solution = Search0.solve()
                    Env1.robots[0].currentPath = q.Queue()
                    for i in solution:
                        Env1.robots[0].currentPath.put(i)
                        legalGoal = True
                # else:
                #     print("Removing goal: {}".format(Env1.robots[0].goal))
            else:
                stuck = True

    if trace:
        print("World Map:\n", Env1.envMatrix)
        print("Local Map:\n", Env1.robots[0].localMap)
        print("World Location:", Env1.robotsLocation[0])
        print("Relative Location:", Env1.robots[0].location)
        print("Current Goal", Env1.robots[0].goal)
        print("Goals list", Env1.robots[0].goalsList)
        input('waiting...')
    nextMove = Env1.robots[0].currentPath.get()
    if Env1.robots[0].localMap[nextMove[0]][nextMove[1]] == 0:
        direction = [nextMove[0] - Env1.robots[0].location[0], nextMove[1] - Env1.robots[0].location[1]]
        Env1.robots[0].move(nextMove)
        Env1.updateEnvMatrix(0, direction)
        Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
        Env1.robots[0].getGoals()
    else:
        newInfo = True

print("World Map:\n", Env1.envMatrix)
print("Local Map:\n", Env1.robots[0].localMap)"""
