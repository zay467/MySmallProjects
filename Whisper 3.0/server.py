import base64
import hashlib
import os
import json
import mysql.connector as mc
from socket import AF_INET, socket, SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
from Cryptodome.Cipher import AES
from Cryptodome import Random
from covid import Covid
import requests

# For AES Encryptiion
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]
# We use the symmetric Encryption So this password have to be the same in both client and server
password = "852020"

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))  

def acceptIncomingConnection():
    while True:
        client , clientAddr = server.accept()
        print("%s : %s has connected."% clientAddr)
        addresses[client] = clientAddr
        # print(client) # the whole data of connection
        # print(addresses[client]) # client IP addr
        t = Thread(target=handleClient,args=(client,))
        t.start()
def handleClient(client):
    # global conversation, reportTF, feedbackTF, suggestionTF,
    conversation = []
    reportTF = False
    feedbackTF = False
    suggestionTF = False
    covidTF = False
    weatherTF = False
    name = bytes.decode(decrypt(client.recv(bufsiz),password))
    clients[client] = name
    while True:
        connetionStart = bytes.decode(decrypt(client.recv(bufsiz),password))
        data = json.loads(connetionStart)
        if data["to"] == "//clientDisconnect":
            client.close()
            conversation = []
            reportTF = False
            feedbackTF = False
            suggestionTF = False
            del clients[client]
            break
        elif data["to"] =="HelpCenter":
            conversation.append(data["msg"])
            if data["msg"] == "Restart":
                aiReply = {"to":"aiReply","msg":"AI has restarted.",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                conversation = []
                reportTF = False
                feedbackTF = False
                suggestionTF = False
            if reportTF:
                # Db Insert
                aiReply = {"to":"aiReply","msg":"Have a great day. Bye!",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                conversation = []
                reportTF = False
            if feedbackTF:
                #db insert
                aiReply = {"to":"aiReply","msg":"Thank you for your Feedback!",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                conversation = []
                feedbackTF = False
            if suggestionTF:
                # db insert
                aiReply = {"to":"aiReply","msg":"Your suggestion are very much appreciated!",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                conversation = []
                suggestionTF = False
            if covidTF:
                covid = Covid()
                try:
                    cData = covid.get_status_by_country_name(conversation[2])
                    aiReply = {"to":"aiReply","msg":f"Country : {cData['country']}\nConfirmed : {cData['confirmed']}\nActice : {cData['active']}\nDeath : {cData['deaths']}\nRecovered : {cData['recovered']}",'from':"HelpCenter"}
                    client.send(encrypt(json.dumps(aiReply),password))
                except ValueError:
                    aiReply = {"to":"aiReply","msg":"Country does not exist!",'from':"HelpCenter"}
                    client.send(encrypt(json.dumps(aiReply),password))
                except :
                    aiReply = {"to":"aiReply","msg":"Server is offline!",'from':"HelpCenter"}
                    client.send(encrypt(json.dumps(aiReply),password))
                conversation = []
                covidTF = False
            if weatherTF:
                try:
                    addr = "https://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s"%(conversation[2],appid)
                    w = requests.get(url = addr)
                    data = w.json()
                    temp = data["main"]["temp"]
                    weat = data["weather"][0]["description"]
                    humi = data["main"]["humidity"]
                    name = data["name"]
                    aiReply = {"to":"aiReply","msg":f"Name : {name}\nTemperature : {temp}\nDescription : {weat}\nHumidity : {humi}",'from':"HelpCenter"}
                    client.send(encrypt(json.dumps(aiReply),password))
                except KeyError:
                    aiReply = {"to":"aiReply","msg":"City does not exist!",'from':"HelpCenter"}
                    client.send(encrypt(json.dumps(aiReply),password))
                except : 
                    aiReply = {"to":"aiReply","msg":"Server is offline!",'from':"HelpCenter"}
                    client.send(encrypt(json.dumps(aiReply),password))
                conversation = []
                weatherTF = False

            if len(conversation)==1 and conversation[0]:
                aiReply = {"to":"aiReply","msg":"Hi! This is your assistant Echo. How can I help you?\nType 'Report' for Report.\nType 'Feedback' for Feedback.\nType 'Suggestion' for Suggestion\nIf you come accross some error, please sent 'Restart'.",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                aiReply = {"to":"aiReply","msg":"If you want to know about Covid-19 cases, Type 'covid-19'.\nOr if you want to know about weather, Type 'weather'.",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
            if len(conversation)==2 and conversation[1]=="Report":
                aiReply = {"to":"aiReply","msg":"Please Type who do you want to report and why?(Please type username specifically)",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                reportTF = True
            if len(conversation)==2 and conversation[1]=="Feedback":
                aiReply = {"to":"aiReply","msg":"How is our app?",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                feedbackTF = True
            if len(conversation)==2 and conversation[1]=="Suggestion":
                aiReply={"to":"aiReply","msg":"What is your Suggestion?",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                suggestionTF = True
            if len(conversation)==2 and conversation[1] == "covid-19":
                aiReply={"to":"aiReply","msg":"Which country do you want to know?",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                covidTF = True
            if len(conversation)==2 and conversation[1]== "weather":
                aiReply={"to":"aiReply","msg":"Which city do you want to know?",'from':"HelpCenter"}
                client.send(encrypt(json.dumps(aiReply),password))
                weatherTF = True
        elif data["to"] =="Group":
            for toAllUser in clients:
                # if data['from'] == name:
                #     print(toAllUser)
                #     print(name)
                #     pass
                # else:
                    toAllUser.send(encrypt(json.dumps(data),password))
        else:
            for onlineList in clients:
                if clients[onlineList]==data["to"]:
                    onlineList.send(encrypt(json.dumps(data),password))
                    # onlineList.send(json.dumps(data).encode('utf-8'))
                    break
            else:
                offline = {"to":"offline","msg":"This user is offline"}
                offline = json.dumps(offline)
                client.send(encrypt(offline,password))
        

clients = {}
addresses = {}

while True:
    user = input("Enter Database username : ")
    dbpassword = input("Enter Password : ")
    try : 
        con = mc.connect(host="localhost",user=user,password=dbpassword)
        os.system('cls')
        break
    except :
        os.system('cls')
        print("Wrong Username or Password!")
appid = input("Enter Open Weather AppId (Press Enter if you don't want to get weather Data) : ")
cur = con.cursor()
cur.execute("show databases")
alldb = cur.fetchall()
if ("livechat",) not in alldb:
    cur.execute("create database livechat")
    cur.execute("use livechat")
cur.execute("use livechat")

cur.execute("show tables")
alltb = cur.fetchall()
if ("userinfo",) not in alltb:
    cur.execute("create table userinfo (id int primary key not null AUTO_INCREMENT, username varchar(100) not null, email varchar(100) not null, password varchar(50) not null,profile MEDIUMBLOB not null);")

cur.execute("select user from mysql.user")
alluser = cur.fetchall()
if ("bot",) not in alluser:
    cur.execute("create user bot@'%' identified by 'password';")
    cur.execute("GRANT ALL PRIVILEGES ON livechat.* TO 'bot'@'%';")

host = ""
port = 33000
bufsiz = 1024
addr = (host,port)
server = socket(AF_INET,SOCK_STREAM)
server.bind(addr)
print("Server IP : "+gethostbyname(gethostname()))
if __name__ == "__main__":
    server.listen(5)
    acceptThread = Thread(target=acceptIncomingConnection)
    acceptThread.start()
    acceptThread.join()
    server.close()