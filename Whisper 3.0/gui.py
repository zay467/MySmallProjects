from tkinter import * 
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from PIL import Image,ImageTk # pillow
from threading import Thread
import json
from Cryptodome.Cipher import AES #pycryptodomex
from Cryptodome import Random
import hashlib
import base64

bg = "#333333"
fg = "#ffffff"
wtf = True
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]
password = "852020"
bufsize = 1024
usernameG = ""
toUsernameG = ""
def reciever():
    while True:
        try:
            msg = bytes.decode(decrypt(client.recv(bufsize), password))
            # msg = bytes.decode(self.parent.master.client.recv(1024))
            msg = json.loads(msg)
            if usernameG ==  msg["to"]:
                if msg['from'] == toUsernameG:
                    Label(innerChatF,text=msg['msg'],bg=bg,fg=fg).pack(side='top',anchor='w',pady=(0,10))
                else :
                    mb.showinfo(title="Whisper",message=f"{msg['from']} is whispering to you.")
                    MsgList.append(msg)
            elif msg["to"] == "offline":
                mb.showinfo(title="Whisper",message=msg['msg'])
            elif msg["to"] == "aiReply":
                print(msg['msg'])
                # if msg["from"] == self.toUsername:
                Label(innerChatF,text=msg['msg'],bg=bg,fg=fg).pack(side='top',anchor='w',pady=(0,10))
                # Label(self.innerChatF,text=msg['msg'],bg=bg,fg=fg).pack(side='top',anchor='w',pady=(0,10))
            elif msg["to"] == 'Group':
                if msg["from"]!=usernameG and toUsernameG=='Group':
                # if msg['to'] == self.toUsername:
                    Label(innerChatF,text=msg["from"]+" : "+msg['msg'],bg=bg,fg=fg).pack(side='top',anchor='w',pady=(0,10))
        except OSError:
            break
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
class LoginFrame(Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent)
        self.config(width=600,height=800,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 2, borderwidth = 2)
        self.loginLabel = Label(self,text="Login",fg=fg,bg=bg)
        self.loginLabel.grid(row=0,column=0,columnspan=2,ipadx=20,pady=(10,30))
        self.signupLabel = Label(self,text="Signup",fg=bg)
        self.signupLabel.grid(row=0,column=2,columnspan=2,ipadx=20,pady=(10,30))
        self.signupLabel.bind("<1>",self.toSignup)

        Label(self,text="Username",fg=bg).grid(row=1,column=0,columnspan=2,padx=20,pady=(0,20))
        self.usernameEnt = Entry(self,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.usernameEnt.grid(row=1,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Password",fg=bg).grid(row=2,column=0,columnspan=2,padx=20,pady=(0,20))
        self.passwordEnt = Entry(self,relief=FLAT,show="*",highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.passwordEnt.grid(row=2,column=2,columnspan=2,pady=(0,30),padx=(0,10))

        self.loginBtn = Label(self, text = "Login", relief = "flat", bg = bg, fg = fg)
        self.loginBtn.grid(row=3,column=1,columnspan=2,pady=(0,30),padx=(30,10),ipadx=20)
        self.loginBtn.bind('<1>',self.login)
        
        Label(self,text="Whisper..",font=("Pacifico",20),fg="teal").grid(row=4,column=1,columnspan=2,pady=(0,30))
    def login(self,e):
        username = self.usernameEnt.get()
        password = self.passwordEnt.get()
        data = self.parent.login(username,password)
        if data[-1]:
            global client,usernameG
            client = self.parent.connectServer(data[0])
            self.pack_forget()
            usernameG = data[0]
            HomeFrame(self.parent,data[0],data[1],data[2],client).pack(pady=(40,0))
        else:
            mb.showerror(title="Whisper",message=data[0])
    def toSignup(self,e):
        self.pack_forget()
        SignupFrame(self.parent).pack(pady=(40,0))
class SignupFrame(Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent)
        self.filepath = 'user.png'
        self.config(width=600,height=800,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 2, borderwidth = 2)
        self.loginLabel = Label(self,text="Login",fg=bg)
        self.loginLabel.grid(row=0,column=0,columnspan=2,ipadx=20,pady=(10,20))
        self.loginLabel.bind('<1>',self.toLoginin)
        self.signupLabel = Label(self,text="Signup",fg=fg,bg=bg)
        self.signupLabel.grid(row=0,column=2,columnspan=2,ipadx=20,pady=(10,20))

        Label(self,text="Profile",fg=bg).grid(row=1,column=0,columnspan=2,padx=20,pady=(0,20))
        self.profile = Label(self, text = "Add Image", relief = "flat", bg = bg, fg = fg)
        self.profile.grid(row=1,column=2,columnspan=2,pady=(0,20),ipadx=32,padx=(0,10))
        self.profile.bind("<1>",self.browseImage)

        Label(self,text="Username",fg=bg).grid(row=2,column=0,columnspan=2,padx=20,pady=(0,20))
        self.usernameEnt = Entry(self,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.usernameEnt.grid(row=2,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Password",fg=bg).grid(row=3,column=0,columnspan=2,padx=20,pady=(0,20))
        self.passwordEnt = Entry(self,relief=FLAT,show="*",highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.passwordEnt.grid(row=3,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Re-password",fg=bg).grid(row=4,column=0,columnspan=2,padx=15,pady=(0,20))
        self.repasswordEnt = Entry(self,relief=FLAT,show="*",highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.repasswordEnt.grid(row=4,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Email",fg=bg).grid(row=5,column=0,columnspan=2,padx=20,pady=(0,20))
        self.emailEnt = Entry(self,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.emailEnt.grid(row=5,column=2,columnspan=2,pady=(0,30),padx=(0,10))

        self.signupbtn = Label(self, text = "Submit", relief = "flat", bg = bg, fg = fg)
        self.signupbtn.grid(row=6,column=1,columnspan=2,pady=(0,30),padx=(30,10),ipadx=20)
        self.signupbtn.bind("<1>",self.signup)

        Label(self,text="Whisper..",font=("Pacifico",20),fg="teal").grid(row=7,column=1,columnspan=2,pady=(0,30))
    def signup(self,e):
        username = self.usernameEnt.get()
        password = self.passwordEnt.get()
        repassword = self.repasswordEnt.get()
        email = self.emailEnt.get()
        filepath = self.filepath
        msg = self.parent.signup(username,password,repassword,email,filepath)
        if msg:
            mb.showerror(title="Signup Error!",message=msg)
        else:
            mb.showinfo(title="Whisper",message="Signup Successful!")
            self.toLoginin(e)

    def toLoginin(self,e):
        self.pack_forget()
        LoginFrame(self.parent).pack(pady=(40,0))
    
    def browseImage(self,e):
        self.filepath = fd.askopenfilename()
class user(Frame):
    def __init__(self, parent,welcome,rightframe, username,profile,owner):
        self.parent = parent
        self.username= username
        self.profile = profile
        self.welcome = welcome
        self.rightFrame = rightframe
        super().__init__(parent, cursor = 'hand2')  
        f = open('temp_profile.png', 'wb')
        f.write(self.profile)
        f.close()
        # self.config(relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth = 1)
        # self.pp_img = PhotoImage(file = 'temp_profile.png')
        self.img = Image.open(r'temp_profile.png')
        self.name = Label(self, text = self.username)
        if owner:
            self.new = self.img.resize((60,60))
        else:
            self.new = self.img.resize((30,30))    
            self.name.bind("<Button-1>",lambda event,name = self.username: self.click(event,name))
        self.pp_img = ImageTk.PhotoImage(self.new)
        Label(self, image = self.pp_img).grid(row=0,column=0)
        self.name.grid(row=0,column=1)
        self.bind("<Enter>",self.lightUp)
        self.bind("<Leave>",self.lightOut)
        
    def lightUp(self,e):
        self.name.config(fg="teal")
    def lightOut(self,e):
        self.name.config(fg=bg)
    def click(self,e,username):
        global wtf,toUsernameG
        if wtf:
            self.welcome.grid_forget()
            ChatFrame(self.rightFrame,username).grid(column=2,row=0,columnspan=4,rowspan=6)
            toUsernameG = username
            Thread(target=reciever).start()
            wtf = False
        else :
            self.grid_forget()
            toUsernameG = username
            ChatFrame(self.rightFrame,username).grid(column=2,row=0,columnspan=4,rowspan=6)
    
class HomeFrame(Frame):
    def __init__(self,parent,username,email,profile,client):
        self.parent = parent
        self.client = client
        self.username = username
        super().__init__(parent)
        self.config(width=800,height=450,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 2, borderwidth = 2)
        # self.grid_propagate(0)
        self.rightFrame = Frame(self)
        self.rightFrame.grid(column=2,row=0,columnspan=4,rowspan=6)
        self.welcome = Welcome(self.rightFrame,username)
        Label(self,text="Whisper..",font=("Pacifico",20),fg="teal").grid(row=0,column=0,sticky="W",padx=(0,15))
        user(self,self.welcome,self.rightFrame,username,profile,True).grid(row=1,column=0,columnspan=2,sticky="W",pady=(0,15))
        # NavFrame(self).grid(row=2,column = 0,columnspan=2,rowspan=4)
        self.friendList = Frame(self)
        self.cv = Canvas(self.friendList,width=100)
        self.sbar = Scrollbar(self.friendList,command=self.cv.yview)
        self.cv.config(yscrollcommand = self.sbar.set)
        self.f = Frame(self.cv)
        self.cv.create_window((0,0), window = self.f)
        
        self.cv.pack(side = 'left',fill='both')
        self.sbar.pack(side = 'right', fill = 'y')
        self.parent.bind("<Configure>", lambda e: self.cv.config(scrollregion = self.cv.bbox('all')))
        # print(self.parent)
        self.friendList.grid(row=2,column = 0,columnspan=2,rowspan=3)
        for i in self.parent.getAllUser():
            if i[0]==username:
                continue
            else:
                user(self.f,self.welcome,self.rightFrame,i[0],i[1],False).pack(side="top",anchor="w")
        
        # user(self.f,self.welcome,self.rightFrame,"Group",self.gpImgData,False).pack(side="top",anchor="w")
        self.gpImg = open('group.png', 'rb')
        self.gpImgData = self.gpImg.read()
        self.opImg = open('operator.png', 'rb')
        self.opImgData = self.opImg.read()
        user(self.f,self.welcome,self.rightFrame,"HelpCenter",self.opImgData,False).pack(side="top",anchor="w")
        self.welcome.grid(column=2,row=0,columnspan=4,rowspan=6)
        user(self.f,self.welcome,self.rightFrame,"Group",self.gpImgData,False).pack(side="top",anchor="w")
        self.welcome.grid(column=2,row=0,columnspan=4,rowspan=6)

class Welcome(Frame):
    def __init__(self,parent,username):
        self.parent = parent
        super().__init__(parent)
        self.config(width=700,height=450,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth = 1)
        self.pack_propagate(0)
        Label(self,text=f"Welcome {username}!",font=("Pacifico",24),fg="teal").pack(side="top",anchor='e')
        Label(self,text="Help Center With AI -").pack(side="top",anchor="e")
        Label(self,text="Messages are Encrypted -").pack(side="top",anchor="e")
        Label(self,text="Messages will not be stored in our database -").pack(side="top",anchor="e")
        Label(self,text="Contact Us",font=("Pacifico",22),fg="teal").pack(side="bottom",anchor="w")
        Label(self,text="- kz3@enterprise.com").pack(side="bottom",anchor="w")
        Label(self,text="- whisperXkz3.com").pack(side="bottom",anchor="w")
        Label(self,text="- Developed By KZ3").pack(side="bottom",anchor="w")
        
MsgList = []
# innerChatF = Frame()
class ChatFrame(Frame):
    def __init__(self,parent,toUsername):
        global innerChatF
        self.parent = parent
        self.toUsername = toUsername
        super().__init__(parent)
        self.config(width=700,height=450,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth = 1)
    
        Label(self,text=self.toUsername,font=14).grid(row=0,column=0,columnspan=3)

        self.chatF = Frame(self,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth = 1)
        self.cv = Canvas(self.chatF,width=670,height=350)
        self.sbar = Scrollbar(self.chatF,command=self.cv.yview)

        self.cv.config(yscrollcommand = self.sbar.set)
        innerChatF = Frame(self.cv)
        self.cv.create_window((0,0), window = innerChatF)
        Label(innerChatF,text="").pack(side="top",padx=330)
        # print(self.parent.master.master)
        self.cv.pack(side = 'left',fill='both',expand=True)
        self.sbar.pack(side = 'right', fill = 'y')
        self.parent.master.master.bind("<Configure>", lambda e: self.cv.config(scrollregion = self.cv.bbox('all')))
        self.chatF.grid(row=1,column=0,columnspan=3,rowspan=3)
        self.tb=Text(self,width=60,height=4,exportselection=0,wrap=CHAR,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth = 1)
        self.tb.grid(row=4,column=0,columnspan=2)
        self.send = Label(self,text="Send",font=("Pacifico",17),fg="teal")
        self.send.bind('<Button-1>', self.send_msg)
        # self.send.bind("<Enter>",self.send_msg)
        self.send.grid(row=4,column=2)
        # self.recThread = Thread(target = self.reciever,args=(self.parent.master.username,))
        # self.recThread.start()
        self.checkExistingMsg(self.toUsername)

    def send_msg(self, e):
        msg = self.tb.get('1.0', 'end-1c')
        Label(innerChatF,text=msg,bg=bg,fg=fg).pack(side='top',anchor='e',pady=(0,10))
        data = json.dumps({'to':self.toUsername, 'msg':msg, 'from':self.parent.master.username})
        self.parent.master.client.send(encrypt(data,password))
        self.tb.delete(1.0,"end-1c")

    def displayMsg(self,msg):
        Label(innerChatF,text=msg,bg=bg,fg=fg).pack(side='top',anchor='w',pady=(0,10))

    def checkExistingMsg(self,toUsername):
        for i,j in enumerate(MsgList):
            if j['from'] == toUsername:
                self.displayMsg(MsgList.pop(i)['msg'])