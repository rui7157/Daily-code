#coding:utf-8
import seed
import times
"""冒泡排序算法
冒泡排序算法的运作如下：

    比较相邻的元素。如果第一个比第二个大，就交换他们两个。
    对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。
    针对所有的元素重复以上的步骤，除了最后一个。
    持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。

"""

num=seed.getNum()
@times.times
def bubble(list):
    listCount=len(list)
    for time in range(listCount):
        time=listCount-time
        for i in range(time-1):
            if list[i]>list[i+1]:
                list[i],list[i+1]=list[i+1],list[i]
    return list

print bubble(num)

#2万数字排序用时：49.1860001087s