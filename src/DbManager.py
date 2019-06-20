from hashlib import md5
import sqlite3
import datetime
import collections
import string
from Errors import UserNameQueryError

class DbManager:
    def __init__(self, documentRoot, accountMD5, isChatRoom=False):
        self.__documentRoot = documentRoot
        self.__accountMD5 = accountMD5
        self.__isChatRoom = isChatRoom
        self.__dataTrunk = []
        self.dataTrunkInfo = []
        self.__dataTrunkCounter = 0
        self.__dataLength = 0
        self.__ContactConn = sqlite3.connect(self.__documentRoot+"/"+self.__accountMD5+"/DB/WCDB_Contact.sqlite")
        self.__MessageConn = sqlite3.connect(self.__documentRoot+"/"+self.__accountMD5+"/DB/MM.sqlite")
        self.__nameIdMap = []
        
    def mergeAllTrunksToTuple(self):
        o = ()
        for tup in self.__dataTrunk:
            o += tuple(tup)
        return o
    
    def mergeSelectedTrunksToTuple(self, *indexes):
        o = ()
        for i in indexes:
            o += tuple(self.__dataTrunk[i])
        return o
    
    def update(self, name):
        if self.__nameIdMap == []:
            ContactCursor = self.__ContactConn.cursor()
            ContactCursor.execute('SELECT "dbContactRemark","userName" FROM "main"."Friend"')
            friendListFromDb = ContactCursor.fetchall()
            friendList = [(f[0].decode("utf-8"), f[1]) for f in friendListFromDb]
            self.__nameIdMap = friendList
        foundFromDb = []
        for f in self.__nameIdMap:
            if name in f[0]:
                foundFromDb.append(f[1])
        userOrChatRoomFound = []
        for f in foundFromDb:
            if f.endswith("@chatroom")==self.__isChatRoom:
                userOrChatRoomFound.append(f)
        if len(userOrChatRoomFound)==0:
            raise UserNameQueryError(" > UserNameQueryError: Can not find user/chatroom whose WeChatID, UserName, Alias, Pinyin of Alias similar to '" + name + "'")
        elif len(userOrChatRoomFound)>1:
            fil = self.getFrindList()
            el = [e + ": " + fil[e] for e in userOrChatRoomFound]
            raise UserNameQueryError(" > UserNameQueryError: More than one user/chatroom similar to '" + name + "' are found: " + str(el))
        self.updateById(userOrChatRoomFound[0], name)
    
    def updateById(self, weChatId, name):
        MessageCursor = self.__MessageConn.cursor()
        m = md5()
        m.update(weChatId.encode('utf-8'))
        userMd5 = m.hexdigest()
        MessageCursor.execute('SELECT * FROM "chat_' + userMd5 + '"')
        dataQueried = MessageCursor.fetchall()
        if len(dataQueried) > 0:
            self.__dataTrunk.append(dataQueried)
            self.dataTrunkInfo.append((self.__dataTrunkCounter, name, len(dataQueried), weChatId))
            self.__dataTrunkCounter += 1
            self.__dataLength += len(dataQueried)
        
    def updateFromList(self, nameList):
        el = ""
        for n in nameList:
            try:
                self.update(n)
            except UserNameQueryError as ve:
                el += (ve.message+"\n")
        if el!="":
            raise UserNameQueryError(el)

    def getFrindList(self):
        return {f[1]: f[0].split("\x00")[0][2:].split("\x12")[0] for f in self.__nameIdMap}


if __name__ == "__main__":
    dbManager = DbManager("D:/WeChatDiscover/Documents", "8087586da2b75fedcfbcfd0e7662ad1a", True)
    dbManager.updateFromList(["GitNote交流群", "shuniu"])
    print(dbManager.dataTrunkInfo)
    t1 = dbManager.mergeAllTrunksToTuple()
    print(len(t1))
    t2 = dbManager.mergeSelectedTrunksToTuple(0)
    print(len(t2))
    tfl = dbManager.getFrindList()
    print(len(tfl))

    dbManager = DbManager("D:/WeChatDiscover/Documents", "8087586da2b75fedcfbcfd0e7662ad1a", False)
    dbManager.updateFromList(["xuanshihua", "wanghui"])
    print(dbManager.dataTrunkInfo)
    t1 = dbManager.mergeAllTrunksToTuple()
    print(len(t1))
    t2 = dbManager.mergeSelectedTrunksToTuple(0)
    print(len(t2))
    tfl = dbManager.getFrindList()
    print(len(tfl))
    pass