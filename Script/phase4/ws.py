from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import threading
from user import *
from item import *
import pickle
from concurrent.futures import ThreadPoolExecutor as TPE
from concurrent.futures import Future
import pickle
from typing import List, Tuple
from random import randint


import sys
import os
from socket import *
import asyncio
import websockets
import logging
import json
import http.cookies
from threading import Thread


def singleton(cls):
		'''generic python decorator to make any class
		singleton.'''
		_instances = {}   # keep classname vs. instance
		def getinstance():
				'''if cls is not in _instances create it
				and store. return the stored instance'''
				if cls not in _instances:
						_instances[cls] = cls()
				return _instances[cls]
		return getinstance



@singleton
class Notifications:
	'''An observer class, saving notifications and notifiying
		registered coroutines'''
	def __init__(self):
		self.observers = {}
		self.broadcast = set()
		self.messages = {}

	def register(self, ws, cid):
		'''register a Lock and an id string'''
		print(cid)
		if cid in self.observers:
			self.observers[cid].add(ws)
		else:
			self.observers[cid] = set([ws])
		self.broadcast.add(ws)
		print(self.observers)

	def unregister(self, ws, cid):
		'''remove registration'''
		if cid not in self.observers:
			return
		self.observers[cid].discard(ws)
		self.broadcast.discard(ws)
		if self.observers[cid] == set():
			del self.observers[cid]
		print(self.observers)

	def addNotification(self, oid, message):
		'''add a notification for websocket conns with id == oid
			the '*' oid is broadcast. Message is the dictionary
			to be sent to connected websockets.
		'''
		if oid == '*':     # broadcast message
			for c in self.broadcast:
				print(c)
				yield from c.send(json.dumps(message))
		print(self.observers)
		if oid in self.observers:
			print("op")
			print (oid)
			print(self.observers[oid])
			for c in self.observers[oid]:
				yield from c.send(json.dumps(message))



def parse_data(data):
	return data.split(' ')

def log(username,password):
	user = User(username, password,"login")
	if user.isFalse:
		return ["hatalisifre","0",username]
	if user.isVerified:
		return ["girildi","1",username]
	return ["girildi","0",username]

def verify(username,verifcode):
	user = User(username, None,"notlogin")
	ret=user.verify(username,verifcode)
	if ret:
		return ["verify",1]
	else:
		return["verify",0]

def other(username,command,own,tit):
	user = User(username, None,"notlogin")
	data_array = parse_data(command)
	vt = sqlite3.connect('database.db')
	userDB = vt.cursor()
	if data_array[0] == "changepassword":
		new = data_array[1]
		old = data_array[2]
		msg = user.changepassword(new, old)
		print("hello")
		return msg
	elif data_array[0] == "lookup":
		print("here")
		msg = user.lookup(*(data_array[1:]))
		return msg
	elif data_array[0] == "friend":
		msg = user.friend(data_array[1])
		return msg
	elif data_array[0] == "setfriend":
		state = data_array[2]
		msg = user.setfriend(data_array[1], state)
		return msg
	elif data_array[0] == "itemlist":
		msg = user.itemlist(data_array[1])
		return ", ".join(msg)
	elif data_array[0] == "watch":
		mode = data_array[2]
		msg = user.watch(data_array[1], mode)
		return msg
	elif data_array[0] == "additem":
		created = 0
		announces = ["notifs"]
		msg=""
		if len(data_array) == 6:  # uniqidsiz
			print(data_array[1:3])
			chosen_item = Item(user.email, *(data_array[1:3]), None, *(data_array[3:]))
			msg = "The item has created successfully with the name: " + chosen_item.title + "."
			created = 1
		elif len(data_array) == 2:  # only isbn
			chosen_item = Item(user.email, None, None, data_array[1], None, None, None)
			msg = "The item has created successfully with the name: " + chosen_item.title + "."
			created = 1
		else:
			msg = "Please write in the format of additem isbn_no or additem type title artist genre year."
		if created:
			userDB.execute("select * from watchers_for_addings where watched=?", (user.email,))
			data = userDB.fetchall()
			for i in data:
				print (i)
				strin = "Notification to " + i[0] + " that " + user.email + " added new item."
				announces.append(strin)
			print(announces)
			vt.close()
		if len(announces):
			return [msg,announces]
		else:
			return msg

	elif data_array[0] == "chooseitem":
		# Chose an item for operations.
		owner = data_array[1]
		title = data_array[2]
		for i in range(3, len(data_array)):
			title += " " + data_array[i]
		print(title)
		userDB.execute(
			"select owner,type,title,uniqid,artist,genre,year from items where (owner=? and title=?)",
			(owner, title))
		data = userDB.fetchall()
		if data:
			msg = "The item: " + title + " has chosen"
		else:
			msg = "There is no item like this."
		vt.close()
		return ["c",msg,owner,title]

	elif data_array[0] == "detail":
		msg = ""
		if own == "" and tit == "":
			msg = "You did not chose any item!"
		else:
			userDB.execute(
				"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
				(own, tit))
			data = userDB.fetchall()
			data=data[0]
			print(data)
			chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
			msg = chosen_item.detail(user.email)
			print (msg)
		return msg

	elif data_array[0] == "view":
		msg=""
		if own=="" and tit=="":
			msg="You did not chose any item!"
			return msg
		else:
			userDB.execute(
				"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
				(own, tit))
			data = userDB.fetchall()
			data=data[0]
			print(data)
			chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
			msg = chosen_item.view(user.email)
			print (msg)
			return msg

	elif data_array[0] == "delete":
		msg = "You cannot delete the item since the item does not belong to you."
		if user.email == own:
			userDB.execute(
				"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
				(own, tit))
			data = userDB.fetchall()
			data=data[0]
			chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
			msg = chosen_item.delete()
		return msg

	elif data_array[0] == "comment":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		print("HERE")
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		announces = ["notifs"]
		comment_text = " ".join(data_array[1:])
		msg = chosen_item.comment(username, comment_text)
		msg2 = msg[1]
		msg = msg[0]
		announces=announces+msg2
		return[msg,announces]

	elif data_array[0] == "locate":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		comment_text = " ".join(data_array[1:])
		msg = chosen_item.locate(comment_text)
		return msg

	elif data_array[0] == "announce":
		if own!=username:
			return["You cannot because you are not owner",["notifs"]]
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		announces = ["notifs"]
		typee = data_array[1]
		announce_msg = " ".join(data_array[2:])
		msg = chosen_item.annouence(typee,announce_msg)
		msg2 = msg[1]
		msg = msg[0]
		announces=announces+msg2
		return[msg,announces]

	elif data_array[0] == "search":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		genre = data_array[1]
		year = data_array[2]
		borrow = data_array[3]
		bool_borrow = False
		if borrow == "yes":
			bool_borrow = True
		text = " ".join(data_array[3:])
		msg = chosen_item.search(username, text, genre, year, bool_borrow)
		return ", ".join(msg)

	elif data_array[0] == "borrowedreq":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		msg = chosen_item.borrowedreq(username)
		return msg
	elif data_array[0] == "borrowedby":
		if own!=username:
			return["You cannot because you are not owner",["notifs"]]
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		msg = chosen_item.borrowedby(data_array[1],data_array[2])
		announces = ["notifs"]
		print (msg)
		msg2 = msg[1]
		msg = msg[0]
		announces=announces+msg2
		return[msg,announces]
	elif data_array[0] == "returned":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		msg = chosen_item.returned(data_array[1])
		return msg
	elif data_array[0] == "listcomments":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		msg = chosen_item.listcomments()
		return ", ".join(msg)
	elif data_array[0] == "rate":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		rating = data_array[1]
		msg = chosen_item.rate(username, rating)
		return msg

	elif data_array[0] == "getrating":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		msg = chosen_item.getrating()
		return msg

	elif data_array[0] == "setstate":
		if own!=username:
			return "You cannot change state because you are not owner."
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		state_type = data_array[1]
		state = data_array[2]
		msg = chosen_item.setstate(state_type, state)
		return msg

	elif data_array[0] == "watch2":
		userDB.execute(
			"select owner,type,title,artist,genre,year from items where (owner=? and title=?)",
			(own, tit))
		data = userDB.fetchall()
		data=data[0]
		chosen_item = Item(data[0], data[1], data[2], None, data[3], data[4], data[5], 1)
		watch_method = data_array[1]
		msg = chosen_item.watch(username,watch_method)
		return msg
		
