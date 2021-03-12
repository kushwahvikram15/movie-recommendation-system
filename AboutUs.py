from tkinter import *
from tkinter import messagebox
import pymongo
from tkinter.font import Font
from template import Template
class about(Template):
    def __init__(self,lst,master,userr_coll, userr_name):
        self.master = master
        self.lst = lst
        self.userr_coll = userr_coll
        self.userr_name = userr_name
        Template.__init__(self,self.lst,self.master)
        self.master.title('about_us')
        print(type(self.userr_coll))

    def show_movie(self, ):
        from movies import movie
        from info import userinfo
        self.dict = self.userr_coll.aggregate([{'$match': {'_id': self.userr_name}}])
        x = list(self.dict)[0]

        docs = x['movie']
        if len(docs) == 0:
            c = userinfo(self.master, self.lst, self.userr_coll, self.userr_name)

        else:
            c = movie(self.lst, self.master, self.userr_coll, self.userr_name)
        self.destroy()

    def blogg(self):
        from blogging import blog
        c = blog(self.lst, self.master, self.userr_coll, self.userr_name)
        self.destroy()

    def homee(self):
        from Home import Application
        self.no = 2
        c = Application(self.master, self.lst,self.no,self.userr_coll,self.userr_name)
        self.destroy()

    def user(self):
        from user_profile import userpf
        c = userpf(self.lst, self.master,self.userr_coll,self.userr_name)
        self.destroy()








