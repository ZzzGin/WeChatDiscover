from Errors import AddWorkError, CacheKeyError
from Clocked_Deco import clock
import sys
import logging
import inspect
import os

class Discoverer:
    def __init__(self):
        self.works = []
        self.failedWorks = []
        self.data = ()
        self.cache = Cache()

        # Setting logger
        self.logger = logging.getLogger("WeChatDiscover")
        formatter = logging.Formatter('%(message)s')
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

        # Create a folder for pipline output
        try:
            abs_path = os.path.abspath((inspect.stack()[1])[1])
        except:
            abs_path = __file__
        directoryOfCaller = os.path.dirname(abs_path)
        filenameOfCaller = os.path.basename(abs_path)
        newFolder = directoryOfCaller + "\\" + "".join(filenameOfCaller.split(".")[:-1])
        if not os.path.exists(newFolder):
            os.makedirs(newFolder)
            self.logger.info("[Info] '" + newFolder + "' created for output.")
        else:
            self.logger.info("[Info] '" + newFolder + "' already created.")
        self.cache["outputFolder"] = newFolder

        
    
    def addWork(self, w):
        if w.__code__.co_argcount < 3:
            raise AddWorkError(" > AddWorkError: The variables of the analysis function should be ('historyData', 'cache', 'logger')")
        if w.__code__.co_varnames[:3] == ("historyData", "cache", "logger"):
            self.works.append(clock(w, self.logger))
            self.logger.info('[Info] ' + w.__name__ + " added.")
        else:
            raise AddWorkError(" > AddWorkError: The variables of the analysis function should be ('historyData', 'cache', 'logger')")
    
    def addWorks(self, *ws):
        for w in ws:
            self.addWork(w)
    
    def doWorks(self):
        for work in self.works:
            result = work(self.data, self.cache, self.logger)
            if result == False:
                self.failedWorks.append(work)
    
    def tryFailedWorksAgain(self):
        fws = []
        for failedWork in self.failedWorks:
            result = failedWork(self.data, self.cache, self.logger)
            if result == False:
                fws.append(failedWork)
        self.failedWorks = fws

    def addFileForLogger(self, fd):
        file_handler = logging.FileHandler(fd)
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

class Cache(dict):
    def __getitem__(self, key):
        try:
            return super(Cache, self).__getitem__(key)
        except KeyError:
            raise CacheKeyError(" > CacheKeyError: '"+ key +"'. This work will be added to Discoverer.failedWorks. Run tryFailedWorksAgain() to avoid sequence error.")

if __name__ == "__main__":
    def work1(historyData, cache, logger):
        logger.info("Doing work 1.")

    def work2(historyData, cache, logger):
        logger.info("Doing work 2.")

    def work3(historyData, cache, logger):
        logger.info("Doing work 3.")    

    d = Discoverer()
    d.addFileForLogger('test123123.log')
    d.addWork(work1)
    d.addWorks(work2, work3)
    d.doWorks()
    d.tryFailedWorksAgain()
    pass