from gui import *
from tkinter import *
from db_operations import *
class Whisper(Tk):
    def __init__(self):
        super().__init__()
        self.config(bg="#ffffff")
        self.state("zoomed")
        self.dbo = Connection()
        self.dbo.startConnection(input("Server IP: "))
        LoginFrame(self).pack(pady=(40,0))
    def signup(self,username,password,repassword,email,filepath):
        return self.dbo.signup(username,password,repassword,email,filepath)
    def login(self,username,password):
        return  self.dbo.login(username,password)
    def connectServer(self,username):
        client = self.dbo.connectServer(username)
        # self.recThread = Thread(target = self.dbo.reciever,args=(username,))
        # self.recThread.start()
        return client
    def getAllUser(self):
        return self.dbo.getAllUser()
    def onClosing(self):
        data = {"to":"//clientDisconnect"}
        if self.dbo.closeConnection(json.dumps(data)):
            root.quit()

root = Whisper()
root.protocol("WM_DELETE_WINDOW", root.onClosing)
root.mainloop()