 #coding:utf-8
import seed
import times
"""插入排序
    从第一个元素开始，该元素可以认为已经被排序
    取出下一个元素，在已经排序的元素序列中从后向前扫描
    如果该元素（已排序）大于新元素，将该元素移到下一位置
    重复步骤3，直到找到已排序的元素小于或者等于新元素的位置
    将新元素插入到该位置后
    重复步骤2~5
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