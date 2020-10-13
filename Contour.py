import cv2
img2 = cv2.imread('data-images/video-1.jpg',1)
gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,195,1)

contours, hierchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img2 = img2.copy()
index = -1
thick = 4
color = [255,0,255]

cv2.drawContours(img2, contours,index,color,thick)
#img = cv2.hconcat([img2,thresh])
#res_small = cv2.resize(img,(0,0), fx = 0.10, fy=0.10)

cv2.imshow('final',img2)

cv2.waitKey()
cv2.destroyWindow()