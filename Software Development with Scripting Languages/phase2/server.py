from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import threading
from user import *
from item import *
import pickle
from concurrent.futures import ThreadPoolExecutor as TPE
from concurrent.futures import Future
import pickle
from typing import List, Tuple
from random import randint

notification_sockets = []


class Server:

    @classmethod
    def parse_data(cls, data):
        return data.split(' ')

    @classmethod
    def thread_f(cls, command_socket, lock):
        user = None
        isVerify = False
        chosen_item = None
        while True:
            data = command_socket.recv(1024)
            lock.acquire()
            decoded_data = data.decode()
            data_array = decoded_data.split(' ')
            if user == None:
                if data_array[0] == "login":
                    user = User(data_array[1], None, None)
                    if user.isVerified == True:
                        isVerify = True
                        msg = "The user has logined successfully"
                    elif user.isVerified == False:
                        user = None
                        msg = "The user should be verified."
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "register":
                    user = User(data_array[1], "", data_array[2])
                    msg = "The user has registered successfully,and your verification number is:" + str(
                        user.verificationNumber)
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                else:
                    msg = "First you should login or register."
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
            elif data_array[0] == "verify":
                if user != None:
                    msg = user.verify(user.email, data_array[1])
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                    isVerify = True
                else:
                    msg = "You should be verified first."
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)

            elif isVerify:
                # owner=None, typeo=None, title=None, uniqid=None, artist=None, genre=None, year=None
                data_array = cls.parse_data(data.decode())

                if data_array[0] == "changepassword":
                    new = data_array[1]
                    old = data_array[2]
                    msg = user.changepassword(new, old)
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "isthererequestfrom":
                    toUser = data_array[1]
                    fromUser = user.email
                    msg = user.isthererequestfrom(toUser, fromUser)
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "isthereuser":
                    who = data_array[1]
                    msg = user.isthereuser(who)
                    print(msg)
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)

                elif data_array[0] == "lookup":
                    msg = user.lookup(*(data_array[1:]))
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "friend":
                    msg = user.friend(data_array[1])
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "setfriend":
                    state = data_array[2]
                    msg = user.setfriend(data_array[1], state)
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "itemlist":
                    msg = user.itemlist(data_array[1])
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)

                elif data_array[0] == "watch":
                    mode = data_array[2]
                    msg = user.watch(data_array[1], mode)
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "logout":
                    isVerify = False
                    user = None
                    chosen_item = None
                    msg = "You successfully logout from the system."
                    msg = pickle.dumps(msg)
                    command_socket.send(msg)
                elif data_array[0] == "additem":
                    created = 0
                    if len(data_array) == 6:  # uniqidsiz
                        chosen_item = Item(user.email, *(data_array[1:3]), None, *(data_array[3:]))
                        msg = "The item has created successfully with the name: " + chosen_item.title + "."
                        msg = pickle.dumps(msg)
                        command_socket.send(msg)
                        created = 1
                    elif len(data_array) == 2:  # only isbn
                        chosen_item = Item(user.email, None, None, data_array[1], None, None, None)
                        msg = "The item has created successfully with the name: " + chosen_item.title + "."
                        msg = pickle.dumps(msg)
                        command_socket.send(msg)
                        created = 1
                    else:
                        msg = "Please write in the format of additem isbn_no or additem type title artist genre year."
                        msg = pickle.dumps(msg)
                        command_socket.send(msg)
                    if created:
                        vt = sqlite3.connect('database.db')
                        userDB = vt.cursor()
                        userDB.execute("select * from watchers_for_addings where watched=?", (user.email,))
                        data = userDB.fetchall()
                        announces = []
                        for i in data:
                            strin = "Notification to " + i[0] + " that " + user.email + " added new item."
                            announces.append(strin)
                        for socks in notification_sockets:
                            msg2 = pickle.dumps(announces)
                            socks.send(msg2)
                        vt.close()

                elif data_array[0] == "chooseitem":
                    # Chose an item for operations.
                    owner = data_array[1]
                    title = data_array[2]
                    for i in range(3, len(data_array)):
                        title += " " + data_array[i]
                    print(title)
                    vt = sqlite3.connect('database.db')
                    userDB = vt.cursor()
                    userDB.execute(
                        "select owner,type,title,uniqid,artist,genre,year from items where (owner=? and title=?)",
                        (owner, title))
                    data = userDB.fetchall()
                    if data:
                        data = data[0]
                        chosen_item = Item(data[0], data[1], data[2], data[3], data[4], data[5], data[6], 1)
                        msg = "The item: " + chosen_item.title + " has chosen"
                        msg = pickle.dumps(msg)
                        command_socket.send(msg)
                    else:
                        msg = "There is no item like this."
                        msg = pickle.dumps(msg)
                        command_socket.send(msg)
                    vt.close()

                # item secmeden item a ait islemleri yapamaz.
                else:
                    if chosen_item != None:
                        if data_array[0] == "comment":
                            comment_text = " ".join(data_array[1:])
                            msg = chosen_item.comment(user.email, comment_text)
                            msg2 = msg[1]
                            msg = pickle.dumps(msg[0])
                            command_socket.send(msg)
                            for socks in notification_sockets:
                                msg2 = pickle.dumps(msg2)
                                socks.send(msg2)
                        elif data_array[0] == "locate":
                            comment_text = " ".join(data_array[1:])
                            #  since there is no user parameter, everybody can change it xd
                            msg = chosen_item.locate(comment_text)
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)
                        elif data_array[0] == "announce":
                            type = data_array[1]
                            announce_msg = " ".join(data_array[2:])
                            msg = chosen_item.annouence(type,announce_msg)
                            msgr = pickle.dumps(msg[0])
                            command_socket.send(msgr)
                            for socks in notification_sockets:
                                msg2 = pickle.dumps(msg[1])
                                socks.send(msg2)
                        elif data_array[0] == "search":
                            """kullanıcı genre year borrow:yes/no girsin"""
                            genre = data_array[1]
                            year = data_array[2]
                            borrow = data_array[3]
                            bool_borrow = False
                            if borrow == "yes":
                                bool_borrow = True
                            text = " ".join(data_array[3:])
                            msg = chosen_item.search(user.email, text, genre, year, bool_borrow)
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)
                        elif data_array[0] == "borrowedreq":
                            msg = chosen_item.borrowedreq(user.email)
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)
                        elif data_array[0] == "borrowedby":
                            msg = chosen_item.borrowedby(data_array[1],data_array[2])
                            msg2 = msg[1]
                            msg = pickle.dumps(msg[0])
                            command_socket.send(msg)
                            for socks in notification_sockets:
                                msg2 = pickle.dumps(msg2)
                                socks.send(msg2)
                        elif data_array[0] == "returned":
                            text = " ".join(data_array[1:])
                            msg = chosen_item.returned(user.email, text)
                            msg2 = msg[1]
                            msg = pickle.dumps(msg[0])
                            command_socket.send(msg)
                            for socks in notification_sockets:
                                msg2 = pickle.dumps(msg2)
                                socks.send(msg2)
                        elif data_array[0] == "listcomments":
                            msg = chosen_item.listcomments()
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)
                        elif data_array[0] == "rate":
                            rating = data_array[1]
                            msg = chosen_item.rate(user.email, rating)
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)

                        elif data_array[0] == "getrating":
                            msg = chosen_item.getrating()
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)

                        elif data_array[0] == "setstate":
                            state_type = data_array[1]
                            state = data_array[2]
                            msg = chosen_item.setstate(state_type, state)
                            msg2 = msg[1]
                            msg = pickle.dumps(msg[0])
                            command_socket.send(msg)

                        elif data_array[0] == "watch2":
                            watch_method = data_array[1]
                            msg = chosen_item.watch(watch_method)
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)

                        elif data_array[0] == "view":
                            msg = chosen_item.view(user.email)
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)

                        elif data_array[0] == "detail":
                            msg = chosen_item.detail(user.email)
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)

                        elif data_array[0] == "delete":
                            msg = chosen_item.delete()
                            msg = pickle.dumps(msg)
                            command_socket.send(msg)

                    else:
                        msg = "There is no such command."
                        msg = pickle.dumps(msg)
                        command_socket.send(msg)


            else:
                msg = "You should be verified first."
                msg = pickle.dumps(msg)
                command_socket.send(msg)
            lock.release()

    @classmethod
    def start_server(cls):
        port = 2325
        command_socket = socket(AF_INET, SOCK_STREAM)
        command_socket.bind(('', port))
        command_socket.listen()
        port = 2326
        command_socket2 = socket(AF_INET, SOCK_STREAM)
        command_socket2.bind(('', port))
        command_socket2.listen()
        lock = threading.Lock()
        while True:
            conn_socket, address = command_socket.accept()
            conn_socket2, address2 = command_socket2.accept()
            notification_sockets.append(conn_socket2)
            th = Thread(target=cls.thread_f, args=(conn_socket, lock,))
            th.start()


if __name__ == "__main__":
    Server.start_server()

