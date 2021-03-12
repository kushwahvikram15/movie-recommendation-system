from tkinter import *
from tkinter import messagebox
import pymongo

from tkinter.font import Font

from recommand_for_you import  AutocompleteEntry
from recommand_for_you import AutocompleteCombobox

from recSys import Rec
from template import Template
class userinfo(Template):
    def __init__(self, master, lst, userr_coll,userr_name):

        self.lst = master
        self.master = lst
        Template.__init__(self, self.master,self.lst)

        self.userr_name = userr_name
        self.userr_coll = userr_coll
        self.l = [{}]
        try:
            self.client = pymongo.MongoClient("localhost",27017)
            self.db = self.client
        except Exception as e:
            messagebox.showinfo("Info", e)

        self.d = self.db.sample_mflix.movies.aggregate([{'$project': {'title': 1}}])

        for dic in self.d:
            self.lst.append(dic['title'])



        self.title('user_info')
        self.geometry('700x500+300+100')
        self.top = Frame(self, height = 50,width = 700, bg='#5e615e')
        self.top.pack()
        myfont = Font(family='Ink Free', size=35, weight='bold')
        self.label = Label(self.top, text='For User Info', bg='#5e615e', fg='#f1ff26', font=myfont)
        self.label.place(x=200, y=0)
        self.strip = Frame(self,height = 5,width = 700,bg = 'red')
        self.strip.pack()


        self.bottom = Frame(self,height = 390,width = 700,bg = '#2b2929')
        self.bottom.pack()

        self.strip = Frame(self, height=5, width=700, bg='red')
        self.strip.pack()
        self.footer = Frame(self, height=50, width=700, bg='#5e615e')
        self.footer.pack()
        self.entrt = Frame(self.bottom, height=100, bg='grey')
        self.entrt.place(x=1200, y=500)
        self.entry = AutocompleteEntry(self.entrt)
        self.entry.set_completion_list(self.lst)
        self.entry.place(x=500, y=500)
        self.entry.focus_set()
        self.combo = AutocompleteCombobox(self.bottom, width=20, height=15, font="Verdana 25")
        self.combo.set_completion_list(self.lst)
        bigfont = Font(family="Helvetica", size=20)
        self.combo.option_add("*TCombobox*Listbox*Font", bigfont)
        self.combo.place(x=80, y=30)
        self.combo.focus_set()
        self.count = 0
        myfontm = Font(family='Ink Free', size=12, weight='bold')
        self.var = DoubleVar()
        self.scale = Scale(self.bottom, variable=self.var, activebackground='black', cursor='arrow', from_=10, to=0,
                      resolution=0.1, sliderlength=15, troughcolor='grey', bg='#2b2929', fg='white', length=150, bd=0,
                      relief=RAISED)
        self.scale.place(x=580, y=30)
        

        p = 0
        for i in 'Rate Here':
            l= Label(self.bottom,text = i,font = myfontm,bg = '#2b2929',fg = '#f1ff26')
            l.place(x = 635,y = 23+p*18)
            p+=1

        self.button1 = Button(self.bottom, text='Search', font="Verdana 13", command=self.Search)

        self.button1.place(x=240, y=85)
        self.button2 = Button(self.footer, text='Submit',activebackground='#08fc6e', command=self.Submit)
        self.button2.place(x=600, y=15)

    def Search(self):
        myfont = Font(family='Ink Free', size=15, weight='bold')

        if len(self.combo.get())==0 or self.scale.get()==0.0:
            messagebox.showinfo('Info','Enter Movie Name With Ratings')
        else:
            if self.count==0:
                self.frame = Frame(self.bottom,height = 25,width = 600,bg = '#2b2929')
                self.frame.place(x = 50,y = 180)
                l = Label(self.frame,text = 'Title',bg = '#2b2929',fg = '#6dad86',font = myfont)
                l.place(x = 0,y = 0)
                l = Label(self.frame, text='Rating',bg = '#2b2929',fg = '#6dad86',font = myfont)
                l.place(x = 400,y = 0)

            if self.combo.get() not in self.l[self.count].values():
                self.d = {}
                self.f = Frame(self.bottom, height=10, width=100 + self.count * 86, bg='#08fc6e')
                self.f.place(x=80, y=10)
                self.info_frame = Frame(self.bottom,height = 23,width = 600,bg = '#2b2929')
                self.info_frame.place(x = 50,y = 225+self.count*30)
                label = Label(self.info_frame,text = f'{self.combo.get()}',bg = '#2b2929',fg='#d3dbdb',font = myfont)
                label.place(x = 0,y = 0)
                label = Label(self.info_frame, text=f'{self.scale.get()}',bg='#2b2929',fg='#d3dbdb',font = myfont)
                label.place(x = 400,y = 0)

                self.d['title'] = self.combo.get()
                self.d['rating'] = self.scale.get()

                self.count += 1
                self.l.append(self.d)
                if self.count==5:
                    self.button1.destroy()

            else:
                messagebox.showinfo('info','movies name not must be same')

        self.userr_coll.update({'_id':f'{self.userr_name}'},{'$push':{'movie':self.d}})


    def Submit(self):
        self.d = self.l
        self.d.remove({})
        Rec(self.userr_coll,self.userr_name)
        from movies import movie
        c = movie(self.lst, self.master, self.userr_coll,self.userr_name)
        self.destroy()


