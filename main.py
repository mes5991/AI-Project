from environment import Environment
from robot import searchAStar
import queue as q
import xlrd
import numpy as np

# Initialize environment (SIZE, Wall%, # of Robots)

file_location = 'D:/Academics/Artificial Intelligence/Project/AI-Project-nested_Astar_Search_-No_BFS-/map.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
env = []

env1 = np.zeros((100, 100))

for col in range(sheet.ncols):
    for row in range(sheet.nrows):
        env1[row, col] = int(sheet.cell_value(row, col))

# env = [[ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
#       [ 1,  0,  0,  1,  0,  0,  0,  0,  0,  1],
#       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  1],
#       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  1],
#       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  1],
#       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  1],
#       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  1],
#       [ 1,  0,  1,  0,  1,  0,  0,  0,  0,  1],
#       [ 1,  0,  0,  0,  0,  0,  1,  0,  0,  1],
#       [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1]]

Env1 = Environment((100,100), .25, 1, env=env1)
print(Env1.envMatrix)
# Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
# Env1.robots[0].getGoals()
#
# print("World Map:\n", Env1.envMatrix)
# print("Local Map:\n", Env1.robots[0].localMap)
#
# trace = False
# newInfo = False
# stuck = False
# while not stuck: #Loop until robot has no unknown locations
#     #If the current goal is no longer unknown, get new goal. Goal initializes as origin.
#     if (Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] != 3) or newInfo:
#         legalGoal = False
#         while not legalGoal and not stuck:
#             if len(Env1.robots[0].goalsList) > 0:
#                 if not newInfo:
#                     Env1.robots[0].goal = Env1.robots[0].getNextGoal()
#                 newInfo = False
#                 if Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3:
#                     Search0 = searchAStar(Env1.robots[0].location, Env1.robots[0].goal, Env1.robots[0].localMap)
#                     solution = Search0.solve()
#                     Env1.robots[0].currentPath = q.Queue()
#                     for i in solution:
#                         Env1.robots[0].currentPath.put(i)
#                         legalGoal = True
#                 # else:
#                 #     print("Removing goal: {}".format(Env1.robots[0].goal))
#             else:
#                 stuck = True
#             # if not Env1.robots[0].goals.empty():
#             #     Env1.robots[0].goal = Env1.robots[0].goals.get()
#             #     if Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3:
#             #         Search0 = searchAStar(Env1.robots[0].location, Env1.robots[0].goal, Env1.robots[0].localMap)
#             #         solution = Search0.solve()
#             #         Env1.robots[0].currentPath = q.Queue()
#             #         # print("Current Goal:", Env1.robots[0].goal)
#             #         for i in solution:
#             #             Env1.robots[0].currentPath.put(i)
#             #         legalGoal = True
#             # else:
#             #     stuck = True
#     if trace:
#         print("World Map:\n", Env1.envMatrix)
#         print("Local Map:\n", Env1.robots[0].localMap)
#         print("World Location:", Env1.robotsLocation[0])
#         print("Relative Location:", Env1.robots[0].location)
#         print("Current Goal", Env1.robots[0].goal)
#         print("Goals list", Env1.robots[0].goalsList)
#         input('waiting...')
#     nextMove = Env1.robots[0].currentPath.get()
#     # print("World Map:\n", Env1.envMatrix)
#     # print("Local Map:\n", Env1.robots[0].localMap)
#     # print("Next Move:", nextMove)
#     # print("World Location", Env1.robotsLocation[0])
#     # print("Local Location", Env1.robots[0].location)
#     if Env1.robots[0].localMap[nextMove[0]][nextMove[1]] == 0:
#         direction = [nextMove[0] - Env1.robots[0].location[0], nextMove[1] - Env1.robots[0].location[1]]
#         Env1.robots[0].visitedCells.append(Env1.robots[0].location)
#         Env1.robots[0].move(nextMove)
#         Env1.updateEnvMatrix(0, direction)
#         Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
#         Env1.robots[0].getGoals()
#         # goalCheck = Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3
#     else:
#         newInfo = True
#         # Env1.robots[0].goals.put(Env1.robots[0].goal)
#
#     # goalCheck = Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3
#     # while goalCheck and not stuck:
#     #     nextMove = Env1.robots[0].currentPath.get()
#     #     print("World Map:\n", Env1.envMatrix)
#     #     print("Local Map:\n", Env1.robots[0].localMap)
#     #     print("Next Move:", nextMove)
#     #     print("World Location", Env1.robotsLocation[0])
#     #     print("Local Location", Env1.robots[0].location)
#     #     if Env1.robots[0].localMap[nextMove[0]][nextMove[1]] == 0:
#     #         direction = [nextMove[0] - Env1.robots[0].location[0], nextMove[1] - Env1.robots[0].location[1]]
#     #         Env1.robots[0].visitedCells.append(Env1.robots[0].location)
#     #         Env1.robots[0].move(nextMove)
#     #         Env1.updateEnvMatrix(0, direction)
#     #         Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
#     #         goalCheck = Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3
#     #     else:
#     #         goalCheck = False
#     #
#     #     # input("Waiting")
#     # Env1.robots[0].currentPath = q.Queue()
# print("World Map:\n", Env1.envMatrix)
# print("Local Map:\n", Env1.robots[0].localMap)

