import time

def times(func):
    nowtime=time.time()
    def wrap(*args,**kw):
        result=func(*args,**kw)
        print "{}s".format(time.time()-nowtime)
        return result
    return wrap
