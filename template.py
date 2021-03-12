from tkinter import *
from tkinter.font import Font
class Template(Toplevel):
    def __init__(self,lst,master):
        Toplevel.__init__(self)
        self.master = master
        self.lst = lst

        self.my_font = Font(family='Ink Free', size=55, weight='bold')
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), 1536))


        self.top = Frame(self, height=150,width = 1536, bg='#5e615e')
        self.top.place(x = 0,y = 0)
        self.f = Frame(self,height = 5,width = 1536,bg = 'red')
        self.f.place(x = 0,y = 150)
        self.f = Frame(self, height=5, width=1536, bg='red')
        self.f.place(x=0, y=655)
        self.footer = Frame(self,height = 200,width = 1536,bg = '#5e615e')
        self.footer.place(x = 0,y = 660)
        self.bottom = Frame(self, height=500, width=1536, bg='#2b2929')
        self.bottom.place(x=0, y=155)

        self.main_menu = Menu(self, font=self.my_font)
        self.config(menu=self.main_menu)

        self.home = Menu(self.main_menu, tearoff=0, fg='black',  activeforeground='blue',
                         activebackground='black')
        self.main_menu.add_cascade(label='Home', menu=self.home)
        self.home.add_command(label='Home', command=self.homee)

        self.Movies = Menu(self.main_menu, tearoff=0, fg='black', activeforeground='blue', activebackground='black')
        self.main_menu.add_cascade(label='Movies', menu=self.Movies)
        self.Movies.add_command(label='Movies', command=self.show_movie)

        self.about = Menu(self.main_menu, tearoff=0, fg='black', activeforeground='blue', activebackground='black')
        self.main_menu.add_cascade(label='About', menu=self.about)
        self.about.add_command(label='About Us', command=self.about_us)


    def show_movie(self):
        from info import userinfo
        from movies import movie
        if self.db.userr.movie.find({}).count() == 0:
            c = userinfo(self.master, self.lst, self.db, self.userr)
        else:
            c = movie(self.lst,self.master)
            self.destroy()

    def about_us(self):
        from AboutUs import about
        c = about(self.lst,self.master)
        self.destroy()

    def homee(self):
        from Home import Application
        c = Application(self.master,self.lst)
        self.destroy()