# print(Env1.robots[0].localMap)
# while not Env1.robots[0].goals.empty():
#     print (Env1.robots[0].goals.get())
# input("DONE")
# print("Robot World Location: ", Env1.robotsLocation[0])
# print("Robot Relative Location: ", Env1.robots[0].location)
# print("Robot Local Map:\n", Env1.robots[0].localMap)
# stuck = False
# while not stuck:
#     Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
#     if Env1.robots[0].currentPath.empty():
#         # input("IN NEW PATH SEARCH...")
#         solution = Env1.robots[0].getClosestUnknown()
#         if solution == None:
#             stuck = True
#         else:
#             for i in solution:
#                 Env1.robots[0].currentPath.put(i)
#
#     # iBump = 0
#     # jBump = 0
#     while (Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3) and (not Env1.robots[0].currentPath.empty()) and not stuck:
#         # print("Robot World Location: ", Env1.robotsLocation[0])
#         # print("Robot Relative Location: ", Env1.robots[0].location)
#         # print("Robot Local Map:\n", Env1.robots[0].localMap)
#         # print("Path to goal,", Env1.robots[0].goal, ",\n", solution)
#         # input("waiting...")
#         nextMove = Env1.robots[0].currentPath.get()
#         # print(Env1.robots[0].localMap.size)
#         # print("nextMove:", nextMove)
#         # nextMove[0] += iBump
#         # nextMove[1] += jBump
#         if Env1.robots[0].localMap[nextMove[0]][nextMove[1]] == 0:
#             direction = [nextMove[0] - Env1.robots[0].location[0], nextMove[1] - Env1.robots[0].location[1]]
#             Env1.robots[0].move(nextMove)
#             Env1.updateEnvMatrix(0, direction)
#             Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
#         else:
#             Env1.robots[0].currentPath = q.Queue()
#         # iBump += iBumpDiff
#         # jBump += jBumpDiff
#     Env1.robots[0].currentPath = q.Queue()
#
# print(Env1.robots[0].localMap)
# print(Env1.envMatrix)
#
#
#
#
#
#
# # for i in range(50):
# #     Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
# #     # print("Robot World Location: ", Env1.robotsLocation[0])
# #     # print("Robot Relative Location: ", Env1.robots[0].location)
# #     # print("Robot Local Map:\n", Env1.robots[0].localMap)
# #     legalMoves = Env1.robots[0].getLegalMoves(Env1.robots[0].location)
# #     choice = random.choice(legalMoves)
# #     direction = [choice[0] - Env1.robots[0].location[0], choice[1] - Env1.robots[0].location[1]]
# #     # print("Direction: ", direction)
# #     Env1.robots[0].move(choice)
# #     Env1.updateEnvMatrix(0, direction)
# #     # print("World Map:\n", Env1.envMatrix)
# # Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
# # print("Robot Local Map:\n", Env1.robots[0].localMap)
# # print("Closest Unknown", Env1.robots[0].getClosestUnknown())
# # print("Robot Relative Location: ", Env1.robots[0].location)
# # input('waiting...')
# # Env1.robots[0].goal = Env1.robots[0].getClosestUnknown()
# # search0 = searchAStar(Env1.robots[0].location, Env1.robots[0].goal, Env1.robots[0].localMap)
# # Env1.robots[0].currentPath = search0.solve()
# # print(Env1.robots[0].currentPath)
#
#
#
# # for i in range(0, len(Env1.robots)):
# #     print("Robot", i, "World Location: ", Env1.robotsLocation[i])
# #     print("Robot", i, "Relative Location: ", Env1.robots[i].location)
# #     Env1.robots[i].updateMap(Env1.robotsLocation[i], Env1.envMatrix)
# #     print("Robot", i, "Local Map After Update:\n", Env1.robots[i].localMap)
# #     legalMoves = Env1.robots[i].getLegalMoves()
# #     print("Robot", i, "Legal Moves:", legalMoves)
#     Env1.robots[i].move(legalMoves[0])
#     Env1.robots[i].updateMap(Env1.robotsLocation[i], Env1.envMatrix)
#     print("Robot", i, "Local Map After Move and Update\n", Env1.robots[i].localMap)
#     print("Robot", i, "Relative Location: ", Env1.robots[i].location)
