import sys 
import os
sys.path.append(os.path.abspath('./src')) 
from DbManager import DbManager 
from Executor import Discoverer
from Analysis import Wordcloud, Middlewares

queryName = "17年雪城大学新生群"
dbm = DbManager("D:/WeChatDiscover/Documents", "8087586da2b75fedcfbcfd0e7662ad1a", True)
dbm.update(queryName)
history = dbm.mergeAllTrunksToTuple()
friendList = dbm.getFrindList()

disc = Discoverer()
disc.addFileForLogger()
disc.data = history
disc.cache["friendList"] = friendList
disc.cache["groupName"] = queryName
# disc.addWork(Wordcloud.WordcloudForChatRoom)
# disc.addWorks(  Middlewares.textMessagesSplitedByIdInGroupChat,
#                 Wordcloud.WordcloudForEachMembersInChatRoom)
disc.doWorks()
pass