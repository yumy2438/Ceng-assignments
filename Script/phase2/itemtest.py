from client import *
from time import sleep


def senaryo1():
    print("esra:",client1.func1("login esra e e"))
    print("esra:",client1.func1("chooseitem artun h"))
    #  artunun h kitabına yorum yap, ama arkadaş degilsiniz. o yüzden yapaMAyacak.
    print("esra:",client1.func1("comment nice book."))
    print("esra:", client1.func1("chooseitem soner b"))
    print("esra:",client1.func1("borrowedreq"))
    sleep(2)
    print("esra:", client1.func1("rate 5"))
    print("esra:",client1.func1("search a a a"))
    print("esra:",client1.func1("view"))
    print("esra:", client1.func1("detail"))
    print("esra:",client1.func1("chooseitem esra f"))
    print("esra:",client1.func1("delete"))
    print("esra:",client1.func1("chooseitem soner c"))
    sleep(1)
    print("esra:",client1.func1("comment i like it."))
    print("esra:",client1.func1("comment but it is too short."))
    print("esra:",client1.func1("comment however i recommended it."))
    print("esra:",client1.func1("comment reallyy."))
def senaryo2():
    print("soner:",client2.func1("login soner s s"))
    print("soner:",client2.func1("chooseitem soner a"))
    print("soner:",client2.func1("setstate comment closefriends"))
    print("soner:",client2.func1("setstate borrow closefriends"))
    print("soner:",client2.func1("chooseitem soner b"))
    print("soner:",client2.func1("listcomments"))#for a
    while True:
        st1 = client2.func1("borrowedby esra 2")
        st2 = client2.func1("borrowedby artun 2")
        #biri borrow edesiye kadar bekle.
        if st1 != "You cannot borrow this item.":
            print("soner:",st1)
            break
        elif st2 != "You cannot borrow this item.":
            print("esra:", st1)
            break
    print("soner:",client2.func1("getrating"))

def senaryo3():

    print("artun:",client3.func1("login artun a a"))
    print("artun:",client3.func1("chooseitem soner a"))
    print("artun:", client3.func1("comment i like it my close friend."))
    print("artun:", client3.func1("chooseitem soner b"))
    print("artun:", client3.func1("borrowedreq"))
    sleep(2)
    print("artun:", client3.func1("rate 3"))
    print("artun:",client3.func1("chooseitem artun h"))
    print("artun:",client3.func1("locate raf 2"))
    print("artun:", client3.func1("chooseitem soner c"))
    print("artun:",client3.func1("watch2 detail"))

    #print("artun:", client3.func1())



client1 = Client()
client2 = Client()
client3 = Client()
th1 = Thread(target=client1.func2, args=())
th1.start()
th2 = Thread(target=client2.func2, args=())
th2.start()
th3 = Thread(target=client3.func2,args=())
th3.start()
th11 = Thread(target=senaryo1, args=())
th21 = Thread(target=senaryo2, args=())
th31 = Thread(target=senaryo3, args=())
print("artun:",client3.func1("register artun a a"))
print("artun:",client3.func1("verify 111111"))
print("artun:",client3.func1("additem h h h h h"))
print("artun:",client3.func1("additem i i i i i"))
print("artun:",client3.func1("friend soner"))
print("artun:",client3.func1("logout"))
print("soner:",client2.func1("login soner s s"))
print("soner:",client2.func1("setfriend artun friend"))
print("soner:",client2.func1("setfriend artun closefriend"))
print("soner:",client2.func1("logout"))
print("-------------------")
th11.start()
th21.start()
th31.start()