# -*- coding: utf-8 -*-

from django.http import *
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import *

from project.models import *
# Create your views here.
import random
import isbnlib
import datetime
from django.db import connection
import time

class Userc:
	def __init__(self, email, password):
			self.email = email
			self.password = password
 
	def changepassword(self, newpassword, oldpassword=None):
		u = User.objects.get(username=self.email)
		usersDB = connection.cursor()
		if oldpassword == None or oldpassword=="":
			self.password = str(random.randint(100000, 999999))
			u.set_password(self.password)
			u.save()
			return "Your temporay password have been set to " + (self.password)
		else:
			print (oldpassword)
			if oldpassword == self.password:
				self.password = newpassword
				u.set_password(self.password)
				u.save()
				
				return "Your password have been changed."
			else:
				
				return "Your old password is false."
		
	def friend(self, email):
		
		usersDB = connection.cursor()
		usersDB.execute("Select username from auth_user where username={}".format("'"+email+"'"))
		data = usersDB.fetchall()
		if data:
			usersDB.execute("Select * from project_friendshiprequests where fromUser={} and toUser={}".format("'"+self.email+"'", "'"+email+"'"))
			data2 = usersDB.fetchall()
			usersDB.execute("Select * from project_friendshiprequests where fromUser={} and toUser={}".format("'"+email+"'", "'"+self.email+"'"))
			data3 = usersDB.fetchall()
			usersDB.execute("Select * from project_friendships where (User1={} and User2={}) or (User1={} and User2={})".format("'"+email+"'", "'"+self.email+"'", "'"+self.email+"'", "'"+email+"'"))
			data4 = usersDB.fetchall()
			if not (data2) and not (data3) and not (data4):
				usersDB.execute("insert into project_friendshiprequests(toUser,fromUser) VALUES({},{})".format("'"+email+"'", "'"+self.email+"'"))
				connection.commit()
				return "You have successfully sent friendship request to this user!"
			if data2:
				return "You already sent friendship request to this user!"
			elif data3:
				return "The user already sent you friendship request"
			elif data4:
				return "You are already friend"
		

	def setfriend(self, user, state):
		"""user is email."""
		
		usersDB = connection.cursor()
		if state == "nofriend":
			usersDB.execute("Select * from project_friendships where (User1={} and User2={}) or (User1={} and User2={})".format("'"+user+"'", "'"+self.email+"'", "'"+self.email+"'", "'"+user+"'"))
			data = usersDB.fetchall()
			usersDB.execute(
				"Select * from project_friendshiprequests where (fromUser={} and toUser={})".format("'"+user+"'", "'"+self.email+"'"))
			data2 = usersDB.fetchall()
			usersDB.execute(
				"Select * from project_friendshiprequests where (toUser={} and fromUser={})".format("'"+user+"'", "'"+self.email+"'"))
			data3 = usersDB.fetchall()
			if data:
				usersDB.execute("delete from project_friendships where (User1={} and User2={}) or (User1={} and User2={})".format("'"+user+"'", "'"+self.email+"'", "'"+self.email+"'", "'"+user+"'"))
				connection.commit()
				
				return "You have successfully unfriended " + user
			elif data2:
				usersDB.execute(
					"delete from project_friendshiprequests where (fromUser={} and toUser={})".format("'"+user+"'", "'"+self.email+"'"))
				connection.commit()
				
				return "You have successfully refused friendship request from " + user
			elif data3:
				usersDB.execute(
					"delete from project_friendshiprequests where (fromUser={} and toUser={})".format("'"+self.email+"'", "'"+user+"'"))
				connection.commit()
				
				return "You have successfully delete friendship request to " + user

		elif state == "friend":
			usersDB.execute("Select * from project_friendships where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
			data = usersDB.fetchall()
			usersDB.execute("Select * from project_friendships where (User2={} and User1={})".format("'"+self.email+"'", "'"+user+"'"))
			data2 = usersDB.fetchall()
			usersDB.execute("Select * from project_friendshiprequests where (toUser={} and fromUser={})".format("'"+self.email+"'", "'"+user+"'"))
			data4 = usersDB.fetchall()
			if data:
				if data[0][3] == 1:
					usersDB.execute("UPDATE project_friendships SET isClose=0 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully change friendship status with " + user + " from close friend to normal friend."
				elif data[0][3] == 3:
					usersDB.execute("UPDATE project_friendships SET isClose=2 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully change friendship status with " + user + " from close friend to normal friend."
			elif data2:
				if data2[0][3] == 2:
					usersDB.execute("UPDATE project_friendships SET isClose=0 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully change friendship status with " + user + " from close friend to normal friend."
				elif data2[0][3] == 3:
					usersDB.execute("UPDATE project_friendships SET isClose=1 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully change friendship status with " + user + " from close friend to normal friend."
			elif data4:
				usersDB.execute("insert into project_friendships(User1,User2,isClose) VALUES({},{},{})".format("'"+self.email+"'","'"+ user+"'", 0))
				connection.commit()
				usersDB.execute("delete from project_friendshiprequests where (toUser={} and fromUser={})".format("'"+self.email+"'", "'"+user+"'"))
				connection.commit()
				return "You have successfully accepted friendship request from " + user
		else:
			usersDB.execute("Select * from project_friendships where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
			data = usersDB.fetchall()
			usersDB.execute("Select * from project_friendships where (User2={} and User1={})".format("'"+self.email+"'", "'"+user+"'"))
			data2 = usersDB.fetchall()
			if data:
				if data[0][3] == 0:
					usersDB.execute("UPDATE project_friendships SET isClose=1 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully changed friendship status with " + user + " from normal friend to close friend."
				elif data[0][3] == 2:
					usersDB.execute("UPDATE project_friendships SET isClose=3 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully changed friendship status with " + user + " from normal friend to close friend."
			elif data2:
				if data2[0][3] == 0:
					usersDB.execute("UPDATE project_friendships SET isClose=2 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully change friendship status with " + user + " from normal friend to close friend."
				elif data2[0][3] == 1:
					usersDB.execute("UPDATE project_friendships SET isClose=3 where (User1={} and User2={})".format("'"+self.email+"'", "'"+user+"'"))
					connection.commit()
					
					return "You have successfully change friendship status with " + user + " from normal friend to close friend."
		

	def itemlist(self, user):
		"""user is mail."""
		
		usersDB = connection.cursor()
		usersDB.execute("select title, view from project_item where owner={}".format("'"+user+"'"))
		data = usersDB.fetchall()
		usersDB.execute("Select * from project_friendships where (User1={} and User2={}) or (User1={} and User2={})".format("'"+user+"'", "'"+self.email+"'", "'"+self.email+"'", "'"+user+"'"))
		isTheyFriend = usersDB.fetchall()
		usersDB.execute(
			"Select * from project_friendships where (User1={} and User2={} and (isClose=1 or isClose=3)) or (User1={} and User2={} and (isClose=2 or isClose=3))".format("'"+user+"'", "'"+self.email+"'", "'"+self.email+"'", "'"+user+"'"))
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
		
		return liste

	def watch(self, user, mode):
		"""user is mail"""
		
		usersDB = connection.cursor()
		usersDB.execute("Select * from project_friendships where (User1={} and User2={}) or (User1={} and User2={})".format("'"+user+"'", "'"+self.email+"'", "'"+self.email+"'", "'"+user+"'"))
		data = usersDB.fetchall()
		if not (data):
			connection.commit()
			
			return "You cannot watch " + user + " because you are not friend."
		elif mode != None:
			usersDB.execute("insert into project_watchersforaddings(watcher,watched,mode) values({},{},{})".format("'"+self.email+"'", "'"+user+"'", "'"+mode+"'"))
			connection.commit()
			
			return loggeduser.email + " has started to watch " + user + " for new item addings with mode " + mode + "."
		else:
			usersDB.execute("delete from project_watchersforaddings where watcher={} and watched={}".format("'"+self.email+"'", "'"+user+"'"))
			connection.commit()
			
			return loggeduser.email + " has ended watching " + user + " for new item addings."

loggeduser=None
def log(request):
	form = AuthenticationForm
	if(request.method=='POST'):
		username = request.POST['username']
		password = request.POST['password']
		global loggeduser
		loggeduser=Userc(username,password)
		giris_kontrol = AuthenticationForm(data=request.POST)
		if(giris_kontrol.is_valid()):
			kullanici = authenticate(username=username,password=password)
			login(request,kullanici)
			#Yönlendir
			return HttpResponseRedirect('home')
		elif username and password:
			user=None
			try:
				user = User.objects.get(username=username)
			except:
				pass
			if user:
				return render(request,'login.html',{'hata':1})
			user = User.objects.create_user(username, username, password)
			b = vers.objects.create()
			b.username=username
			b.vn="111111"
			b.isv="0"
			b.save()
			giris_kontrol = AuthenticationForm(data=request.POST)
			if(giris_kontrol.is_valid()):
				kullanici = authenticate(username=username,password=password)
				login(request,kullanici)
				#Yönlendir
				return HttpResponseRedirect('home')
	return render(request,'login.html',{'hata':0})
@login_required
def home(request):
	q1 = vers.objects.filter(username=request.user.username)[0]
	basarisiz=0
	if q1.isv=="0" and request.method=='POST':
		vnn = request.POST['verificationnumber']
		print(vnn)
		if vnn==q1.vn:
			q1.isv="1"
			q1.save()
			return HttpResponseRedirect('home')
		else:
			basarisiz=1
	return render(request,'home.html',{'isv':q1.isv,'ba':basarisiz})


@login_required
def logout1(request):
	logout(request)
	return redirect('/')

@login_required
def changepassword(request):
	global loggeduser
	donut=""
	if request.method=='POST':
			donut=loggeduser.changepassword(request.POST['textforchangepass2'],request.POST['textforchangepass'])
			kullanici = authenticate(username=loggeduser.email,password=loggeduser.password)
			login(request,kullanici)
	return render(request,'home.html',{'donutchangepass':donut})

@login_required
def lookup(request):
	donut=""
	donutl=[]
	if request.method=='POST':
		elist = request.POST['liste']
		elist2=elist.split(',')
		for m in elist2:
			try:
				user = User.objects.get(username=m)
				donutl.append(m)
			except:
				pass
		donut = ",".join(donutl)
	return render(request,'home.html',{'donut':donut})

@login_required
def itemhtml(request):
	global itemid
	return render(request, 'item.html', {'item': 'chosen item is:' + str(itemid)})


@login_required
def chooseitem(request):
	owner = request.POST['textforchooseitem']
	title = request.POST['textforchooseitem2']
	try:
		item = Item.objects.get(owner=owner, title=title)
		global itemid
		itemid = item.id
		return HttpResponseRedirect('item')
	except Exception as e:
		return render(request, 'home.html', {'donutchooseitem': 'The item could not found.'})


@login_required
def borrowedby(request):
	if request.method == 'POST':
		global itemid
		global loggeduser
		item = Item.objects.get(id=itemid)
		useremail = request.POST['textforborrowedby']
		returndate = request.POST['textforborrowedby2']
		returndate = int(returndate)
		thereis=False
		try:
			itemm=Item.objects.get(id=itemid ,owner=loggeduser.email)
		except:
			return render(request,'item.html',{'donutborrowedby':"You cannot give this item because you are not owner."})
		try:
			itemreq = ItemRequests.objects.get(item_id=itemid ,user_email=useremail)
			thereis=True
			firstitemreq = ItemRequests.objects.filter(item_id=itemid)[0]
			if firstitemreq.user_email!=useremail:
				return render(request,'item.html',{'donutborrowedby':"You cannot give this item to user because order of " + itembor.user_email + " is not 1."})
		except:
			pass
		notifs = []
		stri = "You cannot borrow this item."
		if thereis:
			thereis2=False
			boris=0
			try:
				itembor = ItemBorrows.objects.get(item_id=itemid)
				thereis2=True
				boris=itembor.is_returned
			except:
				pass
			if thereis2:
				if boris == 0:
					return render(request,'item.html',{'donutborrowedby':"It is already borrowed by " + itembor.user_email + "."})
				else:#not borrow for someone
					taking_time = datetime.date.today()
					returned_time = taking_time + datetime.timedelta(weeks=returndate)
					newitemborrow = ItemBorrows(item_id=itemid, user_email=useremail, return_date=returned_time,
												taking_date=taking_time, rate=0, is_returned=0)
					newitemborrow.save()
					try:
						watchitem = WatchItem.objects.get(item_id=itemid, type=1)
						mails = watchitem.user_email
						for mail in mails:
							notification_text = "Notification to " + loggeduser.email + " : " + useremail + "borrowed " + item.title
							notifs.append(notification_text)
							notification_type = 1;  # borrow
							newNotif = Notifications(user_email=useremail, notification_text=notification_text,
													 notification_type=notification_type)
							newNotif.save()
							stri = "The user:" + useremail + " borrowed the item:" + item.title + " until " + str(returned_time) + "."
							return render(request, 'item.html', {'donutborrowedby': stri})
					except:
						stri = "The user:" + useremail + " borrowed the item:" + item.title + " until " + str(returned_time) + "."
						return render(request, 'item.html', {'donutborrowedby': stri})
			else:#not borrow from someone.
				taking_time = datetime.date.today()
				returned_time = taking_time + datetime.timedelta(weeks=returndate)
				newitemborrow = ItemBorrows(item_id=itemid,user_email=useremail,return_date=returned_time,taking_date=taking_time,rate=0,is_returned=0)
				newitemborrow.save()
				cursor=connection.cursor()
				cursor.execute("select user_email from project_watchitem where item_id={} and type={}".format(itemid,"'borrow'"))
				data = cursor.fetchall()
				for i in data:
					newannouence = Notifications(user_email=i[0],notification_text=loggeduser.email + " borrowed item with title: "+ item.title,notification_type="none")
					newannouence.save()
				stri = "The user:" + useremail + " borrowed the item:" + item.title + " until " + str(returned_time) + "."
				return render(request, 'item.html', {'donutborrowedby': stri})

		else:
			return render(request,'item.html',{'donutborrowedby':useremail+"did not make a request yet, you cannot give."})



@login_required
def additem(request):
	if request.method == 'POST':
		uniqueid = request.POST['textforadditem']
		title = request.POST['textforadditem2']
		type = request.POST['textforadditem3']
		artist = request.POST['textforadditem4']
		genre = request.POST['textforadditem5']
		year = request.POST['textforadditem6']
		if uniqueid != "":
			try:
				book_metadata = isbnlib.meta(uniqid, service='default', cache='default')
				artist = book_metadata['Authors'][0]
				year = int(book_metadata['Year'])
				title = book_metadata['Title']
			except Exception as e:
				pass
		Item.objects.create(owner=request.user.username, type=type, title=title, uniqueid="", artist=artist,
							genre=genre,
							year=year, location="", rate=0, view=1, detail=1, borrow=1, comment=1, search=1)
		cursor = connection.cursor()
		cursor.execute("select watcher from project_watchersforaddings where watched={}".format("'"+loggeduser.email+"'"))
		data = cursor.fetchall()
		for i in data:
			newannouence = Notifications(user_email=i[0],notification_text=loggeduser.email + " added and item with title: "+ title,notification_type="none")
			newannouence.save()
		return render(request, 'home.html', {'donutadditem': "You have created the item."})
@login_required
def setfriend(request):
	global loggeduser
	donut=""
	if request.method=='POST':
			donut=loggeduser.setfriend(request.POST['textforsetfriend'],request.POST.get('textforsetfriend2'))
	return render(request,'home.html',{'donutsetfriend':donut})
@login_required
def friend(request):
	global loggeduser
	donut=""
	if request.method=='POST':
			donut=loggeduser.friend(request.POST['textforfriend'])
	return render(request,'home.html',{'donutfriend':donut})

@login_required
def listitems(request):
	global loggeduser
	donut=""
	if request.method=='POST':
			donut=loggeduser.itemlist(request.POST['textforlistitems'])
	return render(request,'home.html',{'donutlistitems':donut})
@login_required
def watchuser(request):
	global loggeduser
	donut=""
	if request.method=='POST':
			donut=loggeduser.watch(request.POST['textforwatchuser'],request.POST.get('textforwatchuser2'))
	return render(request,'home.html',{'donutwatchuser':donut})
@login_required
def getnotifs(request):
	if request.method == 'POST':
		cursor=connection.cursor()
		returnings=[]
		cursor.execute("select msg from project_announces where toUser={}".format("'"+loggeduser.email+"'"))
		datas=cursor.fetchall()
		for i in datas:
			returnings.append("Announce: "+i[0]+" ")
		returnings2=[]
		cursor.execute("select notification_text from project_notifications where user_email={}".format("'"+loggeduser.email+"'"))
		datas=cursor.fetchall()
		for i in datas:
			returnings2.append("Notification: "+i[0]+" ")
		return render(request, 'home.html', {'donutnotifs': returnings,'donutnotifs2': returnings2})
@login_required
def getrating(request):
	if request.method == 'POST':
		try:
			global itemid
			itemborrows = ItemBorrows.objects.filter(item_id=itemid)
			lene = len(itemborrows)
			total=0
			print(itemborrows)
			for i in itemborrows:
				print(i.rate)
				total+=int(i.rate)
			rating = (total)/lene
			return render(request,'item.html',{'donutgetrating':str(rating)+", number of rates: "+str(lene)})
		except:
			return render(request,'item.html',{'donutgetrating':"0,0"})

def getratingF():
	try:
		global itemid
		itemborrows = ItemBorrows.objects.filter(item_id=itemid)
		lene = len(itemborrows)
		total=0
		print(itemborrows)
		for i in itemborrows:
			print(i.rate)
			total+=int(i.rate)
		rating = (total)/lene
		return rating
	except:
		return 0.0


@login_required
def returned(request):
	if request.method == 'POST':
		global itemid
		try:
			itemm=Item.objects.get(id=itemid ,owner=loggeduser.email)
		except:
			return render(request,'item.html',{'donutreturned':"You cannot indicate that this item is returned because you are not owner."})
		itemborrow = ItemBorrows.objects.get(item_id=itemid)
		itemborrow.is_returned = 1
		itemborrow.save()
		location = request.POST['textforreturned']
		item = Item.objects.get(id=itemid)
		item.location = location
		try:
			itemwatches = WatchItem.objects.get(item_id=itemid, type=1)
			iw_email = itemwatches.user_email
			stri = "The item titled with " + item.title + " was returned"
			notifs = []
			for user_email in iw_email:
				notification_text = "Notification to " + user_email + " : The item titled with" + item.title + "is returned."
				# print
				notifs.append(notification_text)
				# print
				notification_type = 1  # borrow
				notif = Notifications(user_email, notification_text, notification_type)
				notif.save()
		except:
			pass
		donut = (stri, notifs)
		return render(request, 'home.html', {'donutreturned': donut})


@login_required
def borrowedreq(request):
	if request.method == 'POST':
		global itemid, loggeduser
		email = loggeduser.email
		if can_look_at_it(email, "borrow"):
			# global user dan alıyo gibi düşün.
			cntrl=True
			try:
				itemreq = ItemRequests.objects.get(item_id=itemid, user_email=email)
				cntrl=False
			except:
				pass
			# daha onceden req. atmadıysa.
			if cntrl:
				#
				request_date = datetime.date.today()
				itreq = ItemRequests.objects.create(item_id=itemid, user_email=email, request_date=request_date)
				itreq2 = ItemRequests.objects.filter(item_id=itemid)
				order = len(itreq2)
				item = Item.objects.get(id=itemid)
				returndata = "A borrow request for item: " + item.title + " successfully created for " + email + " and order is " + str(
					order) + "."
			else:
				returndata = "You have already made a request."
			return render(request, 'item.html', {'donutborrowedreq': returndata})
		else:
			return render(request,'item.html',{'donutborrowedreq':"You cannot make a request for this item."})

@login_required
def rate(request):
	if request.method == 'POST':
		global itemid,loggeduser
		rating = request.POST['textforrate']
		email = loggeduser.email
		item = Item.objects.get(id = itemid)
		cntrl=False
		try:
			borrows = ItemBorrows.objects.get(item_id = itemid,user_email=email)
			cntrl=True
			borrows = ItemBorrows.objects.get(item_id=itemid, user_email=email, rate=0)
			borrows.rate = rating
			borrows.save()
			return render(request,'item.html',{'donutrate':loggeduser.email + " rate the item: " + item.title + " and its rate is:" + str(rating) + "."})
		except Exception as e:
			if cntrl:
				return render(request,'item.html',{'donutrate':"You rated this item before."})
			return render(request,'item.html',{'donutrate':"You cannot rate before borrowing the item."})
@login_required
def locate(request):
	if request.method == 'POST':
		location = request.POST['textforlocate']
		global itemid,loggeduser
		item = Item.objects.get(id=itemid)
		item.location = location
		item.save()
		return render(request,'item.html',{'donutlocate':"The item's location has changed to location:" + location + "."})
@login_required
def setstate(request):
	if request.method == 'POST':
		notifs = []
		#bunu anlamadim?? notifs mi döncek??
		statetype = request.POST['textforsetstate']
		state = request.POST['textforsetstate2']
		global itemid,loggeduser
		item = Item.objects.get(id=itemid)
		state_id = 0
		if state == "closed":
			state_id = 0
		elif state == "everyone":
			state_id = 3
		elif state == "friends":
			state_id = 1
		elif state == "closefriends":
			state_id = 2
		old_state_id = 0
		if statetype == "comment":
			old_state_id = item.comment
			item.comment = state_id
		elif statetype == "view":
			old_state_id = item.view
			item.view = state_id
		elif statetype == "detail":
			old_state_id = item.detail
			item.detail = state_id
		elif statetype == "search":
			old_state_id = item.search
			item.search = state_id
		elif statetype == "borrow":
			old_state_id = item.borrow
			item.borrow = state_id
		if old_state_id == 0:
			old_state = "closed"
		elif old_state_id == 1:
			old_state = "everyone"
		elif old_state_id == 2:
			old_state = "friends"
		else:
			old_state = "close friends"
		item.save()
		stri = "The item's state:" + statetype + " has changed from " + old_state + " to " + state + "."
		return render(request,'item.html',{'donutsetstate':stri})
@login_required
def announce(request):
	if request.method == 'POST':
		global itemid,loggeduser
		item = Item.objects.get(id=itemid)
		if item.owner!=loggeduser.email:
			return render(request,'item.html',{'donutannouence':"you cannot announce a message on this item because YOU ARE NOT OWNER!"})
		""" type 0->close,1->fri,2->close fr. 3-> everyone """
		typee = request.POST['textforannounce']
		msg = request.POST['textforannounce2']
		receivcers=[]
		cursor=connection.cursor()
		if typee=="friends":
			cursor.execute("select User2,User1 from project_friendships where User1={}".format("'"+item.owner+"'"))
			data1=cursor.fetchall()
			cursor.execute("select User1,User2 from project_friendships where User2={}".format("'"+item.owner+"'"))
			data2=cursor.fetchall()
			receivcers=data1+data2
		elif typee=="closefriends":
			cursor.execute("select User2,User1 from project_friendships where User1={} and (isClose==1 or isClose=3)".format("'"+self.owner+"'"))
			data1=cursor.fetchall()
			cursor.execute("select User1,User2 from project_friendships where User2={} and (isClose==2 or isClose=3)".format("'"+self.owner+"'"))
			data2=cursor.fetchall()
			receivcers=data1+data2
		for i in receivcers:
			newannouence = Announces(item_id=itemid,msg=item.owner + " announce a message: " + msg + " on item: " + item.title,toUser=i[0])
			newannouence.save()
		returndata = item.owner + " announce a message: " + msg + "on item: " + item.title
		return render(request,'item.html',{'donutannouence':returndata})
@login_required
def view(request):
	if request.method == 'POST':
		global itemid,loggeduser
		email=loggeduser.email
		if can_look_at_it(email,"view"):
			item = Item.objects.get(id=itemid)
			returndata = "Title: " + item.title + ", Artist: " + item.artist + ", Year: " + str(item.year) + ", Owner: " + item.owner 
			return render(request,'item.html',{'donutview':returndata})
		else:
			return render(request,'item.html',{'donutview':"You are not authorized view this item"})

@login_required
def detail(request):
	if request.method == 'POST':
		global itemid,loggeduser
		email=loggeduser.email
		if can_look_at_it(email,"detail"):
			item = Item.objects.get(id=itemid)
			returndata = "Title: " + item.title + ", Artist: " + item.artist + ", Year: " + str(item.year) + ", Owner: " + item.owner+ ", Rating: " + str(getratingF()) +", Location: " + item.location
			return render(request,'item.html',{'donutdetail':returndata})
		else:
			return render(request,'item.html',{'donutdetail':"You are not authorized to view detail of this item"})
@login_required
def delete(request):
	if request.method == 'POST':
		global itemid,loggeduser
		item = Item.objects.get(id=itemid)
		title = item.title
		owner = item.owner
		returndata="You cannot delete because the item does not belong to you."
		if owner == loggeduser.email:
			item.delete()
			returndata = title + " deleted by "+owner
			try:
				itemrequests = ItemRequests.objects.filter(item_id = itemid).delete()
			except:#no item req
				pass
		return render(request,'home.html')

@login_required
def watchitem(request):
	if request.method == 'POST':
		global itemid,loggeduser
		item = Item.objects.get(id=itemid)
		owner = item.owner
		stri = "You cannot watch this item."
		friend = 0
		close = 0
		user = loggeduser.email
		watch_method = request.POST['textforwatchitem2']
		print(watch_method,user,owner)
		try:
			data1 = Friendships.objects.get(user1=user,user2=owner)
		except Exception as e:
			data1 = None
		try:
			data2 = Friendships.objects.get(user1=owner, user2=user)
		except Exception as e:
			data2 = None

		if data1 or data2:
			friend = 1
		if data1:
			if data1.isClose == 2 or data1.isClose == 3:
				close = 1
		if data2:
			if data2.isClose == 1 or data2.isClose == 3:
				close = 1
		if watch_method == "borrow":
			if item.borrow == 1 and friend:
				newWatch = WatchItem(user_email=user, item_id=itemid, type=watch_method)
				newWatch.save()
				stri = "You started to watch this item."
			elif item.borrow == 2 and close:
				newWatch = WatchItem(user_email=user, item_id=itemid, type=watch_method)
				newWatch.save()
				stri = "You started to watch this item."
			elif item.borrow == 3:
				newWatch = WatchItem(user_email=user, item_id=itemid, type=watch_method)
				newWatch.save()
				stri = "You started to watch this item."
		elif watch_method == "comment":
			if item.comment == 1 and friend:
				newWatch = WatchItem(user_email=user, item_id=itemid, type=watch_method)
				newWatch.save()
				stri = "You started to watch this item."
			elif item.comment == 2 and close:
				newWatch = WatchItem(user_email=user, item_id=itemid, type=watch_method)
				newWatch.save()
				stri = "You started to watch this item."
			elif item.comment == 3:
				newWatch = WatchItem(user_email=user, item_id=itemid, type=watch_method)
				newWatch.save()
				stri = "You started to watch this item."

		return render(request,'item.html',{'donutwatchitem':stri})


@login_required
def comment(request):
	if request.method == 'POST':
		global itemid, loggeduser
		email = loggeduser.email
		if can_look_at_it(email, "comment"):
			request_date = datetime.date.today()
			Comments.objects.create(item_id=itemid, user_email=email,comment_text= request.POST['textforcomment'],comment_date=request_date)
			item=Item.objects.get(id=itemid)
			returndata = "A comment for item: " + item.title + " successfully created by " + email + " and text is " + str(
			request.POST['textforcomment']) + "."
			cursor = connection.cursor()
			cursor.execute("select user_email from project_watchitem where item_id={} and type={}".format(itemid,"'comment'"))
			data = cursor.fetchall()
			for i in data:
				newannouence = Notifications(user_email=i[0],notification_text=loggeduser.email + " commented on item with title: "+ item.title,notification_type="none")
				newannouence.save()
		else:
			returndata="You are not authorized to comment this item."
		return render(request, 'item.html', {'donutcomment': returndata})

@login_required
def commentlist(request):
	if request.method == 'POST':
		donutl=[]
		global itemid
		commentliste=Comments.objects.filter(id=itemid)
		for i in commentliste:
			donutl.append(i.user_email+ ": " + i.comment_text)
		donut = ", ".join(donutl)
		return render(request, 'item.html', {'donutcommentlist': donut})

def can_look_at_it(user, comment_borrow):
	""" """
	global itemid
	close = False
	friendship = False
	item = Item.objects.get(id=itemid)
	try:
		a = Friendships.objects.get(user1=item.owner, user2=user, isClose=1)
		close=True
	except:
		pass
	try:
		b = Friendships.objects.get(user2=item.owner, user1=user, isClose=2)
		close=True
	except:
		pass
	try:
		a = Friendships.objects.get(user1=item.owner, user2=user, isClose=3)
		close=True
	except:
		pass
	try:
		b = Friendships.objects.get(user2=item.owner, user1=user, isClose=3)
		close=True
	except:
		pass
	try:
		a = Friendships.objects.get(user1=item.owner, user2=user)
		friendship=True
	except:
		pass
	try:
		Friendships.objects.get(user2=item.owner, user1=user)
		friendship=True
	except:
		pass
	itemcomment = item.comment
	borrowcomment = item.borrow
	if comment_borrow == "comment":
		if item.owner==user:
			return True
		if itemcomment == 0:
			return False
		elif itemcomment == 1:
			if friendship:
				return True
			else:
				return False
		if itemcomment == 2:
			if close:
				return True
			else:
				return False
		else:
			return True
	elif comment_borrow=="borrow":
		if borrowcomment == 0:
			return False
		elif borrowcomment == 1:
			if friendship:
				return True
			else:
				return False
		if borrowcomment == 2:
			if close:
				return True
			else:
				return False
		else:
			return True
	elif comment_borrow == "detail":
		if item.owner==user:
			return True
		if item.detail == 0:
			return False
		elif item.detail == 1:
			if friendship:
				return True
			else:
				return False
		if item.detail == 2:
			if close:
				return True
			else:
				return False
		else:
			return True
	elif comment_borrow == "view":
		if item.owner==user:
			return True
		if item.view == 0:
			return False
		elif item.view == 1:
			if friendship:
				return True
			else:
				return False
		if item.view == 2:
			if close:
				return True
			else:
				return False
		else:
			return True
	elif comment_borrow == "search":
		if item.owner==search:
			return True
		if item.search == 0:
			return False
		elif item.search == 1:
			if friendship:
				return True
			else:
				return False
		if item.search == 2:
			if close:
				return True
			else:
				return False
		else:
			return True


def searchHelper(user, searchText, genre, year, forborrow=False):
	cursor = connection.cursor()
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
				"select owner, search, borrow,title from project_item where title like {} and genre={} and year>={} and year<={}".format("'"+like_string+"'","'" + genre+"'",int(years[0]), int(years[1])))
			willappend = cursor.fetchall()
			datas1.append(willappend)
			cursor.execute(
				"select owner, search, borrow, title from project_item where artist like {} and genre={} and year>={} and year<={}".format("'"+like_string+"'","'" + genre+"'",int(years[0]), int(years[1])))
			willappend = cursor.fetchall()
			datas2.append(willappend)
		else:
			cursor.execute(
				"select owner, search, borrow,title from project_item where title like {} and genre={} and year={}".format("'"+like_string+"'","'" + genre+"'",int(years[0])))
			willappend = cursor.fetchall()
			datas1.append(willappend)
			cursor.execute(
				"select owner, search, borrow, title from project_item where artist like {} and genre={} and year={}".format("'"+like_string+"'","'" + genre+"'",int(years[0])))
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
			if m[1] == 0 and user!=m[0]:
				continue
			elif m[1] == 1 and user!=m[0]:
				cursor.execute("Select * from project_friendships where (User1={} and User2={}) or (User1={} and User2={})".format("'"+m[0]+"'", "'"+user+"'", "'"+user+"'", "'"+m[0]+"'"))
				isTheyFriend = cursor.fetchall()
				if isTheyFriend:
					returning_datas.append([m[0], m[3]])
			elif m[1] == 2 and user!=m[0]:
				cursor.execute(
					"Select * from project_friendships where (User1={} and User2={} and (isClose=1 or isClose=3)) or (User1={} and User2={} and (isClose=2 or isClose=3))".format("'"+m[0]+"'", "'"+user+"'", "'"+user+"'", "'"+m[0]+"'"))
				isSelfClose = cursor.fetchall()
				if isSelfClose:
					returning_datas.append([m[0], m[3]])
			else:
				returning_datas.append([m[0], m[3]])
		if forborrow:
			if m[2] == 0 and user!=m[0]:
				continue
			elif m[2] == 1 and user!=m[0]:
				cursor.execute("Select * from project_friendships where (User1={} and User2={}) or (User1={} and User2={})".format("'"+m[0]+"'", "'"+user+"'", "'"+user+"'", "'"+m[0]+"'"))
				isTheyFriend = cursor.fetchall()
				if isTheyFriend:
					returning_datas.append([m[0], m[3]])
			elif m[2] == 2 and user!=m[0]:
				cursor.execute(
					"Select * from project_friendships where (User1={} and User2={} and (isClose=1 or isClose=3)) or (User1={} and User2={} and (isClose=2 or isClose=3))".format("'"+m[0]+"'", "'"+user+"'", "'"+user+"'", "'"+m[0]+"'"))
				isSelfClose = cursor.fetchall()
				if isSelfClose:
					returning_datas.append([m[0], m[3]])
			else:
				returning_datas.append([m[0], m[3]])

	return returning_datas


@login_required
def search(request):
	if request.method == 'POST':
		global loggeduser
		email=loggeduser.email
		forborrow=False
		if request.POST.get('textforsearch5')=="yes":
			forborrow=True
		return render(request, 'home.html', {'donutsearch': searchHelper(email,request.POST['textforsearch2'],request.POST['textforsearch3'],request.POST['textforsearch4'],forborrow)})
#COMMENT SU ANKI USERI ALCAKK
#SEARCH ICIN FORBORROW NE ALIYOR{}{}{}
#DELETE METODUNDA SU ANKI USERLA OWNERI KARSILASTIR EGER OYSA GOSTER YOKSA DELETE I GOSTERME.
