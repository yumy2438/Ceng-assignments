from socket import *
from threading import Thread
import pickle

class Client():
	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 2325
		self.s = socket(AF_INET, SOCK_STREAM)
		self.s.connect((self.host, self.port))
		self.email = "None"
		self.host2 = '127.0.0.1'
		self.port2 = 2326
		self.s2 = socket(AF_INET, SOCK_STREAM)
		self.s2.connect((self.host2, self.port2))

	def func1(self,command):
		data_array = command.split(' ')
		if self.email=="None":
			if data_array[0]=="register" or data_array[0]=="login":
				self.email=data_array[1]
		self.s.send(command.encode("ascii"))
		data = self.s.recv(1024)
		data = pickle.loads(data)
		return data

	def func2(self):
		while True:
			data = self.s2.recv(1024)
			data = pickle.loads(data)
			for dat in data:
				if type(dat)==str:
					data_array = dat.split(' ')
					if len(data_array)>2 and data_array[2]==self.email:
						print (dat)
						break





