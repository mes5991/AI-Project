from environment import Environment
from robot import searchAStar
import random

Env1 = Environment((10, 10), .5, 1)
print("World Map:\n", Env1.envMatrix)

for i in range(50):
    Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
    # print("Robot World Location: ", Env1.robotsLocation[0])
    # print("Robot Relative Location: ", Env1.robots[0].location)
    # print("Robot Local Map:\n", Env1.robots[0].localMap)
    legalMoves = Env1.robots[0].getLegalMoves(Env1.robots[0].location)
    choice = random.choice(legalMoves)
    direction = [choice[0] - Env1.robots[0].location[0], choice[1] - Env1.robots[0].location[1]]
    # print("Direction: ", direction)
    Env1.robots[0].move(choice)
    Env1.updateEnvMatrix(0, direction)
    # print("World Map:\n", Env1.envMatrix)
Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
print("Robot Local Map:\n", Env1.robots[0].localMap)
print("Closest Unknown", Env1.robots[0].getClosestUnknown())
print("Robot Relative Location: ", Env1.robots[0].location)
input('waiting...')
Env1.robots[0].goal = Env1.robots[0].getClosestUnknown()
search0 = searchAStar(Env1.robots[0].location, Env1.robots[0].goal, Env1.robots[0].localMap)
Env1.robots[0].currentPath = search0.solve()
print(Env1.robots[0].currentPath)



# for i in range(0, len(Env1.robots)):
#     print("Robot", i, "World Location: ", Env1.robotsLocation[i])
#     print("Robot", i, "Relative Location: ", Env1.robots[i].location)
#     Env1.robots[i].updateMap(Env1.robotsLocation[i], Env1.envMatrix)
#     print("Robot", i, "Local Map After Update:\n", Env1.robots[i].localMap)
#     legalMoves = Env1.robots[i].getLegalMoves()
#     print("Robot", i, "Legal Moves:", legalMoves)
#     Env1.robots[i].move(legalMoves[0])
#     Env1.robots[i].updateMap(Env1.robotsLocation[i], Env1.envMatrix)
#     print("Robot", i, "Local Map After Move and Update\n", Env1.robots[i].localMap)
#     print("Robot", i, "Relative Location: ", Env1.robots[i].location)
