import pymongo
from tkinter import *
from PIL.ImageTk import PhotoImage
import datetime
from tkinter import messagebox
from tkinter.font import Font
from template import Template
from recSys import Rec
from PIL import ImageTk,Image
import os
date = datetime.datetime.now().date()
date = str(date)

class Application():
    def __init__(self,master,lst,no,userr_coll,userr_name):
        self.no = no
        self.userr = userr_name
        self.userr_coll = userr_coll
       
        self.client = pymongo.MongoClient("localhost",27017)#mongodb+srv://vikram:vikram15@cluster0.auc7j.mongodb.net/entertainment?retryWrites=true&w=majority
        self.db = self.client.entertainment
        self.lst = []
        self.master = master
        self.my_font = Font(family='Ink Free', size=55, weight='bold')
        self.master.geometry("{0}x{1}+0+0".format(1536,1536))
        self.master.title("home")
        self.top = Frame(self.master, height=100, width=1536, bg='#5e615e')
        self.top.place(x=0, y=0)
        Label(self.master, text='Movie Recommendation', bg='#5e615e',fg='#f02e2e', font=self.my_font).place(x=350, y=0)
        self.f = Frame(self.master, height=5, width=1536, bg='red')
        self.f.place(x=0, y=80)
        self.f = Frame(self.master, height=5, width=1536, bg='red')
        self.f.place(x=0, y=745)
        self.footer = Frame(self.master, height=100, width=1536, bg='#5e615e')
        self.footer.place(x=0, y=750)
        self.bottom = Frame(self.master, height=660, width=1536, bg='#2b2929')
        self.bottom.place(x=0, y=85)


        #### If user visit first time on home page after login then self.no is 1.####

        if self.no==1:
            self.userr = 'unknown'
            img = Image.open('images/movies_image.png')
            img = img.resize((400, 300), Image.ANTIALIAS)
            self.use = PhotoImage(file="images/movi.png")
            self.movies_image = PhotoImage(img)
            self.user_icon = PhotoImage(file="images/user.png")
            self.user_name = PhotoImage(file="images/s_username.png")
            self.user_lock = PhotoImage(file="images/s_lock.png")
            self.username = StringVar()
            self.password = StringVar()
            self.c_password = StringVar()
            # try:
            self.client = pymongo.MongoClient(f"localhost",27017)
            self.userr_db = self.client[f'{self.userr}']

            # except Exception as e:
            #     messagebox.showinfo("Info", e)
            self.logsign = Frame(self.top, height=50, width=1536, bg='#5e615e')
            self.logsign.place(x=0, y=30)

            login_button = Button(self.logsign, text="SignIn", height=2, width=20, bg="grey", fg="white", command=self.signIn).place(x=1170, y=0)
            login_button = Button(self.logsign, text="SignUp", height=2, width=20, bg="grey", fg="white", command=self.signUp).place(x=1350, y=0)

            self.main_menu = Menu(self.master, font=self.my_font)
            self.master.config(menu=self.main_menu)

            self.home = Menu(self.main_menu, tearoff=0, fg='red',  activeforeground='white',
                             activebackground='black')
            self.main_menu.add_cascade(label='Home', menu=self.home)
            self.home.add_command(label='Home')

            self.Movies = Menu(self.main_menu, tearoff=0, fg='black', activeforeground='white', activebackground='black')
            self.main_menu.add_cascade(label='Movies', menu=self.Movies)
            self.Movies.add_command(label='Movies', command=self.show_movie)

            self.about = Menu(self.main_menu, tearoff=0, fg='black', activeforeground='white', activebackground='black')
            self.main_menu.add_cascade(label='About', menu=self.about)
            self.about.add_command(label='About Us', command=self.about_us)

            self.image = Label(self.bottom, image=self.use, bd=0, bg='#b8b5b0')
            self.image.place(x=0, y=0)
        else:
            self.after_login()
            self.dict = self.userr_coll.aggregate([{'$match': {'_id': self.userr}}])
            x = list(self.dict)[0]
            print(x['count'],len(x['movie']))
            if x['count']==len(x['movie']):
                messagebox.showinfo('Info', 'Take some time to update')
                Rec(self.userr_coll, self.userr)
                self.userr_coll.update({'_id': f'{self.userr}'}, {'$inc': {'count': 5}})

    def fr(self):
        self.frame = Frame(self.bottom, height=400, width=380, bg='#2b2929')
        self.frame.place(x=550, y=70)


    def user_authentication(self):
        self.passs = self.txt_pass.get()
        self.userr = self.txt_user.get()


        b = self.db.user.find({})

        for dic in b:
            if self.userr == dic['_id'] and self.passs == dic['password']:

                # try:


                self.userr_coll = self.db[f'{self.userr}']
                self.logsign.destroy()
                self.after_login()


                # except Exception as e:
                #     messagebox.showinfo("Info", e)

    def signUp(self):

        self.fr()
        self.login_fram = Frame(self.frame, height=400, width=300, bg='#b8b5b0')
        self.login_fram.place(x=0, y=0)
        self.logolbl = Label(self.login_fram, image=self.user_icon, bd=0, bg='#b8b5b0')
        self.logolbl.grid(row=0, columnspan=2, pady=20)

        self.lblname = Label(self.login_fram, text="Name", bg="#b8b5b0", compound=LEFT,
                        font=("times new roman", 20, "bold")).grid(row=1, column=0, pady=10)
        self.txt_user = Entry(self.login_fram, textvariable=self.username, bd=5, relief=GROOVE, font=("", 13))
        self.txt_user.grid(row=1, column=1, padx=20)
        lblpass = Label(self.login_fram, text="Password", image=self.user_lock, bg="#b8b5b0", compound=LEFT,
                        font=("times new roman", 20, "bold")).grid(row=2, column=0, pady=10)
        self.txt_pass = Entry(self.login_fram, bd=5, textvariable=self.password, relief=GROOVE, font=("", 13))
        self.txt_pass.grid(row=2, column=1, padx=20)
        lbluser = Label(self.login_fram, text="Re-Passd", image=self.user_lock, bg="#b8b5b0", compound=LEFT,
                        font=("times new roman", 20, "bold")).grid(row=3, column=0, pady=10)
        self.txt_cpass = Entry(self.login_fram, bd=5, textvariable=self.c_password, relief=GROOVE, font=("", 13))
        self.txt_cpass.grid(row=3, column=1, padx=20, pady=10)

        self.login_button = Button(self.login_fram, text="go to SignIn", bg="grey", command=self.signIn).grid(row=4,
                                                                                                           column=0,
                                                                                                           pady=20)
        self.login_button = Button(self.login_fram, text="Login", bg="grey", command=self.user_check)
        self.login_button.bind('<Return>', self.user_check)
        self.login_button.grid(row=4, column=1,pady=20)




    def signIn(self):

        self.fr()
        self.login_frame = Frame(self.frame, height=400, width=300, bg='#b8b5b0')

        self.login_frame.place(x=0, y=0)
        self.logolbl = Label(self.login_frame, image=self.user_icon, bd=0, bg='#b8b5b0')
        self.logolbl.grid(row=0, columnspan=2, pady=20)

        self.lbluser = Label(self.login_frame, text="Username", image=self.user_name, bg="#b8b5b0", compound=LEFT,
                        font=("times new roman", 20, "bold")).grid(row=1, column=0, pady=10)

        self.txt_user = Entry(self.login_frame, textvariable=self.username, bd=5, relief=GROOVE, font=("", 13))
        self.txt_user.grid(row=1, column=1, padx=20)

        self.lblpass = Label(self.login_frame, text="Password", image=self.user_lock, bg="#b8b5b0", compound=LEFT,
                        font=("times new roman", 20, "bold")).grid(row=2, column=0, pady=10)
        self.txt_pass = Entry(self.login_frame, textvariable=self.password, bd=5, relief=GROOVE, font=("", 13))
        self.txt_pass.grid(row=2, column=1, padx=20)
        self.login_button = Button(self.login_frame, text="Login", bg="grey", command=self.user_authentication)

        self.login_button.bind('<Return>', self.user_authentication)
        self.login_button.grid(row=3, column=0,pady=18)


        self.login_button = Button(self.login_frame, text="go to SignUp", bg="grey", command=self.signUp).grid(row=3, column=1,
                                                                                                pady=18)
        self.label_text = Label(self.login_frame, text="welcome You are in!!!", bg='#b8b5b0',
                           font=("times new roman", 9)).grid(row=4, column=0, pady=20)



    def user_check(self,_event = None):
        print("am here")
        self.coll_name = self.txt_user.get()
        password1 = self.txt_pass.get()
        password2 = self.txt_cpass.get()
        print(password1,password2)
        if password1 == password2:
            password = password2
            a_dict = {'_id':self.coll_name,'password':password}
            b = self.db.user.find({})

            for dic in b:
                if self.coll_name != dic['_id']:

                    self.db.user.insert_one(a_dict)
                    self.user_authentication()
                else:
                    messagebox.showinfo("Info", "Username also taken")


    def after_login(self):
        self.bottom = Frame(self.master, height=660, width=1536, bg='#2b2929')
        self.bottom.place(x=0, y=85)
        img = Image.open('images/movies_image.png')
        img = img.resize((400, 300), Image.ANTIALIAS)
        # self.use = PhotoImage(file="movi.png")
        # self.movies_image = PhotoImage(img)
        import pandas as pd
        import tkinter as tk
        from pandas import DataFrame
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        df = pd.read_csv('data/userProfile.csv')
        df = df.sort_values(by='0', ascending=False)
        df = df[df['0'] > 8]
        figure1 = plt.Figure(figsize=(6, 5), dpi=100,facecolor='#2b2929')
        ax1 = figure1.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure1, self.master)
        canvas.get_tk_widget().place(x=250, y=85)

        y = df['0'].values
        labels = df['Unnamed: 0'].values
        myexplode = [0.2]
        for i in range(len(y) - 1):
            myexplode.append(0)
        patches, texts, autotexts=ax1.pie(y, labels=labels, startangle=90, shadow=True, explode=myexplode, autopct='%1.1f%%',textprops={'color':"w"})
        Label(self.bottom,text = 'Recently Watched..',fg = 'white',font = ("Ink Free",35),bg = '#2b2929').place(x = 1100,y = 10)
        Label(self.bottom, text='User Stats', fg='white', font=("Ink Free", 35), bg='#2b2929').place(x=0,  y=10)

        Frame(self.bottom, height=12, width=1536, bg='#5e5d5b').place(x=0, y=500)
        Frame(self.bottom, height=500, width=17, bg='#5e5d5b').place(x=1050, y=0)
        myfont = Font(family='Ink Free', size=20, weight='bold')
        doc = self.userr_coll.find({})
        movie = list(doc)[0]['movie']
        movie = pd.DataFrame(movie)
        movie.drop_duplicates(subset='title', keep='last', inplace=True)
        movie = movie.tail()
        for i,title in enumerate(movie['title']):
            if i%2==0:
                Label(self.bottom, text=f'{5-i}. {title}', fg='#6dad86', font=myfont, bg='#2b2929',  anchor=W).place(x=1100,y=260-i*35)
            else:
                Label(self.bottom, text=f'{5-i}. {title}', fg='#f0b34a', font=myfont, bg='#2b2929',  anchor=W).place(x=1100,y=260-i*35)
        Button(self.bottom,padx = 170,font = ("Ink Free",35),fg = '#f7ad5e',bg = '#383736' ,text="Movies",  command=self.show_movie).place(x = 500,y = 536)



    def show_movie(self,event_ = None):
        from movies import movie
        from info import userinfo

        try:
            self.dict = self.userr_coll.aggregate([{'$match': {'_id': self.userr}}])
            x = list(self.dict)[0]
        except:
            self.userr_coll.insert_one({'_id':f'{self.userr}','movie':[],'recommanded':[]})
            self.dict = self.userr_coll.aggregate([{'$match': {'_id': self.userr}}])
            x = list(self.dict)[0]
        docs = x['movie']
        if len(docs) == 0:
            c = userinfo(self.master, self.lst, self.userr_coll,self.userr)

        else:
            c = movie(self.lst, self.master, self.userr_coll,self.userr)


    def about_us(self):
        from AboutUs import about
        c = about(self.lst, self.master,self.userr_coll, self.userr)



def main():
    root = Tk(className=' AutocompleteEntry demo')
    lst = []
    no = 1
    userr_coll = 'unknown'
    userr_name = 'unknown'
    app = Application(root,lst,no,userr_coll,userr_name)
    root.title("Phonebook App")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    print(root.winfo_screenwidth())
    root.resizable(False, False)

    root.mainloop()


if __name__ == '__main__':
    main()











