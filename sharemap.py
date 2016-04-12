import numpy as np

def shareMap(robot1,robot2,dir1,dir2):
    item=2 # Location of the other robot

    #arr1=robot1().localMap
    #arr2=robot2().localMap
    #if (dir1==2 and dir2==0) or (dir1==0 and dir2==2):

    # Assigns arrays according to relative locations of robot
    if dir1==2 and dir2==0:
        arr1=robot1
        arr2=robot2
    elif dir1==0 and dir2==2:
        arr1=robot2
        arr2=robot1
    elif dir1==1 and dir2==3:
        arr1=np.transpose(robot1)
        arr2=np.transpose(robot2)
    elif dir1==3 and dir2==1:
        arr1=np.transpose(robot2)
        arr2=np.transpose(robot1)
    # 1 Ignore this comment
    size1=arr1.shape
    size2=arr2.shape
    # 2 Ignore this comment
    sizcol=abs(size1[1]-size2[1])
    #print(sizcol)
    # 3 Ignore this comment

    # Reshaping matrices for convenience
    if size2[1]>size1[1]:
        for n in range(sizcol):
            arr1 = np.insert(arr1,size1[1],3,1)
    print("Array1\n",arr1)
    if size1[1]>size2[1]:
        for n in range(sizcol):
            arr2 = np.insert(arr2,size2[1],3,1)
    print("Array2\n",arr2)
    itemindex1=np.where(arr1==item)
    itemindex2=np.where(arr2==item)
    #print((itemindex1[0][0],itemindex1[1][0]),(itemindex2[0][0],itemindex2[1][0]))
    nsize1=arr1.shape
    nsize2=arr2.shape
    #print(nsize1,nsize2)
    #print(itemindex2[0][0])

    # Sharing Information Part1
    for i in range((itemindex2[0][0]+2) if (itemindex2[0][0]>itemindex1[0][0]) else (itemindex1[0][0]+1)):
        for j in range(nsize1[1]):
            #print(i)
            if (itemindex1[0][0]-i)<0:
                arr1=np.insert(arr1,0,arr2[itemindex2[0][0]+(1-i)],0)
                break
            elif arr1[itemindex1[0][0]-i][j]==3 and (itemindex1[0][0]-i)>=0:
                arr1[itemindex1[0][0]-i][j]=arr2[itemindex2[0][0]+(1-i)][j]
            elif (itemindex2[0][0]+(1-i))<0:
                arr2=np.insert(arr2,0,arr1[itemindex1[0][0]-i],0)
                break
            elif arr2[itemindex2[0][0]+(1-i)][j]==3 and (itemindex2[0][0]+(1-i))>=0:
                arr2[itemindex2[0][0]+(1-i)][j]=arr1[itemindex1[0][0]-i][j]

    # Sharing Information Part2
    sizdiff1=nsize1[0]-(itemindex1[0][0]+1)
    sizdiff2=nsize2[0]-(itemindex2[0][0]+2)
    itemindex1=np.where(arr1==item)
    itemindex2=np.where(arr2==item)
    #print(sizdiff1,sizdiff2)
    sizdiff=sizdiff1 if sizdiff1>=sizdiff2 else sizdiff2
    for i in range(sizdiff):
        for j in range(nsize1[1]):
            if i>(sizdiff1-1):
                arr1=np.insert(arr1,(itemindex1[0][0]+1+i),arr2[itemindex2[0][0]+2+i],0)
                break
            elif i>(sizdiff2-1):
                arr2=np.insert(arr2,(itemindex2[0][0]+2+i),arr1[itemindex1[0][0]+1+i],0)
                break
            elif arr1[itemindex1[0][0]+1+i][j]==3:
                arr1[itemindex1[0][0]+1+i][j]=arr2[itemindex2[0][0]+2+i][j]
            elif arr2[itemindex2[0][0]+2+i][j]==3:
                arr2[itemindex2[0][0]+2+i][j] = arr1[itemindex1[0][0]+1+i][j]
    print("Array1\n",arr1)
    print("Array2\n",arr2)

    # Return Values
    if dir1==2 and dir2==0:
        return arr2,arr1
    elif dir1==0 and dir2==2:
        return arr1,arr2
    elif dir1==1 and dir2==3:
        return np.transpose(arr2),np.transpose(arr1)
    elif dir1==3 and dir2==1:
        return np.transpose(arr1),np.transpose(arr2)
    # 4 Ignore this comment

# Test the code
# Uncomment to test the following case
'''robot1=np.array([[0,1,3,3],[0,0,0,0],[1,1,0,3],[3,3,0,3],[0,0,2,0],[3,3,3,1],[3,3,3,3],[0,0,0,1]])
robot2=np.array([[0,0,2,0],[0,0,0,0],[1,1,0,3],[1,1,1,1]])
(array1,array2)=shareMap(robot1,robot2,2,0)
print("Array1\n",array1)
print("Array2\n",array2)'''

# Uncomment to test the following case
robot1=np.array([[0,1,3,3],[0,0,0,0],[1,1,0,2],[3,1,0,3],[0,0,1,0]])
robot2=np.array([[1,3,0,0],[0,3,0,0],[1,2,0,0],[1,0,1,0]])
(array1,array2)=shareMap(robot1,robot2,1,3)
print("Array1\n",array1)
print("Array2\n",array2)
