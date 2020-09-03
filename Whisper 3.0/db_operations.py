import mysql.connector as mc
import hashlib
import base64
import json
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from Cryptodome.Cipher import AES
from Cryptodome import Random

BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]
password = "852020"
class Connection():
    def startConnection(self,host):
        self.host = host
        try : 
            self.con = mc.connect(host = self.host, user = 'bot', password = 'password')
            self.c = self.con.cursor()
            print("Connection Start!")
        except :
            print("Something went wrong!")
        self.c.execute("use livechat")
    def signup(self,username,password,repassword,email, filepath):
        self.f = open(filepath, 'rb')
        self.data = self.f.read()
        if len(password) >= 8:
            if password == repassword:
                if "@" in email:
                    self.c.execute(f"select username from userinfo where username='{username}';")
                    usernameCheck = self.c.fetchall()
                    if not usernameCheck:
                        self.query = "insert into userinfo (username, email, password, profile) values (%s, %s, %s, %s)"
                        self.value = (username,email,self.myHash(password),self.data)
                        self.c.execute(self.query, self.value)
                        self.con.commit()
                        return False
                    else:
                        return "Username already exist!"
                else:
                    return "Wrong Email format!"
            else:
                return "Two password does not match!"
        else:
            return "Password have to be longer than 8 Character!"
    def login(self,username,password):
        self.c.execute(f"select username,email,profile from userinfo where username='{username}' and password='{self.myHash(password)}'")
        data = self.c.fetchall()
        if data:
            return data[0]+(True,)
        else:
            return ["Wrong Username or password!",False]
    def myHash(self,ps):
        hashPassword = hashlib.sha1(ps.encode("utf-8"))
        encrypt = hashPassword.hexdigest()
        return encrypt
    # def reciever(self,username):
    #     self.username = username
    #     while True:
    #         try:
    #             # msg = bytes.decode(self.decrypt(self.client.recv(self.bufsiz), password))
    #             msg = bytes.decode(self.client.recv(self.bufsiz))
    #             print(msg)
    #             msg = json.loads(msg)
    #             if self.username ==  msg["to"]:
    #                 return msg
    #         except OSError:
    #             print('bye')
    #             break
    def connectServer(self,username):
        host = self.host
        port = 33000
        self.bufsiz = 1024
        self.msgFrom = username
        addr = (host, port)
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect(addr)
        self.client.send(self.encrypt(self.msgFrom,password))
        return self.client
    def encrypt(self,raw, password):
        private_key = hashlib.sha256(password.encode("utf-8")).digest()
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
    def decrypt(self,enc, password):
        private_key = hashlib.sha256(password.encode("utf-8")).digest()
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))
    def getAllUser(self):
        self.c.execute("select username,profile from userinfo")
        return self.c.fetchall()
    def closeConnection(self,data):
        self.client.send(self.encrypt(data,password))
        self.client.close()
        return True
