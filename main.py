from environment import Environment
from robot import searchAStar
import random
import queue as q
import numpy as np
import pygame
np.set_printoptions(threshold = np.nan, suppress = True, linewidth = 300)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 25, 250)
RED = (255, 0, 0)
PURPLE = (160, 32, 240)
robotCount = 4
newInfo = []
stuck = []

pygame.init()
M = robotCount*500
size = (M, 300)  # Set the width and height of the screen [width, height]
screen1 = pygame.display.set_mode(size)
screen1.fill(WHITE)
pygame.display.set_caption("World Map")


z = M / 200  # set the scaling factor based on screen size

"""Code below this line is code for multi-robot search"""
def main():
   # Initialize environment (SIZE, Wall%, # of Robots)
    World = Environment((20, 20), 0, robotCount)
    print("World Map:\n", World.envMatrix)
    for i in range(robotCount):
        World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix)
        World.robots[i].getGoals()
        newInfo.append(False)
        stuck.append(False)
        print("Local Map", i, "\n", World.robots[i].localMap)
    done = False
    trace = False
    count = 0

    # Start pygame screen in loop .Program quits when user closes the screen
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop Run loop while any robots are not stuck
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
                    nextMove = World.robots[i].currentPath.get()
                    #Only move to the next location if it is empty
                    if World.robots[i].localMap[nextMove[0]][nextMove[1]] == 0:
                        direction = [nextMove[0] - World.robots[i].location[0], nextMove[1] - World.robots[i].location[1]]
                        World.robots[i].move(nextMove)
                        World.updateEnvMatrix(i, direction)
                        World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix)
                        World.robots[i].getGoals()
                        renderMap(World.robots[i].localMap,i)
                    else:
                        newInfo[i] = True
            if trace:
                print("World Map:\n", World.envMatrix)
                for i in range(robotCount):
                    print("Local Map", i,"\n", World.robots[i].localMap)
                input('waiting')
            renderMap(World.envMatrix)

        print("World Map:\n", World.envMatrix)
        for i in range(robotCount):
            print("Local Map", i,"\n", World.robots[i].localMap)

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

if  __name__ == "__main__":
    main()