import PIL
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time

class FR_GUI(tk.Tk):
    """this is the app
    it inherits from tk.Tk
    """
    def __init__(self):
        super().__init__()
        #self.title = "Self Registration Kiosk"
        self.geometry("700x1050")
        # self.attributes("-fullscreen", True)
        # self.wm_attributes("-topmost", 1)

        self.home = WelcomeScreen(self)
        self.home.pack(expand=True,fill=tk.BOTH)
        self.front = FrontPage(self)
        self.second = SecondPage(self)

    def welcome_screen(self):
        self.front.pack_forget()
        self.second.pack_forget()
        self.home.pack(expand=True,fill=tk.BOTH)

    def show_first(self):
        self.home.pack_forget()
        self.second.pack_forget()
        self.front.pack(expand=True, fill=tk.BOTH)
        self.front.show_frame()

    def show_second(self):
        self.front.cap.release()
        self.front.pack_forget()
        self.home.pack_forget()
        self.second.pack(expand=True, fill=tk.BOTH)

class WelcomeScreen (tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        #self.input = tk.StringVar()

        self.mainframe = tk.Frame(self)
        self.mainframe.pack(side=tk.TOP,padx=5,pady=80)#expand=True, fill=tk.BOTH)

        self.name_label = tk.Label(
            self.mainframe,
            text=" Image Analysis ",
            font=("Courier", 18),
        )

        self.name_label.pack()

        self.take_pic_btn = tk.Button(
            self.mainframe,
            text="Take Pictures",
            font=("Courier", 15),
            command=self.close_welcome)

        self.take_pic_btn.pack()

        self.load_pic_btn = tk.Button(
            self.mainframe,
            text="Load Pictures",
            font=("Courier", 15),
            command=self.close_welcome)

        self.load_pic_btn.pack()

    def close_welcome(self):
        self.master.show_first()

class FrontPage(tk.Frame):
    """This is a class to make the front page
    it inherits from tk.Frame
    """

    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

        self.mainframe = tk.Frame(self)
        self.mainframe.pack(side=tk.TOP,padx=5,pady=20,expand=True, fill=tk.BOTH)

        self.name_label = tk.Label(
            self.mainframe,
            text="Press 'Take shot' to take picture: ",
            font=("Courier", 13),
        )
        self.name_label.pack()

        self.label_count = tk.Label(
            self.mainframe,
            )
        self.label_count.pack()

        self.lmain = tk.Label(
            self.mainframe,
            anchor=tk.CENTER
            #text='cam frame'
        )
        self.lmain.pack()

        self.ent_btn = tk.Button(
            self.mainframe,
            text="Take shot",
            font=("Courier", 15),
            command=self.onClick)#self.start_cam)

        self.ent_btn.pack(side = 'bottom')

        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source)

        #get cam width & height
        self.width  = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def cam_release(self):
        self.cap.release()

    def show_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)

    after_id = None

    def countdown(self,count):
        # change text in label
        self.label_count['text'] = count
        if count > 0:
            # call countdown again after 1000ms (1s)
            self.after(1000, self.countdown, count-1)
        else:
            self.snapshot()

    '''Start counting down.'''
    def onClick(self):
        self.countdown(2)

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.cap.read()
        out_name = ("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
        cv2.imwrite(out_name, frame)
        self.cam_release()
        print(out_name)
        self.master.show_second()

class SecondPage(tk.Frame):
    """This is a class to make the second page
    it inherits from tk.Frame
    """

    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

        self.firstName = tk.StringVar()
        self.lastName = tk.StringVar()
        #self.email = tk.StringVar()
        self.ph_one = tk.IntVar()

        self.mainframe = tk.Frame(self)
        self.mainframe.pack(fill=tk.BOTH, pady=80)

        self.label = tk.Label(
            self.mainframe, text="person not registered. \n please register: "
        )
        self.label.pack()

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP,padx=5,pady=10)#expand=True, fill=tk.BOTH)

        self.center_frame = tk.Frame(self)
        self.center_frame.pack(side=tk.TOP,padx=5,pady=10)

        self.low_frame = tk.Frame(self)
        self.low_frame.pack(side=tk.TOP, padx=5,pady=10)#,expand = True)

        fname_label = tk.Label(self.top_frame,text="First Name",font=("Courier", 13))
        self.fname_entry = tk.Entry(self.top_frame, textvariable = self.firstName)

        lname_label = tk.Label(self.top_frame,text="Last Name ",font=("Courier", 13))
        self.lname_entry = tk.Entry(self.top_frame, textvariable = self.lastName)

        fname_label.grid(row=0, column=0)
        self.fname_entry.grid(row=0, column=1)

        lname_label.grid(row=1, column=0)
        self.lname_entry.grid(row=1, column=1)

        self.home_button = tk.Button(self.low_frame,text='Home',command=self.clear_widgets).grid(row=0,column=0,pady=4)
        self.submit_button = tk.Button(self.low_frame,text='Submit',command=self.form_submit).grid(row=0,column=1,pady=10)

    def form_submit(self):
        self.f_name = self.firstName.get()
        self.l_name = self.lastName.get()
        self.submit_label = tk.Label(self.center_frame,text="Thank you "+self.f_name+" "+self.l_name+" for your registeration",font=("Courier", 13))
        self.submit_label.grid(row=2,column=0)
        self.submit_label['text'] = ""

    def clear_widgets(self):
        self.refresh()
        self.master.welcome_screen()

    def refresh(self):
        self.fname_entry.delete(0,"end")
        self.lname_entry.delete(0,"end")
        self.fname_entry.focus_set()



app = FR_GUI()
app.bind("<Escape>", exit)
app.mainloop()

