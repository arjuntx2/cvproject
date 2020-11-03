from tkinter import *
import tkinter.ttk as ttk
import cv2
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog


class MyApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.frames = {}
        for F in (PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='NSEW')
        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class PageOne(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source)

        # get cam width & height
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.make_widget()

    def make_widget(self):
        self.feedlabel = Label(self, bg="steelblue", fg="white", text="WEBCAM FEED", font=('Comic Sans MS', 20))
        self.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.cameraLabel = Label(self, bg="steelblue", borderwidth=3, relief="groove")
        self.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        self.saveLocationEntry = Entry(self, width=55, textvariable=self.destPath)
        self.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)

        self.browseButton = Button(self, width=10, text="BROWSE", command=self.destBrowse)
        self.browseButton.grid(row=3, column=2, padx=10, pady=10)

        self.captureBTN = Button(self, text="CAPTURE", command=self.Capture, bg="LIGHTBLUE", font=('Comic Sans MS', 15),
                                 width=20)
        self.captureBTN.grid(row=4, column=1, padx=10, pady=10)

        self.CAMBTN = Button(self, text="STOP CAMERA", command=self.StopCAM, bg="LIGHTBLUE", font=('Comic Sans MS', 15),
                             width=13)
        self.CAMBTN.grid(row=4, column=2)

        self.previewlabel = Label(self, bg="steelblue", fg="white", text="IMAGE PREVIEW",
                                  font=('Comic Sans MS', 20))
        self.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

        self.imageLabel = Label(self, bg="steelblue", borderwidth=3, relief="groove")
        self.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

        self.openImageEntry = Entry(self, width=55, textvariable=self.imagePath)
        self.openImageEntry.grid(row=3, column=4, padx=10, pady=10)

        self.openImageButton = Button(self, width=10, text="BROWSE", command=self.imageBrowse)
        self.openImageButton.grid(row=3, column=5, padx=10, pady=10)

        #ttk.Label(self, text='This is page two').grid(padx=(20, 20), pady=(20, 20))
        self.button2 = Button(self, text='Next Page',
                             command=lambda: self.controller.show_frame(PageTwo))
        self.button2.grid(row=4, column=1, padx=10, pady=10)

            # Calling ShowFeed() function
        self.ShowFeed()

        # Defining ShowFeed() function to display webcam feed in the cameraLabel;
    def ShowFeed(self):
        # Capturing frame by frame
        ret, frame = self.cap.read()

        if ret:
            # Flipping the frame vertically
            frame = cv2.flip(frame, 1)

            # Displaying date and time on the feed
            #cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                        #(0, 255, 255))

            # Changing the frame color from BGR to RGB
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # Creating an image memory from the above frame exporting array interface
            videoImg = Image.fromarray(cv2image)

            # Creating object of PhotoImage() class to display the frame
            imgtk = ImageTk.PhotoImage(image=videoImg)

            # Configuring the label to display the frame
            self.cameraLabel.configure(image=imgtk)

            # Keeping a reference
            self.cameraLabel.imgtk = imgtk

            # Calling the function after 10 milliseconds
            self.cameraLabel.after(10, self.ShowFeed)
        else:
            # Configuring the label to display the frame
            self.cameraLabel.configure(image='')

    def destBrowse(self):
        # Presenting user with a pop-up for directory selection. initialdir argument is optional
        # Retrieving the user-input destination directory and storing it in destinationDirectory
        # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
        self.destDirectory = filedialog.askdirectory(initialdir="data-images")

        # Displaying the directory in the directory textbox
        self.destPath.set(self.destDirectory)

    def imageBrowse(self):
        # Presenting user with a pop-up for directory selection. initialdir argument is optional
        # Retrieving the user-input destination directory and storing it in destinationDirectory
        # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
        self.openDirectory = filedialog.askopenfilename(self,initialdir="data-images")

        # Displaying the directory in the directory textbox
        self.imagePath.set(self.openDirectory)

        # Opening the saved image using the open() of Image class which takes the saved image as the argument
        imageView = Image.open(self.openDirectory)

        # Resizing the image using Image.resize()
        imageResize = imageView.resize((640, 480), Image.ANTIALIAS)

        # Creating object of PhotoImage() class to display the frame
        imageDisplay = ImageTk.PhotoImage(imageResize)

        # Configuring the label to display the frame
        self.imageLabel.config(image=imageDisplay)

        # Keeping a reference
        self.imageLabel.photo = imageDisplay

    # Defining Capture() to capture and save the image and display the image in the imageLabel
    def Capture(self):
        # Storing the date in the mentioned format in the image_name variable
        image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

        # If the user has selected the destination directory, then get the directory and save it in image_path
        if self.destPath.get(self) != '':
            image_path = self.destPath.get(self)
        # If the user has not selected any destination directory, then set the image_path to default directory
        else:
            image_path = "data-images"

        # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
        imgName = image_path + '/' + image_name + ".jpg"

        # Capturing the frame
        ret, frame = self.cap.read()

        # Displaying date and time on the frame
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430, 460), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    (0, 255, 255))

        # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
        success = cv2.imwrite(imgName, frame)

        # Opening the saved image using the open() of Image class which takes the saved image as the argument
        saved_image = Image.open(imgName)

        # Creating object of PhotoImage() class to display the frame
        saved_image = self.ImageTk.PhotoImage(saved_image)

        # Configuring the label to display the frame
        self.imageLabel.config(image=saved_image)

        # Keeping a reference
        self.imageLabel.photo = saved_image

        # Displaying messagebox
        if success:
            self.messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)

    # Defining StopCAM() to stop WEBCAM Preview
    def StopCAM(self):
        # Stopping the camera using release() method of cv2.VideoCapture()
        self.cap.release()

        # Configuring the CAMBTN to display accordingly
        self.CAMBTN.config(text="START CAMERA", command=self.StartCAM)

        # Displaying text message in the camera label
        self.cameraLabel.config(text="CAMERA IS OFF", font=('Comic Sans MS', 79))

    def StartCAM(self):
        # Creating object of class VideoCapture with webcam index
        self.cap = cv2.VideoCapture(0)

        # Setting width and height
        width_1, height_1 = 640, 480
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

        # Configuring the CAMBTN to display accordingly
        self.CAMBTN.config(text="STOP CAMERA", command=self.StopCAM)

        # Removing text message from the camera label
        self.cameraLabel.config(text="")

        # Calling the ShowFeed() Function
        self.ShowFeed()

    # Creating object of tk class

    # Creating object of class VideoCapture with webcam index
    #self.cap = cv2.VideoCapture(0)

    # Setting width and height
    #width, height = 640, 480
    #self.set.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Setting the title, window size, background color and disabling the resizing property
    #root.title("PyCAMERA")
    #root.geometry("1340x670")
    #root.resizable(False, False)
    #root.configure(background="steelblue")

    # Creating tkinter variables
    destPath =StringVar()
    imagePath=StringVar()


class PageTwo(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        self.make_widget()

    def make_widget(self):
        ttk.Label(self, text='This is page two').grid(padx=(20,20), pady=(20,20))
        button1 = ttk.Button(self, text='Previous Page',
                             command=lambda: self.controller.show_frame(PageOne))
        button1.grid()


if __name__ == '__main__':
    app = MyApp()
    app.title('Multi-Page Test App')
    app.mainloop()