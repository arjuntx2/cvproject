import cv2
import numpy as np

img = cv2.imread('data-images/idenprof.jpg')
height, width = img.shape[:2]
# Change these values to fit the size of your region of interest
roi_size = 10 # (10x10)
roi_values = img[(height-roi_size)/2:(height+roi_size)/2,(width-roi_size)/2:(width+roi_size)/2]
mean_blue = np.mean(roi_values[:,:,0])
mean_green = np.mean(roi_values[:,:,1])
mean_red = np.mean(roi_values[:,:,2])

print("R: {}  G: {}  B: {}").format(mean_red, mean_green, mean_blue)