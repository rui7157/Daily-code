#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-15 12:06:20
# @Author  : NvRay (nvray@foxmail.com)
#快速排序
import generate_num


def quick_sort(lists, left, right):
    # 快速排序
    if left >= right:
        return lists
    key = lists[left]
    low = left
    high = right
    while left < right:
        while left < right and lists[right] >= key:
            right -= 1
        lists[left] = lists[right]
        while left < right and lists[left] <= key:
            left += 1
        lists[right] = lists[left]
    lists[right] = key
    quick_sort(lists, low, left - 1)
    quick_sort(lists, left + 1, high)
    return lists

if __name__=="__main__":
    data=generate_num()
    quick_sort(data, 0, data[len(data)])