import numpy as np
import sharemap
def share_check(locList,robList):
    for i in range(len(locList)):
        for j in range(i+1,len(list)):
            if (((locList[i][0]-locList[j][0])==-1) and (abs(locList[i][1]-locList[j][1])!=1)):
                arr1=robList[i].localMap
                arr2=robList[j].localMap
                index1=np.where(arr1==2)
                index2=np.where(arr2==2)

                #Consider robot1. The following code will mark the position of robot2 as 2 in the local map of robot1.
                #The result from sharemap function will have only one 2 and it will indicate the location of robot1 in
                #first local map(robot1's local map). The same happens to robot2 and its local map.

                arr1[index1[0][0]][index1[1][0]]=0
                arr1[index1[0][0]+1][index1[1][0]]=2
                arr2[index2[0][0]][index2[1][0]]=0
                arr2[index2[0][0]-1][index2[1][0]]=2
                dir1=2
                dir2=0
                (robList[i].localMap,robList[j].localMap)=sharemap.shareMap(arr1,arr2,dir1,dir2)
            elif (((locList[i][0]-locList[j][0])==1)  and (abs(locList[i][1]-locList[j][1])!=1)):
                arr1=robList[i].localMap
                arr2=robList[j].localMap
                index1=np.where(arr1==2)
                index2=np.where(arr2==2)
                arr1[index1[0][0]][index1[1][0]]=0
                arr1[index1[0][0]-1][index1[1][0]]=2
                arr2[index2[0][0]][index2[1][0]]=0
                arr2[index2[0][0]+1][index2[1][0]]=2
                dir1=0
                dir2=2
                (robList[i].localMap,robList[j].localMap)=sharemap.shareMap(arr1,arr2,dir1,dir2)
            elif (((locList[i][1]-locList[j][1])==-1) and (abs(locList[i][0]-locList[j][0])!=1)):
                arr1=robList[i].localMap
                arr2=robList[j].localMap
                index1=np.where(arr1==2)
                index2=np.where(arr2==2)
                arr1[index1[0][0]][index1[1][0]]=0
                arr1[index1[0][0]][index1[1][0]+1]=2
                arr2[index2[0][0]][index2[1][0]]=0
                arr2[index2[0][0]][index2[1][0]-1]=2
                dir1=1
                dir2=3
                (robList[i].localMap,robList[j].localMap)=sharemap.shareMap(arr1,arr2,dir1,dir2)
            elif (((locList[i][1]-locList[j][1])==1) and (abs(locList[i][0]-locList[j][0])!=1)):
                arr1=robList[i].localMap
                arr2=robList[j].localMap
                index1=np.where(arr1==2)
                index2=np.where(arr2==2)
                arr1[index1[0][0]][index1[1][0]]=0
                arr1[index1[0][0]][index1[1][0]-1]=2
                arr2[index2[0][0]][index2[1][0]]=0
                arr2[index2[0][0]][index2[1][0]+1]=2
                dir1=3
                dir2=1
                (robList[i].localMap,robList[j].localMap)=sharemap.shareMap(arr1,arr2,dir1,dir2)
            else:
                return
