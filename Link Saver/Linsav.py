import webbrowser
import sys
import os
import mysql.connector as mc

class menu:
    def __init__(self):
        self.menulist()
    def choose(self,num):
        os.system("cls")
        if num=="1":
            self.new()
        elif num=="2":
            self.display()
        elif num=="3":
            self.ls()
        else :
            sys.exit()
    def menulist(self):
        os.system("cls")
        print(form.format("New URL",": (Type 1)"))
        print(form.format("My URL",": (Type 2)"))
        print(form.format("Open URL",": (Type 3)"))
        print(form.format("Exit",": (Type Anything)"))
        self.choose(input())
    def display(self,tfc = True):
        cur.execute(query[4])
        data = cur.fetchall()
        print(form1.format("ID","Info","URL"))
        for i in range(len(data)):
            print(form1.format(data[i][0],data[i][2],data[i][1]))
        if not data:
            print("It is empty!\n")
            input()
            self.menulist()
        else :
            print()
            if tfc:
                self.dele()
    def new(self):
        tf = True
        url = input("Enter new URL : ")
        name = input("Enter URL Info : ")
        cur.execute(query[4])
        data = cur.fetchall()
        for i in range(len(data)):
            if data[i][1] == url:
                tf = False
        if tf:
            num = len(data)+1
            cur.execute(query[5].format(num,url,name))
            con.commit()
            print("Done!")
        else :
            print("This URL already exist!")
        input("Press Anything to go back!")
        self.menulist()
    def dele(self,tbn="urls"):
        print("Press * to delete all")
        p = input("Press Anything to go back! And to remove URL press r : ")
        if p=="r":
            while True:
                print("Press 0 to go back!")
                id = input("Enter ID of URL you wanna remove : ")
                if id != "0":
                    cur.execute(query[6].format(tbn,id))
                    cur.execute(query[4])
                    data = cur.fetchall()
                    num = len(data)
                    for j in range(num):
                        cur.execute(query[7].format(j+1,data[j][1]))
                    con.commit()
                else :
                    self.menulist()
        elif p=="*":
            pp = input("Press y if you are sure... else press anything : ")
            if pp == "y":
                cur.execute("delete from urls")
                con.commit()
                self.menulist()
            else:
                self.menulist()
        else:
            self.menulist()
    def ls(self):
        print("My URL list\n\nTo curstom open url press c...")
        print("Press o to open all...\nPress anythings to go back...\n")
        self.display(False)
        c = input()
        if c=="o":
            cur.execute("select urln from urls")
            data = cur.fetchall()
            for i in range(len(data)):
                webbrowser.open(data[i][0])
            print("Done!")
            input()
        elif c=="c":
            print("Enter ID of url you want to open\nEg. 1,2,3,4...")
            nid = list(map(int,input().split(sep=",")))
            for j in nid:
                cur.execute("select urln from urls where id = {}".format(j))
                curl = cur.fetchall()
                webbrowser.open(curl[0][0])
            self.menulist()
        else :
            self.menulist()
while True:
    print("SQL Server")
    user = input("Enter User Name : ")
    passworrd = input("Password : ")
    try:
        con = mc.connect(host = "localhost",user = user,password=passworrd)
        break
    except:
        os.system("cls")
        print("Wrong Username or Passoword!")
cur = con.cursor()
query = ["show databases","create database myurl","use myurl","""create table {} (id int primary key,urln varchar(500),ne varchar(100));""",
        "select * from urls","""insert into urls values({},"{}","{}");""","delete from {} where id = {}","""update urls set id = {} where urln="{}" """]
cur.execute(query[0])
dbs = cur.fetchall()
if ("myurl",) not in dbs:
    for i in range(1,4):
        if i==3:
            cur.execute(query[i].format("urls"))
            break
        cur.execute(query[i])
cur.execute(query[2])
form = "{:<10}{}"
form1 = "{:<7}->{:<20}{}"
start = menu()


