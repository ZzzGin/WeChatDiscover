import sys 
import os
sys.path.append(os.path.abspath('./src')) 
from DbManager import DbManager 
from Executor import Discoverer
from Analysis import Wordcloud

dbm = DbManager("D:/WeChatDiscover/Documents", "8087586da2b75fedcfbcfd0e7662ad1a", True)
dbm.update("119哈哈群")
history = dbm.mergeAllTrunksToTuple()
friendList = dbm.getFrindList()

disc = Discoverer()
disc.data = history
disc.cache["friendList"] = friendList
disc.addWork(Wordcloud.WordcloudForChatRoom)
disc.doWorks()
