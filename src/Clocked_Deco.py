import time
from Errors import CacheKeyError

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        try:
            result = func(*args)
            elapsed = time.perf_counter()-t0
            name = func.__name__
            # arg_str = ", ".join(repr(arg) for arg in args)
            # print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
            print('[Done] [%0.8fs] Work: "%s" is done. Return: "%r"' % (elapsed, name, result))
            return result
        except CacheKeyError as e:
            elapsed = time.perf_counter()-t0
            name = func.__name__
            print('[Fail] [%0.8fs] Work: "%s" encounters an error. Return: "False"' % (elapsed, name))
            print(e.message)
            return False
    return clocked

if __name__ == "__main__":
    @clock
    def loops(l):
        for i in range(len(l)):
            pair = (i, l[i])
        return "Finished"

    @clock
    def test():
        for i in range(1, 7):
            lst = range(10**i)
            loops(lst)
        return "TestPassed"
    test()