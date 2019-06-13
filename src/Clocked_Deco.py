import time
from Errors import CacheKeyError

def clock(func, logger):
    def clocked(*args):
        t0 = time.perf_counter()
        try:
            name = func.__name__
            logger.info('[>>>>] Work: "%s" started.' % (name))
            result = func(*args)
            elapsed = time.perf_counter()-t0
            # arg_str = ", ".join(repr(arg) for arg in args)
            # print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
            logger.info('[<<<<] [%0.8fs] Work: "%s" finished. Return: "%r"' % (elapsed, name, result))
            return result
        except CacheKeyError as e:
            elapsed = time.perf_counter()-t0
            name = func.__name__
            logger.info('[Fail] [%0.8fs] Work: "%s" encounters an error. Return: "False"' % (elapsed, name))
            logger.info(e.message)
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