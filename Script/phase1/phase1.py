import random
import sqlite3
import isbnlib
import datetime


class User:
	def __init__(self, email, namesurname, password):
		vt=sqlite3.connect('test.sqlite')
		usersDB = vt.cursor()
		usersDB.execute("Select * from user_main_infos where email=(?)",(email,))
		data=usersDB.fetchall()
		if not(data):
			print("New user have been added!")
			self.email=email
			self.namesurname=namesurname
			self.password=password
			self.isVerified=0
			self.verificationNumber=random.randint(100000,999999)
			print("Your account is need to be verified and verification number is: " + str(self.verificationNumber))
			usersDB.execute("""INSERT INTO user_main_infos VALUES(?, ?, ?, ?, ?)""",(self.email, self.namesurname, self.password, self.isVerified, self.verificationNumber))
			vt.commit()
		else:
			self.email=data[0][0]
			self.namesurname=data[0][1]
			self.password=data[0][2]
			self.isVerified=data[0][3]
			self.verificationNumber=data[0][4]
		vt.close()
	@staticmethod
	def verify(email, verification):
			vt=sqlite3.connect('test.sqlite')
			usersDB = vt.cursor()
			usersDB.execute("Select verificationNumber, isActive from user_main_infos where email=?",(email,))
			data=usersDB.fetchall()
			actualVerificationNumber=data[0][0]
			if data[0][1]:
				print ("Your account have already been verified.")
			elif actualVerificationNumber==verification:
				usersDB.execute("UPDATE user_main_infos SET isActive=1 where email=?",(email,))
				vt.commit()
				print ("Your account successfully verified.")
			else:
				print ("Verification number is false.")
			vt.close()
	
	def changepassword(self, newpassword, oldpassword=None):
			vt=sqlite3.connect('test.sqlite')
			usersDB = vt.cursor()
			if oldpassword==None:
					self.password=random.randint(100000,999999)
					print ("Your temporay password have been set to " + self.password)
					usersDB.execute("UPDATE user_main_infos SET password=? where email=?",(self.password,self.email,))
					vt.commit()
			else:
					if oldpassword==self.password:
							self.password=newpassword
							usersDB.execute("UPDATE user_main_infos SET password=? where email=?",(newpassword,self.email,))
							vt.commit()
							print ("Your password have been changed.")
					else:
							print ("Your old password is false.")
			vt.close()
	def lookup(self,emaillist):
			vt=sqlite3.connect('test.sqlite')
			usersDB = vt.cursor()
			liste=[]
			for i in emaillist:
				usersDB.execute("Select email from user_main_infos where email=?",(i,))
				data=usersDB.fetchall()
				if data:
					liste.append(i)
			print (liste)
			vt.close()
	def friend(self,email):
			vt=sqlite3.connect('test.sqlite')
			usersDB = vt.cursor()
			usersDB.execute("Select email from user_main_infos where email=?",(email,))
			data=usersDB.fetchall()
			if data:
				usersDB.execute("Select * from friendship_requests where fromUser=? and toUser=?",(self.email,email,))
				data2=usersDB.fetchall()
				usersDB.execute("Select * from friendship_requests where fromUser=? and toUser=?",(email,self.email,))
				data3=usersDB.fetchall()
				usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(email,self.email,self.email,email,))
				data4=usersDB.fetchall()
				if not(data2) and not(data3) and not(data4) :
					usersDB.execute("insert into friendship_requests VALUES(?,?)",(email,self.email,))
					vt.commit()
					print("You have successfully sent friendship request to this user!")	
			vt.close()
	def setfriend(self, user, state):
			vt=sqlite3.connect('test.sqlite')
			usersDB = vt.cursor()
			if state=="notfriend":
				usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(user.email,self.email,self.email,user.email,))
				data=usersDB.fetchall()
				usersDB.execute("Select * from friendship_requests where (fromUser=? and toUser=?) or (fromUser=? and toUser=?)",(user.email,self.email,self.email,user.email,))
				data2=usersDB.fetchall()
				if data:
					usersDB.execute("delete from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(user.email,self.email,self.email,user.email,))
					vt.commit()
					print ("You have successfully unfriended " + user.namesurname)
				elif data2:
					usersDB.execute("delete from friendship_requests where (fromUser=? and toUser=?) or (fromUser=? and toUser=?)",(user.email,self.email,self.email,user.email,))
					vt.commit()
					print ("You have successfully refused friendship request from " + user.namesurname)
			elif state=="friend":
				usersDB.execute("Select * from friendships where (User1=? and User2=?)",(self.email,user.email,))
				data=usersDB.fetchall()
				usersDB.execute("Select * from friendships where (User2=? and User1=?)",(self.email,user.email,))
				data2=usersDB.fetchall()
				usersDB.execute("Select * from friendship_requests where (fromUser=? and toUser=?)",(self.email,user.email,))
				data3=usersDB.fetchall()
				usersDB.execute("Select * from friendship_requests where (toUser=? and fromUser=?)",(self.email,user.email,))
				data4=usersDB.fetchall()
				if data:
					if data[0][2]==1:
						usersDB.execute("UPDATE friendships SET isClose=0 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully change friendship status with " + user.namesurname + " from close friend to normal friend.")
					elif data[0][2]==3:
						usersDB.execute("UPDATE friendships SET isClose=2 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully change friendship status with " + user.namesurname + " from close friend to normal friend.")
				elif data2:
					if data2[0][2]==2:
						usersDB.execute("UPDATE friendships SET isClose=0 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully change friendship status with " + user.namesurname + " from close friend to normal friend.")
					elif data2[0][2]==3:
						usersDB.execute("UPDATE friendships SET isClose=1 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully change friendship status with " + user.namesurname + " from close friend to normal friend.")
				elif data3:
					usersDB.execute("insert into friendships VALUES(?,?,?)",(self.email,user.email,0,))
					vt.commit()
					usersDB.execute("delete from friendship_requests where (fromUser=? and toUser=?)",(self.email,user.email,))
					vt.commit()
					print ("You have successfully accepted friendship request from " + user.namesurname)
				elif data4:
					usersDB.execute("insert into friendships VALUES(?,?,?)",(self.email,user.email,0,))
					vt.commit()
					usersDB.execute("delete from friendship_requests where (toUser=? and fromUser=?)",(self.email,user.email,))
					vt.commit()
					print ("You have successfully accepted friendship request from " + user.namesurname)
			else:
				usersDB.execute("Select * from friendships where (User1=? and User2=?)",(self.email,user.email,))
				data=usersDB.fetchall()
				usersDB.execute("Select * from friendships where (User2=? and User1=?)",(self.email,user.email,))
				data2=usersDB.fetchall()
				if data:
					if data[0][2]==0:
						usersDB.execute("UPDATE friendships SET isClose=1 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully changed friendship status with " + user.namesurname + " from normal friend to close friend.")
					elif data[0][2]==2:
						usersDB.execute("UPDATE friendships SET isClose=3 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully changed friendship status with " + user.namesurname + " from normal friend to close friend.")
				elif data2:
					if data2[0][2]==0:
						usersDB.execute("UPDATE friendships SET isClose=2 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully change friendship status with " + user.namesurname + " from normal friend to close friend.")
					elif data2[0][2]==1:
						usersDB.execute("UPDATE friendships SET isClose=3 where (User1=? and User2=?)",(self.email,user.email,))
						vt.commit()
						print ("You have successfully change friendship status with " + user.namesurname + " from normal friend to close friend.")
			vt.close()
	def itemlist(self,user):
		vt=sqlite3.connect('test.sqlite')
		usersDB = vt.cursor()
		usersDB.execute("select title, view from items where owner=?",(user.email,))
		data=usersDB.fetchall()
		usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(user.email,self.email,self.email,user.email,))
		isTheyFriend=usersDB.fetchall()
		usersDB.execute("Select * from friendships where (User1=? and User2=? and (isClose=1 or isClose=3)) or (User1=? and User2=? and (isClose=2 or isClose=3))",(user.email,self.email,self.email,user.email))
		isSelfClose=usersDB.fetchall()
		liste=[]
		for i in data:
			if i[1]==0:
				continue
			elif i[1]==1 and isTheyFriend:
				liste.append(i[0])
			elif i[1]==2 and isSelfClose:
				liste.append(i[0])
			else:
				liste.append(i[0])
		print(liste)
		vt.close()
	def watch(self,user,mode):
				vt=sqlite3.connect('test.sqlite')
				usersDB = vt.cursor()
				usersDB.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(user.email,self.email,self.email,user.email,))
				data=usersDB.fetchall()
				if not(data):
						print("You cannot watch " + user.namesurname + " because you are not friend.")
				elif mode!=None:
						usersDB.execute("insert into watchers_for_addings values(?,?,?)",(self.email,user.email,mode))
						vt.commit()
						print(self.namesurname+ " has started to watch "+ user.namesurname+ " for new item addings with mode " + mode +".")
				else:
						usersDB.execute("delete from watchers_for_addings where watcher=? and watched=?",(self.email, user.email,))
						print(self.namesurname + " has ended watching " + user.namesurname + " for new item addings.")
				vt.close()


