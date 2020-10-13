#!/usr/bin/env python
__author__ = "Arjun Tejani"
__version__ = "0.0.1"
__status__ = ""
import cv2
import os
import glob

'''''
 Following command shows how to read images
 '''''

for img in glob.glob("data-images/*"):
    cv_img = cv2.imread(img)
    cv2.imshow('show',cv_img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

'''''
 Following command shows how to save image frames
 '''''
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def capture_img():
    cv2.namedWindow("test")
    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()


'''''
   Following command shows how to save videos
'''''


def capture_vid():
    filename = 'video.avi'
    resolution = '720p'
    fps = 25
    # (width,height)
    DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }

    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def videotype(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    out = cv2.VideoWriter(filename, videotype(filename), fps, (1920, 1080))

    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('feed', frame)
        k = cv2.waitKey(1)
        if k == 27: #escape to end
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

#capture_img()
capture_vid()



