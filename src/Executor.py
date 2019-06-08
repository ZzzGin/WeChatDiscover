from Errors import AddWorkError, CacheKeyError
from Clocked_Deco import clock

class Discoverer:
    def __init__(self):
        self.works = []
        self.failedWorks = []
        self.data = ()
        self.cache = Cache()
    
    def addWork(self, w):
        if w.__code__.co_argcount < 2:
            raise AddWorkError(" > AddWorkError: The variables of the analysis function should be ('input', 'cache')")
        if w.__code__.co_varnames[:2] == ("input", "cache"):
            self.works.append(clock(w))
        else:
            raise AddWorkError(" > AddWorkError: The variables of the analysis function should be ('input', 'cache')")
    
    def addWorks(self, *ws):
        for w in ws:
            self.addWork(w)
    
    def doWorks(self):
        for work in self.works:
            result = work(self.data, self.cache)
            if result == False:
                self.failedWorks.append(work)
    
    def tryFailedWorksAgain(self):
        fws = []
        for failedWork in self.failedWorks:
            result = failedWork(self.data, self.cache)
            if result == False:
                fws.append(failedWork)
        self.failedWorks = fws

class Cache(dict):
    def __getitem__(self, key):
        try:
            return super(Cache, self).__getitem__(key)
        except KeyError:
            raise CacheKeyError(" > CacheKeyError: '"+ key +"'. This work will be added to Discoverer.failedWorks. Run tryFailedWorksAgain() to avoid sequence error.")

if __name__ == "__main__":
    from Analysis import Character, Sentence, Wordcloud
    d = Discoverer()
    d.addWork(Sentence.SentenceCounterForEachMenber_CR)
    d.addWorks( Character.CharacterCounterForEachMenber_CR,
                Wordcloud.WordcloudForChatRoom)
    d.doWorks()
    d.tryFailedWorksAgain()
    pass