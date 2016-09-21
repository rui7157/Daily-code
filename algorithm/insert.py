#coding:utf-8
import times
import seed
numList=seed.getNum()

@times.times
def insert_sort(list):
    n = len(list)
    for i in range(1, n):
        # 后一个元素和前一个元素比较
        # 如果比前一个小
        if list[i] < list[i - 1]:
            # 将这个数取出
            temp = list[i]
            # 保存下标
            index = i
            # 从后往前依次比较每个元素
            for j in range(i - 1, -1, -1):
                # 和比取出元素大的元素交换
                if list[j] > temp:
                    list[j + 1] = list[j]
                    index = j
                else:
                    break
            # 插入元素
            list[index] = temp
    return list


print insert_sort(numList)