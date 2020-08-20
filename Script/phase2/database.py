import sqlite3
import os
import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
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
conn.commit()
conn.close()
