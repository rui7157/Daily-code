 #coding:utf-8
import seed
import times
"""希尔排序
    每次以一定步长(就是跳过等距的数)进行排序，直至步长为1.
"""
numList=seed.getNum()
@times.times
def insertion(numList):
    newList=[numList[0]]
    print newList
    for index,i in enumerate(numList[1:]):
        for l in range(len(newList)):
            if newList[l]>i:
                newList.insert(l,i)
                break
            elif l==len(newList)-1:
                newList.append(i)
    return newList

print insertion(numList)


#2万数字排序用时：21.4830000401s