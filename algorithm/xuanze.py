#coding:utf-8
import seed
import times
"""选择排序
    在未排序序列中找到最小（大）元素，存放到排序序列的起始位置，
    再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。
    重复第二步，直到所有元素均排序完毕。
"""

@times.times
def selection(list): 
    n=len(list) 
    for i in range (0,n): 
        min = i 
        for j in range(i+1,n): 
            if list[j]<list[min]: 
                min=j 
        list[min],list[i]=list[i],list[min] 
    return list


print selection(seed.getNum())
#2万数字排序用时：22.3760001659s