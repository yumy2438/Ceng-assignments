from client import *
from time import sleep


def senaryo1():
    # simdi itemlarına bakalim.
    print("client1:", client1.func1("register esra e e"), "\n")
    print("client1:", client1.func1("verify 111111"), "\n")
    print("client1:", client1.func1("changepassword k e"), "\n")
    print("client1:", client1.func1("changepassword e k"), "\n")
    # baska userla ilgili islem yapmadan once olusmasını bekle..
    while True:
        answer = client1.func1("isthereuser soner")
        if answer == "t":
            break
    #  itemlarına bakalim.
    print("client1:", client1.func1("itemlist soner"), "\n")
    print("client1:", client1.func1("friend soner"), "\n")
    sleep(2)
    print("client1:", client1.func1("itemlist soner"), "\n")
    print("client1:",client1.func1("watch soner borrow"),"\n")
    print("client1:",client1.func1("watch soner detail"),"\n")
    print("client1:", client1.func1("additem f f f f f"), "\n")
    print("client1:", client1.func1("additem g g g g g"), "\n")


def senaryo2():
    print("client2:", client2.func1("register soner s s"), "\n")
    print("client2:", client2.func1("verify 111111"), "\n")
    #  item ekledik.
    print("client2:", client2.func1("additem a a s a a"), "\n")
    print("client2:", client2.func1("lookup [esra,soner,hakan]"), "\n")
    print("client2:", client2.func1("logout"), "\n")
    print("client2:", client2.func1("login soner s s"), "\n")
    #  wait request from esra.
    while True:
        answer = client2.func1("isthererequestfrom esra")
        if (answer == "t"):
            break
    print("client2:", client2.func1("setfriend esra friend"), "\n")
    sleep(2)
    print("client2:", client2.func1("additem b b b b b"), "\n")
    print("client2:", client2.func1("additem c c c c c"), "\n")
    print("client2:", client2.func1("additem d d d d d"), "\n")
    print("client2:", client2.func1("additem e e e e e"), "\n")
    print("client2:", client2.func1("chooseitem soner e"), "\n")
    print("client2:", client2.func1("announce friend message"), "\n")



client1 = Client()
client2 = Client()

th1 = Thread(target=client1.func2, args=())
th1.start()
th2 = Thread(target=client2.func2, args=())
th2.start()
th11 = Thread(target=senaryo1, args=())
th21 = Thread(target=senaryo2, args=())
th11.start()
th21.start()
