from tkinter import *
from tkinter import messagebox
import pymongo
from tkinter.font import Font
from recommand_for_you import  AutocompleteEntry
from recommand_for_you import AutocompleteCombobox
import requests
import os
from PIL import ImageTk, Image
from template import Template
from PIL import Image
from resizeimage import resizeimage
from info import userinfo
from tkinter import messagebox
from recSys import Rec
import io
class movie(Template):
    def __init__(self,lst,master,userr_coll,userr_name):
        self.userr_coll = userr_coll
        self.userr_name = userr_name
        self.master = master
        self.lst = []
        Template.__init__(self, self.lst, self.master)


        self.master.title('movies')
        self.key = -1
        try:
            self.client = pymongo.MongoClient("localhost",27017)
            self.db = self.client
        except Exception as e:
            messagebox.showinfo("Info", e)

        self.d = self.db.sample_mflix.movies.aggregate([{'$project': {'title': 1}}])

        for dic in self.d:
            self.lst.append(dic['title'])
        self.movie_list = []
        self.names_list = list(self.userr_coll.find({}))[0]['recommanded']
        for i in range(10):
            self.dict = self.db.sample_mflix.movies.aggregate([{'$match': {'title': f'{self.names_list[i]}'}}, {'$limit': 10}])
            try:
                url = list(self.dict)[0]['poster']
            except:
                url = 'https://m.media-amazon.com/images/M/MV5BYzk0YWQzMGYtYTM5MC00NjM2LWE5YzYtMjgyNDVhZDg1N2YzXkEyXkFqcGdeQXVyMzE0MjY5ODA@._V1_SY1000_SX677_AL_.jpg'
            page = requests.get(url)
            load = Image.open(io.BytesIO(page.content))
            load = load.resize((200, 70), Image.ANTIALIAS)
            self.movie_list.append(load)
        self.update_list()
        self.dict = self.userr_coll.aggregate([{'$match': {'_id': self.userr_name}}])
        x = list(self.dict)[0]

        docs = x['movie']
        if len(docs)==0:
            c = userinfo(self.master,self.lst,self.userr_coll,self.userr_name)


    def update_list(self):

        self.top = Frame(self, height=150, width=1536, bg='#5e615e')
        self.top.pack(side=TOP)
        self.fs = Frame(self, height=5, width=1536, bg='red')
        self.fs.pack()
        
        self.bottom = Frame(self, height=200, width=1536, bg='#2b2929')
        self.bottom.pack()
     
        myfont = Font(family='Ink Free', size=20, weight='bold')
        Label(self.bottom, text = 'Recommanded for you',font = myfont,bg = '#2b2929',fg = '#6dad86').place(x = 15, y = 135)

        self.canvas = Canvas(self, height=260, width=1536, bg='#2b2929')
        self.scroll_y = Scrollbar(self, orient="horizontal", command=self.canvas.xview, bg='#2b2929', troughcolor='#2b2929')
        self.frame = Frame(self.canvas, bg='#2b2929', width=1536)
        self.frame_label = Frame(self.canvas, bg='#2b2929', width=1536)


        self.fram = Frame(self.frame)

        bg_icon = ImageTk.PhotoImage(self.movie_list[0])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=0))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[0]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[1])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=1))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[1]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[2])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=2))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[2]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[3])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=3))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[3]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[4])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=4))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[4]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[5])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=5))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[5]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[6])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=6))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[6]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[7])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=7))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[7]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[8])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=8))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[8]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)

        bg_icon = ImageTk.PhotoImage(self.movie_list[9])
        fram = Frame(self.frame, height=100, width=200, bg='#2b2929', cursor='hand2')
        l1 = Label(fram, image=bg_icon)
        l1.bind('<Button-1>', lambda a: self.get(key=9))
        l1.pack(side=LEFT, padx=10)
        fram.pack(side=LEFT)
        l1.image = bg_icon
        fra = Frame(self.frame_label, height=60, width=200, bg='#2b2929')
        fra.pack(side=LEFT, padx=10)
        x = Label(fra, text=f'{self.names_list[9]}', width=30, fg='yellow', bg='#2b2929')
        x.place(x=0, y=0)


        self.canvas.create_window(0, 0, anchor='n', window=self.frame, height=80)
        self.canvas.update_idletasks()
        self.canvas.create_window(0, 80, anchor='n', window=self.frame_label, height=60)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),
                         xscrollcommand=self.scroll_y.set, bg='#2b2929')
        self.canvas.pack()
        self.scroll_y.pack(fill='x')
        
        self.f = Frame(self, height=100, width=1536, bg='#2b2929')
        self.f.pack()
        self.bottom_strip = Frame(self,height = 5,width = 1536,bg = 'red')
        self.bottom_strip.pack()
        self.bott = Frame(self, height=150, width=1536, bg='#5e615e')
        self.bott.pack()


        #
        self.top_img = PhotoImage(file=r'images/youtube.png')
        self.top_img_label = Label(self.top, image=self.top_img, bg='#5e615e')
        self.top_img_label.place(x=360, y=20)
        self.label = Label(self.top, text='Movies Explorer', bg='#5e615e', fg='#fa0202', font=self.my_font)
        self.label.place(x=520, y=30)
        self.entrt = Frame(self.bottom, height=100, bg='grey')
        self.entrt.place(x=1300, y=500)
        self.entry = AutocompleteEntry(self.entrt)
        self.entry.set_completion_list(self.lst)
        self.entry.place(x=700, y=500)
        self.entry.focus_set()
        self.combo = AutocompleteCombobox(self.bottom, width=25, height=15, font="Verdana 25")
        self.combo.set_completion_list(self.lst)
        bigfont = Font(family="Helvetica", size=20)
        self.combo.option_add("*TCombobox*Listbox*Font", bigfont)
        self.combo.place(x=480, y=30)
        self.combo.focus_set()
        button = Button(self.bottom, text='Search', font="Verdana 13", command=self.search)
        button.bind('<Return>',self.search)
        button.place(x=700, y=85)
        # I used a tiling WM with no controls, added a shortcut to quit
        self.bind('<Control-Q>', lambda event=None: self.destroy())
        self.bind('<Control-q>', lambda event=None: self.destroy())

    def get(self,key):
        self.key = key
        self.search()
        self.key = -1

    def search(self,_event = None):

        self.canvas.destroy()
        self.fram.destroy()
        self.scroll_y.destroy()
        self.bott.destroy()
        self.bottom_strip.destroy()
        self.f.destroy()


        self.img_frame = Frame(self.bottom, bg='#2b2929', height=500, width=360)
        self.img_frame.pack(side=LEFT)
        self.strip = Frame(self.bottom, bg='#5e615e', height=500, width=15)
        self.strip.pack(side=LEFT)
        self.info_frame = Frame(self.bottom, bg='#2b2929', height=500, width=545)
        self.info_frame.pack(side=LEFT)
        self.strip = Frame(self.bottom, bg='#5e615e', height=500, width=15)
        self.strip.pack(side=LEFT)
        self.desc_frame = Frame(self.bottom, bg='#2b2929', height=500, width=580)
        self.desc_frame.pack(side=LEFT)
        self.desc_subframe = Frame(self.desc_frame, bg='#2b2929', height=500, width=580)
        self.desc_subframe.place(x = 60,y = 0)
        if self.key==-1:
            self.dict = self.db.sample_mflix.movies.aggregate([{'$match': {'title': f'{self.combo.get()}'}}])
        else:
            self.dict = self.db.sample_mflix.movies.aggregate([{'$match': {'title': f'{self.names_list[self.key]}'}}])

        try:
            url = list(self.dict)[0]['poster']
        except:
            url = 'https://as2.ftcdn.net/jpg/02/25/53/45/500_F_225534502_aLk2Qu5EM1A6Jfy91mBqgeV45APDJOHj.jpg'
        page = requests.get(url)
        load = Image.open(io.BytesIO(page.content))
        load = load.resize((300, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        frame = Frame(self.img_frame, bg='white', height=300, width=300)
        frame.place(x=30, y=20)
        img = Label(frame, image=render)
        img.image = render
        img.place(x=0, y=0)
        # self.canvas = Canvas(self.bottom, bg='black')
        # coord = 370, 110, 700, 110
        # self.canvas.create_line(coord)
        my_font = Font(family='Ink Free', size=30, weight='bold')
        if self.key==-1:
            label1 = Label(self.info_frame, text=f'{self.combo.get()}', fg='#14ba38', font=my_font, bg='#2b2929', width=25)
        else:
            label1 = Label(self.info_frame, text=f'{self.names_list[self.key]}', fg='#14ba38', font=my_font, bg='#2b2929',width=25)
        label1.place(x=25, y=35)
        myfont = Font(family='Ink Free', size=15, weight='bold')
        myfontm = Font(family='Ink Free', size=13)
        if self.key == -1:
            self.dict = self.db.sample_mflix.movies.aggregate([{'$match': {'title': f'{self.combo.get()}'}}])
        else:
            self.dict = self.db.sample_mflix.movies.aggregate([{'$match': {'title': f'{self.names_list[self.key]}'}}])
        l = list(self.dict)
        type = l[0]['type']
        label_type = Label(self.info_frame, text=f'Type          :   ', fg='#6dad86', font=myfont, bg='#2b2929',
                           width=16, anchor=W)
        label_type.place(x=30, y=130)
        label_typp = Label(self.info_frame, text=f'{type}', fg='#d3dbdb', font=myfont, bg='#2b2929', width=40, anchor=W)
        label_typp.place(x=155, y=130)

        if 'languages' in l[0].keys():
            language = l[0]['languages']
        else:
            language = 'Unknown'
        label_lang = Label(self.info_frame, text=f'Languages  :   ', fg='#6dad86', font=myfont, bg='#2b2929', width=16,anchor=W)
        label_lang.place(x=30, y=170)
        label_language = Label(self.info_frame, text=f'{language}', fg='#d3dbdb', font=myfont, bg='#2b2929', width=40,
                               anchor=W)
        label_language.place(x=155, y=170)

        cast = l[0]['cast']
        label_cast = Label(self.info_frame, text=f'Cast          :   ', font=myfont, fg='#6dad86', bg='#2b2929',
                           width=16, anchor=W)
        label_cast.place(x=30, y=210)
        label_castt = Label(self.info_frame, text=f'{cast}', fg='#d3dbdb', font=myfont, bg='#2b2929', wraplength=350,
                            height=3, width=30, anchor=W)
        label_castt.place(x=155, y=210)

        generes = l[0]['genres']
        label_genre = Label(self.info_frame, text=f'Genres       :   ', fg='#6dad86', font=myfont, bg='#2b2929',
                            width=14, anchor=W)
        label_genre.place(x=30, y=285)
        label_genres = Label(self.info_frame, text=f'{generes}', fg='#d3dbdb', font=myfont, bg='#2b2929', width=30,
                             anchor=W)
        label_genres.place(x=155, y=285)

        year = l[0]['year']
        label_year = Label(self.info_frame, text=f'Year          :   ', fg='#6dad86', font=myfont, bg='#2b2929',
                           width=16, anchor=W)
        label_year.place(x=30, y=320)
        label_yearr = Label(self.info_frame, text=f'{year}', font=myfont, fg='#d3dbdb', bg='#2b2929', width=40,
                            anchor=W)
        label_yearr.place(x=155, y=320)

        country = l[0]['countries']
        label_countryy = Label(self.info_frame, text=f'Countries   :   ', fg='#6dad86', font=myfont, bg='#2b2929',
                               width=16, anchor=W)
        label_countryy.place(x=30, y=360)
        label_country = Label(self.info_frame, text=f'{country}', fg='#d3dbdb', font=myfont, bg='#2b2929', width=40,
                              anchor=W)
        label_country.place(x=155, y=360)

        award = l[0]['awards']['wins']
        labe = Label(self.info_frame, text=f'Awards      :   ', fg='#6dad86', font=myfont, bg='#2b2929', width=16,
                     anchor=W)
        labe.place(x=30, y=397)
        label_award = Label(self.info_frame, text=f'{award}', fg='#d3dbdb', font=myfont, bg='#2b2929', width=40,
                            anchor=W)
        label_award.place(x=155, y=397)

        try:
            director = l[0]['directors']
        except:
            director = ''
        label_directors = Label(self.info_frame, text=f'Directors   :   ', fg='#6dad86', font=myfont, bg='#2b2929',
                                width=16, anchor=W)
        label_directors.place(x=30, y=434)
        label_direct = Label(self.info_frame, text=f'{director}', fg='#d3dbdb', font=myfont, bg='#2b2929', width=40,
                             anchor=W)
        label_direct.place(x=155, y=434)

        imdb_rating = l[0]['imdb']['rating']
        label5 = Label(self.img_frame, text=f'Imdb Rating : ', bg='#2b2929', font=myfont, fg='#6dad86', width=17,
                       anchor=W)
        label5.place(x=60, y=330)
        label5 = Label(self.img_frame, text=f'{imdb_rating}', fg='#d3dbdb', bg='#2b2929', font=myfont, width=17,
                       anchor=W)
        label5.place(x=200, y=330)

        label_rate = Label(self.img_frame, text='---Rate The Movie---', fg='#6dad86', font=myfont, bg='#2b2929',
                           width=17, anchor=W)
        label_rate.place(x=65, y=370)

        self.var = DoubleVar()
        scale = Scale(self.img_frame, variable=self.var, activebackground='black', cursor='arrow', from_=0, to=10,
                      orient=HORIZONTAL, resolution=0.1,
                      sliderlength=15, troughcolor='blue', bg='#2b2929', length=150, bd=0, relief=RAISED)
        button_submit = Button(self.img_frame, text='submit', command=self.submit_rating)
        button_submit.bind('<Return>', self.submit_rating)
        button_submit.place(x=215, y=422)
        scale.place(x=55, y=417)
        label_note = Label(self.img_frame, text='Note : If you watched this movie,please rate us', bg='#2b2929',
                           fg='#d3dbdb', )
        label_note.place(x=20, y=465)

        try:
            full_plot = l[0]['fullplot']
        except:
            full_plot = ''
        description = Label(self.desc_subframe, text=f'{full_plot}', font=myfontm, fg='#a6ada8', bg='#2b2929', width=446,
                            height=15, wraplength=446, anchor=NW)
        description.place(x=0, y=135)
        description_label = Label(self.desc_subframe, text='Movie Description', fg='#266a70', font=myfont, bg='#2b2929')
        description_label.place(x=180, y=100)

        b = Button(self.desc_subframe, text='X', font='15', activeforeground='black', bg='#2b2929', fg='grey',
                   activebackground='red'
                   , command=self.exitt)
        b.place(x=400, y=15)
        if self.key == -1:
            self.d = {'title': self.combo.get(), 'rating ': self.var.get()}
        else:
            self.d = {'title': self.names_list[self.key], 'rating ': self.var.get()}

    def submit_rating(self,_event = None):
        self.userr_coll.update({'_id':f'{self.userr_name}'},{'$push':{'movie':self.d}})
        self.userr_coll.update({'_id': f'{self.userr_name}'}, {'$inc': {'count': 1}})
        messagebox.showinfo('Info','Thank you for your rating')
        self.exitt()

    def exitt(self):
        self.top.destroy()
        self.bottom.destroy()
        self.f.destroy()
        self.fs.destroy()
        self.strip.destroy()
        self.canvas.destroy()
        self.fram.destroy()
        self.scroll_y.destroy()
        self.update_list()





    def about_us(self):
        from AboutUs import about
        c = about(self.lst, self.master,self.userr_coll, self.userr_name)
        self.destroy()

    def homee(self):
        from Home import Application
        self.no = 2
        c = Application(self.master, self.lst,self.no,self.userr_coll,self.userr_name)
        self.destroy()

    def blogg(self):
        from blogging import blog
        c = blog(self.lst, self.master, self.userr_coll,self.userr_name)
        self.destroy()
