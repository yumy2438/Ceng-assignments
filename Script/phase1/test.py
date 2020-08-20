import sqlite3
import os
from phase1 import *
import random
def construct_database(cur,db):
	cur.execute("create table user_main_infos(\
		email,\
		namesurname,\
		password,\
		isActive,\
		verificationNumber)")
	cur.execute("create table friendships(\
		User1 text,\
		User2 text,\
		isClose integer)")
	cur.execute("create table friendship_requests(\
		toUser text,\
		fromUser text)")
	cur.execute("create table watchers_for_addings(watcher,watched, mode)")
	cur.execute("create table items (item_id integer primary key,\
			owner text,\
		type text,\
		title text,\
		uniqid text,\
		artist text,\
		genre text,\
		year integer,\
		location text,\
		rate integer,\
		view integer,\
		detail integer,\
		borrow integer,\
		comment integer,\
		search integer)")
	cur.execute("create table comments(\
			comment_id integer not null primary key,\
			user_email text,\
			comment_text text\
			,comment_date text\
			,item_id integer)")
	cur.execute("create table itemborrows(\
			borrow_id integer primary key,\
			item_id integer,\
			user_email text,\
			return_date text,\
			taking_date text,\
			rate integer,\
			is_returned integer)")
	cur.execute("create table itemrequests(\
			request_id integer primary key,\
			item_id integer,\
			user_email text,\
			request_date text)")
	#type=0 comment, 1=barrow
	cur.execute("create table notifications(\
		notification_id integer,\
		user_email text,\
		notification_text text,\
		notification_type integer\
		)")
	cur.execute("create table watch(\
			user_email text,\
			item_id integer,\
			type integer,\
			primary key(user_email,item_id,type))")
	cur.execute("create table announces(\
			announce_id integer,\
			item_id integer,\
			friend_type integer,\
			msg text)")
	cur.execute("create table watch2(\
		user_followed text,\
		user_following text,\
		primary key(user_followed,user_following))")
	db.commit()

        

def test():
	print("--------------------------------------------------")
	print("TEST1")
	print("--------------------------------------------------")
	db = sqlite3.connect("test.sqlite")
	cur = db.cursor()
	construct_database(cur,db)
	print("A USER WİLL BE CREATED...")
	user1=User("e217155@metu.edu.tr", "Soner Durmaz", "123456")
	print("THE USER WİLL BE VERIFIED...")
	user1.verify(user1.email,user1.verificationNumber)
	print("THE USER WILL CHANGE HIS PASSWORD...")
	user1.changepassword("soner", "123456")
	print("ANOTHER USER WİLL BE CREATED...")
	user2=User("e217218@metu.edu.tr", "Esra Yildiz", "123456")
	print("THE RECENT CREATED USER WİLL BE VERIFIED...")
	user2.verify(user2.email,user2.verificationNumber)
	print("THE FIRST CREATED USER WILL SEARCH TWO EMAILS WITH LOOKUP FUNCTION AND THE ONE EMAIL IS REGISTERED")
	user1.lookup(["e217218@metu.edu.tr", "sd@sd.com"])
	print("THE FIRST CREATED USER WİLL SEND FRIENDSHIP REQUEST TO THE SECOND CREATED USER...")
	user1.friend("e217218@metu.edu.tr")
	print("THE SECOND CREATED USER WİLL ACCEPT THE FRIENDSHIP REQUEST FROM THE FIRST CREATED USER...")
	user2.setfriend(user1,"friend")
	print("THE FIRST CREATED USER WİLL WATCH THE FIRST CREATED USER FOR NEW ADDINGS DETAIL...")
	user1.watch(user2,"detail")
	print("AN ITEM WILL BE CREATED BELONG TO FIRST CREATED USER")
	item1 = Item("e217155@metu.edu.tr","Kitap","Serenad",None,"Zülfü Livaneli","Dram","2003")
	print("AN ITEM WILL BE CREATED BELONG TO SECOND CREATED USER")
	item2 = Item("e217218@metu.edu.tr","Film","Yıldızlararası",None,"Christopher Nolan","Science","2014")
	print("THE RECENT CREATED ITEM WILL BE OPEN FRIENDS FOR DETAIL AND AN NOTIFICATION WILL GOES TO USER1")
	item2.setstate("detail","friends")
	print("THE FIRST CREATED USER WİLL END TO WATCH THE FIRST CREATED USER FOR NEW ADDINGS DETAIL...")
	user1.watch(user2,None)
	print("THE SECOND CREATED ITEM WILL BE OPEN TO EVERYONE TO VIEW")
	item2.setstate("view","everyone")
	print("THE FIRST USER WILL BE LOOK SECOND USER'S ITEMS")
	user1.itemlist(user2)
	print("THE RECENT CREATED ITEM WILL BE OPEN FRIENDS TO SEARCH")
	item2.setstate("search","friends")
	user1.watch(user2,None)
	print("THE USER1 WILL SEARCH AN ITEM WHICH SEARCH TEXT IS NOLAN AND GENRE IS SCIENCE AND YEAR IS 2014")
	item2.search(user1.email, "Nolan", "Science","2014")
	print("THE SECOND ITEM WILL BE OPEN ONLY CLOSE FRIENDS TO SEARCH")
	item2.setstate("search","close friends")
	print("THE USER1 WILL SEARCH AN ITEM WHICH SEARCH TEXT IS NOLAN AND GENRE IS SCIENCE AND YEAR IS 2014 AFTER IT WILL OPEN TO CLOSE FRIENDS TO SEARCH")
	item2.search(user1.email, "Nolan", "Science","2014")
	db.close()
	os.remove("test.sqlite")

