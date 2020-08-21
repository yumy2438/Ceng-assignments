import random
import sqlite3
import isbnlib
import datetime


class User:
    def __init__(self, email, namesurname=None, password=None):
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        usersDB.execute("Select * from user_main_infos where email=(?)", (email,))
        data = usersDB.fetchall()
        if not (data):
            self.email = email
            self.namesurname = namesurname
            self.password = password
            self.isVerified = 0
            self.verificationNumber = 111111
            usersDB.execute("""INSERT INTO user_main_infos VALUES(?, ?, ?, ?, ?)""",
                            (self.email, self.namesurname, self.password, self.isVerified, self.verificationNumber))
            vt.commit()
        else:
            self.email = data[0][0]
            self.namesurname = data[0][1]
            self.password = data[0][2]
            self.isVerified = data[0][3]
            self.verificationNumber = data[0][4]
        vt.close()

    @staticmethod
    def verify(email, verification):
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        usersDB.execute("Select verificationNumber, isActive from user_main_infos where email=?", (email,))
        data = usersDB.fetchall()
        actualVerificationNumber = data[0][0]
        if data[0][1]:
            vt.close()
            return "Your account have already been verified."
        elif str(actualVerificationNumber) == verification:
            usersDB.execute("UPDATE user_main_infos SET isActive=1 where email=?", (email,))
            vt.commit()
            vt.close()
            return "Your account successfully verified."
        else:
            vt.close()
            return "Verification number is false."
        vt.close()

    def changepassword(self, newpassword, oldpassword):
        print(newpassword, oldpassword)
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        if oldpassword == None:
            self.password = random.randint(100000, 999999)
            usersDB.execute("UPDATE user_main_infos SET password=? where email=?", (self.password, self.email,))
            vt.commit()
            vt.close()
            return "Your temporay password have been set to " + self.password
        else:
            if oldpassword == self.password:
                self.password = newpassword
                usersDB.execute("UPDATE user_main_infos SET password=? where email=?", (newpassword, self.email,))
                vt.commit()
                vt.close()
                return "Your password have been changed."
            else:
                vt.close()
                return "Your old password is false."
        vt.close()

    def lookup(self, emaillist):
        emaillist = emaillist.strip('][').split(',')
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        liste = []
        for i in emaillist:
            usersDB.execute("Select email from user_main_infos where email=?", (i,))
            data = usersDB.fetchall()
            if data:
                liste.append(i)
        vt.close()
        return liste
    def friend(self, email):
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        usersDB.execute("Select email from user_main_infos where email=?", (email,))
        data = usersDB.fetchall()
        if data:
            usersDB.execute("Select * from friendship_requests where fromUser=? and toUser=?", (self.email, email,))
            data2 = usersDB.fetchall()
            usersDB.execute("Select * from friendship_requests where fromUser=? and toUser=?", (email, self.email,))
            data3 = usersDB.fetchall()
            usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",
                            (email, self.email, self.email, email,))
            data4 = usersDB.fetchall()
            if not (data2) and not (data3) and not (data4):
                usersDB.execute("insert into friendship_requests VALUES(?,?)", (email, self.email,))
                vt.commit()
                return "You have successfully sent friendship request to this user!"
        vt.close()

    def setfriend(self, user, state):
        """user is email."""
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        if state == "notfriend":
            usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",
                            (user, self.email, self.email, user,))
            data = usersDB.fetchall()
            usersDB.execute(
                "Select * from friendship_requests where (fromUser=? and toUser=?) or (fromUser=? and toUser=?)",
                (user, self.email, self.email, user,))
            data2 = usersDB.fetchall()
            if data:
                usersDB.execute("delete from friendships where (User1=? and User2=?) or (User1=? and User2=?)",
                                (user, self.email, self.email, user,))
                vt.commit()
                vt.close()
                return "You have successfully unfriended " + user
            elif data2:
                usersDB.execute(
                    "delete from friendship_requests where (fromUser=? and toUser=?) or (fromUser=? and toUser=?)",
                    (user, self.email, self.email, user,))
                vt.commit()
                vt.close()
                return "You have successfully refused friendship request from " + user
        elif state == "friend":
            usersDB.execute("Select * from friendships where (User1=? and User2=?)", (self.email, user,))
            data = usersDB.fetchall()
            usersDB.execute("Select * from friendships where (User2=? and User1=?)", (self.email, user,))
            data2 = usersDB.fetchall()
            usersDB.execute("Select * from friendship_requests where (fromUser=? and toUser=?)",
                            (self.email, user,))
            data3 = usersDB.fetchall()
            usersDB.execute("Select * from friendship_requests where (toUser=? and fromUser=?)",
                            (self.email, user,))
            data4 = usersDB.fetchall()
            if data:
                if data[0][2] == 1:
                    usersDB.execute("UPDATE friendships SET isClose=0 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully change friendship status with " + user + " from close friend to normal friend."
                elif data[0][2] == 3:
                    usersDB.execute("UPDATE friendships SET isClose=2 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully change friendship status with " + user + " from close friend to normal friend."
            elif data2:
                if data2[0][2] == 2:
                    usersDB.execute("UPDATE friendships SET isClose=0 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully change friendship status with " + user + " from close friend to normal friend."
                elif data2[0][2] == 3:
                    usersDB.execute("UPDATE friendships SET isClose=1 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully change friendship status with " + user + " from close friend to normal friend."
            elif data3:
                usersDB.execute("insert into friendships VALUES(?,?,?)", (self.email, user, 0,))
                vt.commit()
                usersDB.execute("delete from friendship_requests where (fromUser=? and toUser=?)",
                                (self.email, user,))
                vt.commit()
                vt.close()
                return "You have successfully accepted friendship request from " + user
            elif data4:
                usersDB.execute("insert into friendships VALUES(?,?,?)", (self.email, user, 0,))
                vt.commit()
                usersDB.execute("delete from friendship_requests where (toUser=? and fromUser=?)",
                                (self.email, user,))
                vt.commit()
                vt.close()
                return "You have successfully accepted friendship request from " + user
        else:
            usersDB.execute("Select * from friendships where (User1=? and User2=?)", (self.email, user,))
            data = usersDB.fetchall()
            usersDB.execute("Select * from friendships where (User2=? and User1=?)", (self.email, user,))
            data2 = usersDB.fetchall()
            if data:
                if data[0][2] == 0:
                    usersDB.execute("UPDATE friendships SET isClose=1 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully changed friendship status with " + user + " from normal friend to close friend."
                elif data[0][2] == 2:
                    usersDB.execute("UPDATE friendships SET isClose=3 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully changed friendship status with " + user + " from normal friend to close friend."
            elif data2:
                if data2[0][2] == 0:
                    usersDB.execute("UPDATE friendships SET isClose=2 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully change friendship status with " + user + " from normal friend to close friend."
                elif data2[0][2] == 1:
                    usersDB.execute("UPDATE friendships SET isClose=3 where (User1=? and User2=?)",
                                    (self.email, user,))
                    vt.commit()
                    vt.close()
                    return "You have successfully change friendship status with " + user + " from normal friend to close friend."
        vt.close()

    def itemlist(self, user):
        """user is mail."""
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        usersDB.execute("select title, view from items where owner=?", (user,))
        data = usersDB.fetchall()
        usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",
                        (user, self.email, self.email, user,))
        isTheyFriend = usersDB.fetchall()
        usersDB.execute(
            "Select * from friendships where (User1=? and User2=? and (isClose=1 or isClose=3)) or (User1=? and User2=? and (isClose=2 or isClose=3))",
            (user, self.email, self.email, user))
        isSelfClose = usersDB.fetchall()
        liste = []
        for i in data:
            if i[1] == 0:
                continue
            elif i[1] == 3:
                liste.append(i[0])
            elif i[1] == 1 and isTheyFriend:
                liste.append(i[0])
            elif i[1] == 2 and isSelfClose:
                liste.append(i[0])
            else:
                continue
        vt.close()
        return liste

    def watch(self, user, mode):
        """user is mail"""
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",
                        (user, self.email, self.email, user,))
        data = usersDB.fetchall()
        if not (data):
            vt.commit()
            vt.close()
            return "You cannot watch " + user + " because you are not friend."
        elif mode != None:
            usersDB.execute("insert into watchers_for_addings values(?,?,?)", (self.email, user, mode))
            vt.commit()
            vt.close()
            return self.namesurname + " has started to watch " + user + " for new item addings with mode " + mode + "."
        else:
            usersDB.execute("delete from watchers_for_addings where watcher=? and watched=?", (self.email, user,))
            vt.commit()
            vt.close()
            return self.namesurname + " has ended watching " + user + " for new item addings."


    def isthererequestfrom(self, toUser, fromUser):
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        usersDB.execute("select * from friendship_requests where toUser=? and fromUser=?", (fromUser, toUser))
        data = usersDB.fetchall()
        if data:
            vt.commit()
            vt.close()
            return "t"
        vt.close()
        return "f"

    def isthereuser(self,user):
        vt = sqlite3.connect('database.db')
        usersDB = vt.cursor()
        usersDB.execute("select * from user_main_infos where email=?", (user,))
        data = usersDB.fetchall()
        if data:
            vt.commit()
            vt.close()
            return "t"
        vt.close()
        return "f"