import sqlite3
import isbnlib
import datetime

class Item:

    def __init__(self, owner=None, typeo=None, title=None, uniqid=None, artist=None, genre=None, year=None, isOld=None):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        if isOld==1:
            cursor.execute("select * from items where owner=? and title=?",(owner,title))
            data=cursor.fetchall()
            itemi=data[0]
            self.item_id=itemi[0]
            self.owner=itemi[1]
            self.type=itemi[2]
            self.title=title
            self.artist=itemi[5]
            self.genre=itemi[6]
            self.year=itemi[7]
            self.location=itemi[8]
            self.rating=itemi[9]
            self.view_at=itemi[10]
            self.detail_at=itemi[11]
            self.borrow_at=itemi[12]
            self.comment_at=itemi[13]
            self.search_at=itemi[14]
            self.rating_number=0
            pass
            return
        self.location = ""
        self.rating = 0
        self.rating_number = 0
        self.owner = owner
        self.comment_at = 1
        self.view_at = 1
        self.detail_at = 1
        self.borrow_at = 1
        self.search_at = 1
        self.type = typeo
        self.title = title
        self.artist=artist
        self.year=None
        if uniqid != None:
            try:
                book_metadata = isbnlib.meta(uniqid, service='default', cache='default')
                self.artist = book_metadata['Authors'][0]
                self.year = int(book_metadata['Year'])
                self.title = book_metadata['Title']
            except Exception as e:
                pass
        cursor.execute("insert into items(owner,type,title,uniqid,artist,genre,year,location,rate,view,detail\
				,borrow,comment,search) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?\
			)", (owner, typeo, self.title, uniqid, self.artist, genre, self.year, self.location, 0, 1, 1, 1, 1, 1))
        self.item_id = int(cursor.lastrowid)
        db.commit()
        db.close()

    def borrowedreq(self, user):
        "user is mail form."
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        if self.can_look_at_it(user, "borrow"):
            cursor.execute("select *from itemrequests where (item_id=? and user_email=?)", (int(self.item_id), user))
            count = 0
            for x in cursor:
                count += 1
            #daha onceden req. atmadıysa.
            if count == 0:
                #
                request_date = datetime.date.today()
                cursor.execute("insert into itemrequests(item_id,user_email,request_date) values(?,?,?)",
                               (self.item_id, user, request_date))
                cursor.execute("select * from itemrequests where item_id=?" \
                               , (self.item_id,))
                order = 0
                for x in cursor:
                    order += 1
                db.commit()
                db.close()
                return "A borrow request for item: " + self.title + " successfully created for " + user + " and order is " + str(
                        order) + "."
            else:
                db.close()
                return "You have already made a request."
        # else:
        # print("You cannot borrow.")
        db.close()

    def comment(self, user, comment_text):
        "user is email form."
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        stri="comment error"
        notifs=[]
        if self.can_look_at_it(user, "comment"):
            time_date_str = datetime.date.today()
            cursor = db.cursor()
            cursor.execute("insert into comments(item_id,user_email,comment_text,comment_date) values(?,?,?,?)",
                           (self.item_id, user, comment_text, time_date_str))
            stri="User:" + user + " had a comment about the item:" + self.title + " \"" + comment_text + "\""
            # For watch method:
            notifs=[]
            cursor.execute("select user_email from watch where (item_id=? and type=?)", (self.item_id, 0))
            for user_email in cursor:
                if (user_email != user):
                    notification_text = "Notification to " + user_email + " : " + user + "commented to " + self.title;
                    notifs.append(notification_text)
                    notification_type = 0;  # comment
                    cursor.execute(
                        "insert into notifications(user_email,notification_text,notification_type) values(?,?,?)",
                        (user_email, notification_text, notification_type))
                    db.commit()
        db.close()
        return (stri,notifs)

    def borrowedby(self, user, returndate):
        "user is mail form."
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("select * from itemrequests where (item_id=? and user_email=?)", (int(self.item_id), user))
        data = cursor.fetchall()
        #req atmıs mı
        stri="cannot borrow"
        notifs=[]
        if data:
            print("fetched")
            cursor.execute("select is_returned,user_email from itemborrows where (item_id=?)", (int(self.item_id),))
            for x in cursor:
                if x[0] == 0:
                    return "It is already borrowed by "+x[1]+"."
            taking_time = datetime.date.today()
            returned_time = taking_time + datetime.timedelta(weeks=int(returndate))
            cursor.execute("insert into itemborrows(item_id,user_email,return_date,taking_date,rate,is_returned)\
										values(?,?,?,?,?,?)",
                           (int(self.item_id), user, returned_time, taking_time, 0, 0))
            cursor.execute("select user_email from watch where (item_id=? and type=?)", (int(self.item_id), 1))
            notifs=[]
            for user_email in cursor:
                if (user != user_email):
                    notification_text = "Notification to " + user_email + " : "+ user +"borrowed "+self.title
                    notifs.append(notification_text)
                    notification_type = 1;  # borrow
                    cursor.execute("insert into notifications(user_email,notification_text,notification_type) values(?,?,?)\
						", user_email, notification_text, notification_type)
            db.commit()
            stri= "The user:" + user + " borrowed the item:" + self.title + " until " + returned_time.strftime("%d-%b-%Y") + "."
        db.close()
        return(stri,notifs)
    # returned olunca is_returned = 1.
    def returned(location=None):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("update itemborrows set is_returned=? where item_id=?", (1, self.item_id))
        cursor.execute("update items set location=? where item_id=?", (location, self.item_id))
        cursor.execute("select user_email from watch where (item_id=? and type=?)", (self.item_id, 1))
        stri="The item titled with "+self.title+" was returned"
        notifs=[]
        for user_email in cursor:
            notification_text = "Notification to " + user_email +" : The item titled with"+ self.title +"is returned."
            # print
            notifs.append(notification_text)
            # print
            notification_type = 1  # borrow
            cursor.execute("insert into notifications(user_email,notification_text,notification_type) values(?,?,?)\
			", user_email, notification_text, notification_type)
        """ bunu tam anlamadım :D """
        db.close()
        return (stri,notifs)
    def listcomments(self):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor = db.cursor()
        cursor.execute("select user_email,comment_text from comments where item_id=?", (self.item_id,))
        comment_user_list = []
        for x in cursor:
            comment_user_list.append(x)
        return comment_user_list
        db.close()

    def rate(self, user, rating):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("select *from itemborrows where (item_id=? and user_email=?)", (self.item_id, user))
        count = 0
        for x in cursor:
            count += 1
        if count > 0:
            cursor.execute("select *from itemborrows where (item_id=? and user_email=? and rate=?)",
                           (self.item_id, user, 0))
            count = 0
            for x in cursor:
                count += 1
            if count > 0:
                cursor.execute("update itemborrows set rate=? where (item_id=? and user_email=?)",
                               (rating, self.item_id, user))
                db.commit()
                db.close()
                return user + " rate the item: " + self.title + " and its rate is:" + str(rating) + "."
        return "You cannot rate before borrow"

    def getrating(self):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("select rate from itemborrows where (item_id=? and rate!=?)", (self.item_id, 0))
        for x in cursor:
            self.rating += x[0]
            self.rating_number += 1
        if self.rating != 0:
            overall_rating = self.rating / self.rating_number;
        else:
            overall_rating = 0
        db.close()
        return (overall_rating, self.rating_number)

    def locate(self, location):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("update items set location=? where item_id=?", (location, self.item_id))
        return "The item's location has changed to location:" + location + "."
        db.commit()
        db.close()

    def setstate(self, state_type, state):
        db = sqlite3.connect("database.db")
        """ state type = view,comment,search,borrow,detail
            state = closed,everyone,friends,close friends
        """
        notifs=[]
        cursor = db.cursor()
        cursor.execute("select * from watchers_for_addings where watched=?", (self.owner,))
        data = cursor.fetchall()

        state_id = 0
        if state == "closed":
            state_id = 0
            self.obje_set_state(state_type, 0)
        elif state == "everyone":
            state_id = 3
            self.obje_set_state(state_type, 3)
        elif state == "friends":
            state_id = 1
            self.obje_set_state(state_type, 1)
        elif state == "closefriends":
            state_id = 2
            self.obje_set_state(state_type, 2)

        cursor.execute("select " + state_type + " from items where item_id=?", (self.item_id,))
        for x in cursor:
            old_state_id = x
        if old_state_id == 0:
            old_state = "closed"
        elif old_state_id == 1:
            old_state = "everyone"
        elif old_state_id == 2:
            old_state = "friends"
        else:
            old_state = "close friends"
        # if old_state == state:
        # print("Item's state is already "+old_state)
        # else:
        stri="The item's state:"+ state_type + " has changed from "+old_state+" to "+ state+"."
        cursor.execute("update items set " + state_type + "=? where item_id=?", (state_id, self.item_id))
        db.commit()
        db.close()
        return(stri,notifs)

    #  0 -> close degiller
    #  1 -> 1. 2.ye close
    #  2 -> 2. 1.ye close
    #  3 -> birbirine close
    def watch(self,user, watch_method):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        stri="You cannot watch this item."
        friend=0
        close=0
        cursor.execute("select isClose from friendships where (User1=? and User2=?)",(user, self.owner))
        data1=cursor.fetchall()
        cursor.execute("select isClose from friendships where (User2=? and User1=?)",(user, self.owner))
        data2=cursor.fetchall()
        if data1 or data2:
            friend=1
        if data1:
            if data1[0][0]==2 or data1[0][0]==3:
                close=1
        if data2:
            if data2[0][0]==1 or data2[0][0]==3:
                close=1
        if watch_method=="borrow":
            if self.borrow_at==1 and friend:
                cursor.execute("insert into watch values(?,?,?)",(user,self.item_id,watch_method))
                db.commit()
                stri="You started to watch this item."
            elif self.borrow_at==2 and close:
                cursor.execute("insert into watch values(?,?,?)",(user,self.item_id,watch_method))
                db.commit()
                stri="You started to watch this item."
            elif self.borrow_at==3:
                cursor.execute("insert into watch values(?,?,?)",(user,self.item_id,watch_method))
                db.commit()
                stri="You started to watch this item."
        elif watch_method=="detail":
            if self.detail_at==1 and friend:
                cursor.execute("insert into watch values(?,?,?)",(user,self.item_id,watch_method))
                db.commit()
                stri="You started to watch this item."
            elif self.detail_at==2 and close:
                cursor.execute("insert into watch values(?,?,?)",(user,self.item_id,watch_method))
                db.commit()
                stri="You started to watch this item."
            elif self.detail_at==3:
                cursor.execute("insert into watch values(?,?,?)",(user,self.item_id,watch_method))
                db.commit()
                stri="You started to watch this item."
        db.close()
        return stri

    def annouence(self,typee, msg):
        print(msg)
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        receivcers=[]
        announcelist=[]
        if typee=="friend":
            cursor.execute("select User2,User1 from friendships where User1=?",(self.owner,))
            data1=cursor.fetchall()
            cursor.execute("select User1,User2 from friendships where User2=?",(self.owner,))
            data2=cursor.fetchall()
            receivcers=data1+data2
        elif typee=="closefriend":
            cursor.execute("select User2,User1 from friendships where User1=? and (isClose==1 or isClose=3)",(self.owner,))
            data1=cursor.fetchall()
            cursor.execute("select User1,User2 from friendships where User2=? and (isClose==2 or isClose=3)",(self.owner,))
            data2=cursor.fetchall()
            receivcers=data1+data2
        for i in receivcers:
            announcelist.append("Announce to " + i[0] + " from " + self.owner + " that: " + msg)
        stri=self.owner + " announce a message: " + msg
        db.close()
        return (stri,announcelist)

    def can_look_at_it(self, user, comment_borrow):
        """ """
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        close = False
        friendship = False
        cursor.execute("select *from friendships where\
			(User1=? and User2=? and isClose=?)\
			 or \
			(User2=? and User1=? and isClose=?)", (self.owner, user, 1, self.owner, user, 2))
        count = 0
        for x in cursor:
            count += 1
        if count != 0:
            close = True
        cursor.execute("select * from friendships where \
			((User1=? and User2=?) \
			or \
			(User1=? and User2=?))", \
                       (self.owner, user, user, self.owner))
        count = 0
        for x in cursor:
            count += 1
        if count != 0:
            friendship = True
        if comment_borrow == "comment":
            if self.comment_at == 0:
                return False
            elif self.comment_at == 1:
                if friendship:
                    return True
                else:
                    return False
            if self.comment_at == 2:
                if close:
                    return True
                else:
                    return False
            else:  # everyone
                return True
        else:
            if self.borrow_at == 0:
                return False
            elif self.borrow_at == 1:
                if friendship:
                    return True
                else:
                    return False
            if self.borrow_at == 2:
                if close:
                    return True
                else:
                    return False
            else:  # everyone
                return True
        db.close()

    def obje_set_state(self, state_type, no):
        if (state_type == "comment"):
            self.comment_at = no
        elif (state_type == "search"):
            self.search_at = no
        elif (state_type == "borrow"):
            self.borrow_at = no
        elif (state_type == "detail"):
            self.detail_at = no
        else:
            self.view_at = no

    def search(self, user, searchText, genre, year, forborrow=False):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        words = searchText.split(" ")
        years = year.split(":")
        datas1 = []
        datas2 = []
        datas3 = []
        datas4 = []
        for i in words:
            like_string = "%" + i + "%"
            if len(years) == 2:
                cursor.execute(
                    "select owner, search, borrow,title from items where title like ? and genre=? and year>=? and year<=?",
                    (like_string, genre, years[0], years[1],))
                willappend = cursor.fetchall()
                datas1.append(willappend)
                cursor.execute(
                    "select owner, search, borrow, title from items where artist like ? and genre=? and year>=? and year<=?",
                    (like_string, genre, int(years[0]), int(years[1]),))
                willappend = cursor.fetchall()
                datas2.append(willappend)
            else:
                cursor.execute(
                    "select owner, search, borrow,title from items where title like ? and genre=? and year=?",
                    (like_string, genre, years[0],))
                willappend = cursor.fetchall()
                datas1.append(willappend)
                cursor.execute(
                    "select owner, search, borrow, title from items where artist like ? and genre=? and year=?",
                    (like_string, genre, years[0],))
                willappend = cursor.fetchall()
                datas2.append(willappend)
        for b in datas1[0]:
            boole = True
            for c in datas1[1:]:
                if not (b in c):
                    boole = False
                    break
            if boole:
                datas3.append(b)

        for d in datas2[0]:
            boole = True
            for e in datas2[1:]:
                if not (d in e):
                    boole = False
                    break
            if boole:
                datas4.append(d)

        returning_datas = []

        merged = list(set(datas3) - set(datas4)) + list(set(datas4) - set(datas3))

        for m in merged:
            if not (forborrow):
                if m[1] == 0:
                    continue
                elif m[1] == 1:
                    cursor.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",
                                   (m[0], user, user, m[0],))
                    isTheyFriend = cursor.fetchall()
                    if isTheyFriend:
                        returning_datas.append([m[0], m[3]])
                elif m[1] == 2:
                    cursor.execute(
                        "Select * from friendships where (User1=? and User2=? and (isClose=1 or isClose=3)) or (User1=? and User2=? and (isClose=2 or isClose=3))",
                        (m[0], user, user, m[0]))
                    isSelfClose = cursor.fetchall()
                    if isSelfClose:
                        returning_datas.append([m[0], m[3]])
                else:
                    returning_datas.append([m[0], m[3]])
            if forborrow:
                if m[2] == 0:
                    continue
                elif m[2] == 1:
                    cursor.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",
                                   (m[0], user, user, m[0],))
                    isTheyFriend = cursor.fetchall()
                    if isTheyFriend:
                        returning_datas.append([m[0], m[3]])
                elif m[2] == 2:
                    cursor.execute(
                        "Select * from friendships where (User1=? and User2=? and (isClose=1 or isClose=3)) or (User1=? and User2=? and (isClose=2 or isClose=3))",
                        (m[0], user, user, m[0]))
                    isSelfClose = cursor.fetchall()
                    if isSelfClose:
                        returning_datas.append([m[0], m[3]])
                else:
                    returning_datas.append([m[0], m[3]])

        return returning_datas

    def view(self,user):
        return "Title: " + str(self.title) + ", Artist: " + str(self.artist) + ", Year: " + str(self.year)

    def detail(self,user):
        "user email form."
        if self.owner == user:
            return "Title: " + str(self.title) + ", Artist: " + str(self.artist) + ", Year: " + str(self.year)  + ", Owner: " + self.owner + ", Location: " + str(self.location)
        else:
            return "Title: " + str(self.title) + ", Artist: " + str(self.artist) + ", Year: " + str(self.year) + ", Owner: " + self.owner

    def delete(self):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("delete from items where title=? and owner=?", (self.title, self.owner))
        db.commit()
        stri=self.title + "deleted by "+self.owner
        db.commit()
        return stri