def test2():
	print("--------------------------------------------------")
	print("TEST2")
	print("--------------------------------------------------")
	friend_type = ["friend","closefriend"]
	state_type = ["view","comment","search","borrow","detail"]
	states = ["closed","everyone","friends","close friends"]
	locations = ["shelf1","shelf2","shelf3"]
	comment_texts=["nicee!","i dont like it.","beautiful...","you are a liar!"]
	db = sqlite3.connect("test.sqlite")
	cur = db.cursor()
	construct_database(cur,db)
	users_name = ["Rachel Green","Joey Tribbiani","Ross Geller","Phoebe Buffay","Chandler Bing","Monica Geller"]
	users_mail = ["rachel_g@mail.com","joey_t@mail.com","ross_g@mail.com","phoebe_b@mail.com","changler_b@mail.com","monica_g@mail.com"]
	
	users = []
	for x in range(6):
		user = User(users_mail[x],users_name[x],"111111")
		users.append(user)
	for x in range(6):
		y = random.randint(0,5)
		if y==x:
			if y !=0:
				y-=1
			if y != 5:
				y+=1
		users[x].friend(users[y].email)
		fr_type = friend_type[random.randint(0,1)]
		users[x].setfriend(users[y],fr_type)
		print(users[x].namesurname+" is "+fr_type+" with "+ users[y].namesurname)
	item_types = ["movie","book"]
	item_title = ["Star Wars: The Last Jedi","Inception","The Matrix","The Little Prince",\
					"A Tale of Two Cities"]
	uniqid = ["978-0446310789"]
	artist = ["George Lucas","Christopher Nolan","Wachowski Brothers",\
	"Antoine de Saint-Exupéry","Charles Dickens"]
	genre = ["Fantasy","Sci-Fi","Sci-Fi","Fantasy","Historical Fiction"] 
	year = ["2017","2010","1999","1943","1859"]
	print("-------------------------------")
	print("CREATING ITEMS")
	print("-------------------------------")
	items = []
	print("Trying adding the book with isbn number:")
	print("-------------------------------")
	item = Item(users_mail[5],item_types[1],None,"9780446310789",None,None,None)
	items.append(item)
	for x in range(5):
		if x<3:
			item = Item(users_mail[x],item_types[0],item_title[x],None,artist[x],genre[x],year[x])
		elif x<5:
			item = Item(users_mail[x],item_types[1],item_title[x],None,artist[x],genre[x],year[x])
		for m in range(4):
			item.setstate(state_type[m],states[random.randint(1,3)])
		items.append(item)
	print("-------------------------------")
	print("Borrowing requests for permitted users:")
	print("-------------------------------")
	for x in range(30):
		y = random.randint(0,5)
		if (x%6) == y:
			if y != 0:
				y-=1
			elif y != 5:
				y+=1
		items[x%6].borrowedreq(users[y])
	print("-------------------------------")
	print("Locating items:")
	print("-------------------------------")
	for x in range(5):
		items[x].locate(locations[random.randint(0,2)])
	print("-------------------------------")
	print("Borrowed by:")
	print("-------------------------------")
	for x in range(40):
		items[x%6].borrowedby(users[random.randint(0,5)],2)


	print("-------------------------------")
	print("Rating items:")
	print("-------------------------------")
	for x in range(15):
		rating=random.randint(1,5)
		items[x%6].rate(users[random.randint(0,5)],rating)
	print("-------------------------------")
	print("Rating results:")
	print("-------------------------------")
	for x in range(6):
		(rating,number)=items[x].getrating()
		print("The average rating of "+ items[x].title +" is " + str(rating) + "(" + str(number) + ")")

	print("-------------------------------")
	print("Make a comment:")
	print("-------------------------------")
	
	for x in range(15):
		items[x%6].comment(users[random.randint(0,5)],comment_texts[random.randint(0,3)])
	print("-------------------------------")
	print("List comments:")
	print("-------------------------------")
	
	for x in range(6):
		for (user,comment) in items[x].list_comments():
			print(user+" had a comment about the item "+items[x].title+": "+comment)


	db.close()
	os.remove("test.sqlite")


test()
test2()


