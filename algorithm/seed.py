import random

def getNum(count=20000):
    """return data type:list"""

    return [random.randint(0,10000) for n in range(count)]
