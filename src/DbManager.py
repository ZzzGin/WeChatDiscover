from hashlib import md5
import sqlite3
import datetime
import collections
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
        ContactCursor = self.__ContactConn.cursor()
        ContactCursor.execute('SELECT "dbContactRemark","userName" FROM "main"."Friend"')
        friendListFromDb = ContactCursor.fetchall()
        friendList = [(f[0].decode("utf-8"), f[1]) for f in friendListFromDb]
        foundFromDb = []
        for f in friendList:
            if name in f[0]:
                foundFromDb.append(f[1])
        userOrChatRoomFound = []
        for f in foundFromDb:
            if f.endswith("@chatroom")==self.__isChatRoom:
                userOrChatRoomFound.append(f)
        if len(userOrChatRoomFound)==0:
            raise UserNameQueryError("Can not find user/chatroom whose WeChatID, UserName, Alias, Pinyin of Alias similar to '" + name + "'")
        elif len(userOrChatRoomFound)>1:
            el = [e for e in userOrChatRoomFound]
            raise UserNameQueryError("More than one user/chatroom similar to '" + name + "' are found: " + str(el))
        
        MessageCursor = self.__MessageConn.cursor()
        m = md5()
        m.update(userOrChatRoomFound[0].encode('utf-8'))
        userMd5 = m.hexdigest()
        MessageCursor.execute('SELECT * FROM "chat_' + userMd5 + '"')
        dataQueried = MessageCursor.fetchall()
        if len(dataQueried) > 0:
            self.__dataTrunk.append(dataQueried)
            self.dataTrunkInfo.append((self.__dataTrunkCounter, name, len(dataQueried), userOrChatRoomFound[0]))
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




if __name__ == "__main__":
    dbManager = DbManager("D:/WeChatDiscover/Documents", "8087586da2b75fedcfbcfd0e7662ad1a", True)
    dbManager.updateFromList(["GitNote交流群", "shuniu"])
    print(dbManager.dataTrunkInfo)
    t1 = dbManager.mergeAllTrunksToTuple()
    print(len(t1))
    t2 = dbManager.mergeSelectedTrunksToTuple(0)
    print(len(t2))
    pass