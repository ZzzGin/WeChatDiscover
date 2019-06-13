from Errors import CacheKeyError
import functools

def needs(*ns):
    def needsChecked(func):
        @functools.wraps(func)
        def wrapped_f(historyData, cache, logger):
            for n in ns:
                if n not in cache:
                    raise CacheKeyError(" > CacheKeyError: '"+ n +"'. Cache needs check failed for:" + func.__name__)
            return func(historyData, cache, logger)
        return wrapped_f
    return needsChecked