@asyncio.coroutine 
def websockethandler(websocket, path):

	print("hh")
	
	# websocket.request_headers is a dictionary like object
	print (websocket.request_headers.items())
	# following parses the cookie object
	if 'Cookie' in websocket.request_headers:
		print(http.cookies.SimpleCookie(websocket.request_headers['Cookie']))

	# get the list of ids to follow from browser
	reqlist = yield from websocket.recv()
	idlist = json.loads(reqlist)
	
	print('connected', idlist)

	if type(idlist) != list:
		idlist = [idlist]
	for myid in idlist:
		Notifications().register(websocket, myid)

	print(Notifications().observers)

	try:
		while True:
			data = yield from websocket.recv()
			try:
				print("here")
				message = json.loads(data)
				command=message['command']
				ret=None
				if command=='login':
					ret=log(message['username'],message['password'])
				elif command=="verify":
					ret=verify(message['username'],message['code'])
				elif command=="other":
					reti=other(message['username'],message['commande'],message['owner'],message['titlee'])
					print("there")
					print(reti)
					if isinstance(reti, list):
						if reti[0]=="c":
							yield from Notifications().addNotification(message['username'], ["choosei",reti[1],reti[2],reti[3]]) 
							continue
						ret=["other",reti[0]]
						print("yeah")
						yield from Notifications().addNotification("*", reti[1]) 
					else:
						print("OMG")
						ret=["other",reti]
				yield from Notifications().addNotification(message['username'], ret) 
			except Exception as e:
				print("invalid message. {} : exception: {}".format(data, str(e)))
	except Exception as e:
		print(e)
	finally:
		print('closing', idlist)
		for myid in idlist:
			Notifications().unregister(websocket, myid)
		websocket.close()


#enable logging
logging.basicConfig(level=logging.DEBUG)

ws_addr = getaddrinfo('127.0.0.1','5675', AF_INET, SOCK_STREAM)
ws_addr = ws_addr[0][4]

## Following creates a UDP handler
#udplistener = loop.create_datagram_endpoint(
#    	GetNotifications, local_addr=udp_addr )
# following creates a websocket handler
loop = asyncio.get_event_loop()
loop.set_debug(True)
ws_server = websockets.serve(websockethandler, ws_addr[0],ws_addr[1], loop = loop)

#loop.run_until_complete(ws_server)
# start both in an infinite service loop
#asyncio.async(ws_server)
#asyncio.ensure_future(ws_server)
loop.run_until_complete(ws_server)
loop.run_forever()
print("mm")