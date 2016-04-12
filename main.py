from environment import Environment
from robot import searchAStar
import random
import queue as q
import numpy as np

np.set_printoptions(threshold = np.nan, suppress = True, linewidth = 300)
#Initilize environment (SIZE, Wall%, # of Robots)
Env1 = Environment((10, 10), .45, 2)
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
print("Local Map:\n", Env1.robots[0].localMap)
