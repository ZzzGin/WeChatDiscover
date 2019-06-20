import sys 
import os
sys.path.append(os.path.abspath('./src')) 
from Analysis.DataMapper.Mapper06082019 import mapper as m
from Analysis.CacheNeeds import needs

@needs("friendList")
def textMessagesSplitedByIdInGroupChat(historyData, cache, logger):
    r = dict()
    for h in historyData:
        if h[m.Type]==1:
            if h[m.Des]==0:
                r.setdefault("myself", ["", []])[1].append(h[m.Message])
            else:
                s = h[m.Message].split(":")
                Id = s[0]
                text = "".join(s[1:]).strip("\n")
                r.setdefault(Id, [cache["friendList"][Id], []])[1].append(text)
    cache["textMessagesSplitedByIdInGroupChat"] = r
    logger.info("[Info] Groupchat messages splited.")
    for c in r:
        logger.info(" > [" + c + "] " + r[c][0] + ": " + str(len(r[c][1])) + " messages.")
    return True