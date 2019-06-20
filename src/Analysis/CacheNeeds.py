from Errors import CacheKeyError
import functools

predefinedCacheKeyHints = {
    "test": "This is a test hint.",
    "outputFolder": "A folder path(string) for logger file and figures: Auto provided when Discoverer is initiated.",
    "groupName": "A string of the group name: Should be defined by hand.",
    "friendList": "A dict mapping WeChat ID to name: Can be returned by DbManager.getFrindList()",
    "textMessagesSplitedByIdInGroupChat": "A dict splits all text messages by WeChat IDs: Can be produced by Middlewares.textMessagesSplitedByIdInGroupChat"
}

def needs(*ns):
    def needsChecked(func):
        @functools.wraps(func)
        def wrapped_f(historyData, cache, logger):
            em = []
            for n in ns:
                if n not in cache:
                    em.append(" > CacheKeyError: '"+ n +"'. Cache needs check failed for: " + func.__name__ + "\n"
                        + (("    - Hint: " + predefinedCacheKeyHints[n]) if n in predefinedCacheKeyHints else "    - Not a pre-defined key name."))
            if len(em) != 0:
                raise CacheKeyError("\n".join(em))
            return func(historyData, cache, logger)
        return wrapped_f
    return needsChecked