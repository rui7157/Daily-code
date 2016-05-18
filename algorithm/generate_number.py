import random
def rend(size=100):
    seed=[]
    for i in range(size):
        seed.append(random.randint(0, 100000))
    return seed