class Item:

	def __init__(self,owner=None,typeo=None,title=None,uniqid=None,artist=None,genre=None,year=None):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		self.location = ""
		self.rating = 0
		self.rating_number=0
		self.owner = owner
		self.comment_at = 0
		self.view_at = 0
		self.detail_at = 0
		self.borrow_at = 0
		self.search_at = 0
		self.type=typeo
		self.title=title
		if uniqid!=None:
			try:
				book_metadata=isbnlib.meta(uniqid,service='default',cache='default')
				self.artist = book_metadata['Authors'][0]
				self.year = int(book_metadata['Year'])
				self.title = book_metadata['Title']
			except Exception as e:
				pass
		cursor.execute("insert into items(owner,type,title,uniqid,artist,genre,year,location,rate,view,detail\
				,borrow,comment,search) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?\
			)",(owner,typeo,title,uniqid,artist,genre,year,self.location,0,0,0,0,0,0))
		self.item_id = int(cursor.lastrowid)
		db.commit()
		print("A new item successfully created with the name:"+self.title+" by "+owner)
		db.close()

	def borrowedreq(self,user):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		if self.can_look_at_it(user,"borrow"):
			cursor.execute("select *from itemrequests where (item_id=? and user_email=?)",(self.item_id,user.email))
			count = 0
			for x in cursor:
				count+=1
			if count == 0:
				request_date = datetime.date.today()
				cursor.execute("insert into itemrequests(item_id,user_email,request_date) values(?,?,?)",(self.item_id,user.email,request_date))
				cursor.execute("select * from itemrequests where item_id=?"\
					,(self.item_id,))
				order = 0
				for x in cursor:
					order+=1
				db.commit()
				print("A borrow request for item: "+self.title+" successfully created for "+ user.namesurname+ " and order is " + str(order) + ".")
			#else:
			#print("You cannot borrow.")
		db.close()
	def comment(self,user,comment_text):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		if self.can_look_at_it(user,"comment"):
			time_date_str = datetime.date.today()
			cursor = db.cursor()
			cursor.execute("insert into comments(item_id,user_email,comment_text,comment_date) values(?,?,?,?)",(self.item_id,user.email,comment_text,time_date_str))
			print("User:"+user.email+" had a comment about the item:"+self.title+" \""+comment_text+"\"")
			#For watch method:
			cursor.execute("select user_email from watch where (item_id=? and type=?)",(self.item_id,0))
			for user_email in cursor:
				if (user_email != user.email):
					notification_text = user_email+" commented.";
					notification_type = 0; #comment
					cursor.execute("insert into notifications(user_email,notification_text,notification_type) values(?,?,?)",(user_email,notification_text,notification_type))
			db.commit()
		#else:
		#	print("You have no right to do it.")
		db.close()

	def borrowedby(self,user,returndate):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		"""cursor.execute("select user_email from itemrequests order by request_id asc limit 1")
		if cursor.rowcount >0:
			print("sdıjfoskdfl")
			if cursor[0] == user.email:"""
		cursor.execute("select * from itemrequests where (item_id=? and user_email=?)",(self.item_id,user.email))
		count = 0
		for x in cursor:
			count+=1
		if count > 0:
			cursor.execute("select is_returned from itemborrows where (item_id=?)",(self.item_id,))
			for x in cursor:
				if x[0]==0:
					return
			taking_time = datetime.date.today()
			returned_time = taking_time+datetime.timedelta(weeks=returndate)
			cursor.execute("insert into itemborrows(item_id,user_email,return_date,taking_date,rate,is_returned)\
										values(?,?,?,?,?,?)",(self.item_id,user.email,returned_time,taking_time,0,0))
			cursor.execute("select user_email from watch where (item_id=? and type=?)",(self.item_id,1))
			for user_email in cursor:
				if(user.email != user_email):
					notification_text = user.email + " borrowed it."
					notification_type = 1;#borrow
					cursor.execute("insert into notifications(user_email,notification_text,notification_type) values(?,?,?)\
						",user_email,notification_text,notification_type)
			db.commit()
			print("The user:"+user.email+" borrowed the item:"+self.title)
		#else:
			#print("First you:"+user.email+" should make a request for the item:"+self.title)
				#else:
			#	print("You cannot give this user; since there are people in the request list befor this user.")
		#else:
		#	print("There is no user in request list for item:"+self.title)
		db.close()
	# returned olunca is_returned = 1.
	def returned(location=None):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		cursor.execute("update itemborrows set is_returned=? where item_id=?",(1,self.item_id))
		cursor.execute("update items set location=? where item_id=?",(location,self.item_id))
		cursor.execute("select user_email from watch where (item_id=? and type=?)",(self.item_id,1))
		for user_email in cursor:
			notification_text = "The item is returned."
			#print
			print(notification_text)
			#print
			notification_type = 1#borrow
			cursor.execute("insert into notifications(user_email,notification_text,notification_type) values(?,?,?)\
			",user_email,notification_text,notification_type)
		""" bunu tam anlamadım :D """
		db.close()

	def list_comments(self):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		cursor = db.cursor()
		cursor.execute("select user_email,comment_text from comments where item_id=?",(self.item_id,))
		comment_user_list = []
		for x in cursor:
			comment_user_list.append(x)
		return comment_user_list
		db.close()

	def rate(self,user,rating):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		cursor.execute("select *from itemborrows where (item_id=? and user_email=?)",(self.item_id,user.email))
		count = 0
		for x in cursor:
			count+=1
		if count>0:
			cursor.execute("select *from itemborrows where (item_id=? and user_email=? and rate=?)",(self.item_id,user.email,0))
			count = 0
			for x in cursor:
				count+=1
			if count > 0:
				cursor.execute("update itemborrows set rate=? where (item_id=? and user_email=?)",(rating,self.item_id,user.email))
				print(user.email+" rate the item: "+ self.title + " and its rate is:"+str(rating)+".")
				db.commit()
				db.close()

	def getrating(self):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		cursor.execute("select rate from itemborrows where (item_id=? and rate!=?)",(self.item_id,0))
		for x in cursor:
			self.rating+=x[0]
			self.rating_number+=1
		if self.rating != 0:
			overall_rating=self.rating/self.rating_number;		
		else:
			overall_rating = 0
		return (overall_rating,self.rating_number)
		db.close()



	def locate(self,location):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		cursor.execute("update items set location=? where item_id=?",(location,self.item_id))
		print("The item's location has changed to location:"+location+".")
		db.commit()
		db.close()

	def setstate(self,state_type,state):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		""" state type = view,comment,search,borrow,detail
			state = closed,everyone,friends,close friends
		"""
		cursor = db.cursor()
		cursor.execute("select * from watchers_for_addings where watched=?",(self.owner,))
		data=cursor.fetchall()

		state_id = 0
		if state=="closed":
			state_id = 0
			self.obje_set_state(state_type,0)
		elif state=="everyone":
			state_id = 3
			self.obje_set_state(state_type,3)
		elif state=="friends":
			state_id = 1
			self.obje_set_state(state_type,1)
		elif state =="close friends":
			state_id = 2
			self.obje_set_state(state_type,2)
		
		cursor.execute("select "+state_type+" from items where item_id=?",(self.item_id,))
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
		#if old_state == state:
			#print("Item's state is already "+old_state)
		#else:
			#print("The item's state:"+ state_type + " has changed from "+old_state+" to "+ state+".")
		cursor.execute("update items set "+state_type+"=? where item_id=?",(state_id,self.item_id))	
		db.commit()

		for i in data:
			cursor.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(i[0],self.owner,self.owner,i[0],))
			data3=cursor.fetchall()
			if not(data3):
				continue
			if i[2]=="borrow":
				if state_type=="borrow" and state=="friends":
					print("Notification to "+ i[0] + " : "+self.owner + " added a borrowable book which name is " + self.title)
			elif i[2]=="detail":
				if state_type=="detail" and state=="friends":
					print("Notification to "+ i[0] + " : "+self.owner + " added a book which name is " + self.title)
			else:
				continue
		db.close()

	def watch(user,watch_method):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		cursor.execute("select (detail,comment,borrow) from items where item_id=?",(self.item_id,))
		detail = 0
		comment = 0
		borrow = 0
		for x in cursor:
			detail = x[0]
			comment = x[1]
			borrow = x[2]
		cursor.execute("select from isClose friends where ((user1=? and user2=?) or (user2=? and user1=?))",(user,self.owner))
		friendship = 0 #not friend
		count = 0
		for x in cursor:
			count+=1
		if count > 0:
			friendship = isClose
		if watch_method=="borrow":
			if borrow == 0:
				print("No right to watch this.")
			elif borrow == 1:
				if friendship !=0:
					cursor.execute("insert into watch values (?,?,?)",(user,self.item_id,watch_method))
					#watch it.
			elif borrow == 2:
				if friendship == 2:
					#watch it.
					cursor.execute("insert into watch values (?,?,?)",(user,self.item_id,watch_method))
			elif borrow ==3:
					#watch it.
					cursor.execute("insert into watch values (?,?,?)",(user,self.item_id,watch_method))
		else:#comment
			if (detail != 0) and (comment != 0):
				if detail == 1:
					#you can click watch
					if comment == 1:
						if friendship != 0:
							cursor.execute("insert into watch values (?,?,?)",(user,self.item_id,watch_method))
					if comment == 2:
						if friendship == 2:
							cursor.execute("insert into watch values (?,?,?)",(user,self.item_id,watch_method))
					if comment == 3:
							cursor.execute("insert into watch values (?,?,?)",(user,self.item_id,watch_method))	
				#elif detail == 2: #detailimi sadece
			else:
				print("No right to watch it.")
		db.commit()
		db.close()

	def annouence(type,msg):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		""" type 0->close,1->fri,2->close fr. 3-> everyone """
		print(self.owner+" announce a message: "+ msg)
		cursor.execute("insert into announces values(item_id,msg,friend_type) (?,?,?)",(self.item_id,msg,type))
		db.close()

	def can_look_at_it(self,user,comment_borrow):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		close = False
		friendship = False
		cursor.execute("select *from friendships where\
			(User1=? and User2=? and isClose=?)\
			 or \
			(User2=? and User1=? and isClose=?)",(self.owner,user.email,1,self.owner,user.email,2))
		count = 0
		for x in cursor:
			count+=1
		if count!=0:
			close = True
		cursor.execute("select * from friendships where \
			((User1=? and User2=?) \
			or \
			(User1=? and User2=?))",\
			(self.owner,user.email,user.email,self.owner))
		count = 0
		for x in cursor:
			count+=1
		if count!=0:
			friendship = True
		if comment_borrow=="comment":
			if self.comment_at == 0 :
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
			else:#everyone
				return True
		else:
			if self.borrow_at == 0 :
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
			else:#everyone
				return True
		db.close()

	def obje_set_state(self,state_type,no):
		if(state_type == "comment"):
			self.comment_at = no
		elif(state_type == "search"):
			self.search_at = no
		elif(state_type == "borrow"):
			self.borrow_at = no
		elif(state_type == "detail"):
			self.detail_at = no
		else:
			self.view_at = no
	def search(self,user, searchText, genre, year, forborrow=False):
		db = sqlite3.connect("test.sqlite")
		cursor = db.cursor()
		words=searchText.split(" ")
		years=year.split(":")
		datas1=[]
		datas2=[]
		datas3=[]
		datas4=[]
		for i in words:
			like_string="%"+i+"%"
			if len(years)==2:
				cursor.execute("select owner, search, borrow,title from items where title like ? and genre=? and year>=? and year<=?",(like_string,genre,years[0],years[1],))
				willappend=cursor.fetchall()
				datas1.append(willappend)
				cursor.execute("select owner, search, borrow, title from items where artist like ? and genre=? and year>=? and year<=?",(like_string,genre,int(years[0]),int(years[1]),))
				willappend=cursor.fetchall()
				datas2.append(willappend)
			else:
				cursor.execute("select owner, search, borrow,title from items where title like ? and genre=? and year=?",(like_string,genre,years[0],))
				willappend=cursor.fetchall()
				datas1.append(willappend)
				cursor.execute("select owner, search, borrow, title from items where artist like ? and genre=? and year=?",(like_string,genre,years[0],))
				willappend=cursor.fetchall()
				datas2.append(willappend)
		for b in datas1[0]:
			boole=True
			for c in datas1[1:]:
				if not(b in c):
					boole=False
					break
			if boole:
				datas3.append(b)
		
		for d in datas2[0]:
			boole=True
			for e in datas2[1:]:
				if not(d in e):
					boole=False
					break
			if boole:
				datas4.append(d)

		returning_datas=[]

		merged=list(set(datas3) - set(datas4))+list(set(datas4) - set(datas3))

		for m in merged:
			if not(forborrow):
				if m[1]==0:
					continue
				elif m[1]==1:
					cursor.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(m[0],user,user,m[0],))
					isTheyFriend=cursor.fetchall()
					if isTheyFriend:
						returning_datas.append([m[0], m[3]])
				elif m[1]==2:
					cursor.execute("Select * from friendships where (User1=? and User2=? and (isClose=1 or isClose=3)) or (User1=? and User2=? and (isClose=2 or isClose=3))",(m[0],user,user,m[0]))
					isSelfClose=cursor.fetchall()
					if isSelfClose:
						returning_datas.append([m[0], m[3]])
				else:
					returning_datas.append([m[0], m[3]])
			if forborrow:
				if m[2]==0:
					continue
				elif m[2]==1:
					cursor.execute("Select * from friendships where (User1=? and User2=?) or (User1=? and User2=?)",(m[0],user,user,m[0],))
					isTheyFriend=cursor.fetchall()
					if isTheyFriend:
						returning_datas.append([m[0], m[3]])
				elif m[2]==2:
					cursor.execute("Select * from friendships where (User1=? and User2=? and (isClose=1 or isClose=3)) or (User1=? and User2=? and (isClose=2 or isClose=3))",(m[0],user,user,m[0]))
					isSelfClose=cursor.fetchall()
					if isSelfClose:
						returning_datas.append([m[0], m[3]])
				else:
					returning_datas.append([m[0], m[3]])

		print (returning_datas)







	   
	
