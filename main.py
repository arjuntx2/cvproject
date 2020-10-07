#!/usr/bin/env python
__author__ = "Arjun Tejani"
__version__ = "0.0.1"
__status__ = ""
import cv2
import os

filename = 'video.avi'
res = '720p'
fps = 25

# (width,height)
DIMENSIONS =  {
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
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
out = cv2.VideoWriter(filename, videotype(filename), fps, (1920,1080))

while True:
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('feed',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()



