# !/usr/bin/env python

__author__ = "Arjun Tejani"
__version__ = "0.0.1"
__status__ = ""

import cv2
import numpy as np
from datetime import datetime
import math, os, glob, ctypes
import matplotlib.pyplot as plt
import logging


def setup_logger(name, log_file, level=logging.DEBUG):
    """Function setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # '%(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


class camera_calibration:
    def __init__(self, N_checkerboard_height, N_checkerboard_width):

        self.N_checkerboard_height = N_checkerboard_height
        self.N_checkerboard_width = N_checkerboard_width

        self.CHECKERBOARD = (N_checkerboard_height, N_checkerboard_width)
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Creating vector to store vectors of 3D points for each checkerboard image
        self.objpoints = []
        # Creating vector to store vectors of 2D points for each checkerboard image
        self.imgpoints = []

        # Defining the world coordinates for 3D points
        self.objp = np.zeros((1, self.CHECKERBOARD[0] * self.CHECKERBOARD[1], 3), np.float32)
        self.objp[0, :, :2] = np.mgrid[0:self.CHECKERBOARD[0], 0:self.CHECKERBOARD[1]].T.reshape(-1, 2)

        # flags
        self.prev_img_shape = None

    def capture_from_images(self, path_to_folder):
        ret = False
        files = glob.glob(path_to_folder + '*jpg')
        for file in files:
            im_src = cv2.imread(file)
            gray = cv2.cvtColor(im_src, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                     cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

            """
            If desired number of corner are detected,
            we refine the pixel coordinates and display 
            them on the images of checker board
            """
            if ret == True:
                self.objpoints.append(self.objp)
                # refining pixel coordinates for given 2d points.
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgpoints.append(corners2)
                # Draw and display the corners
                im_src = cv2.drawChessboardCorners(im_src, self.CHECKERBOARD, corners2, ret)

            user32 = ctypes.windll.user32
            screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            if im_src.shape[0] > screensize[0]:
                im_src_ = cv2.resize(im_src, (0, 0), fx=screensize[0] / (2 * im_src.shape[0]),
                                     fy=screensize[0] / (2 * im_src.shape[0]))
            else:
                im_src_ = im_src
            cv2.imshow('img', im_src_)
            cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(datetime.fromtimestamp(datetime.timestamp(datetime.now())), end='')
        print(" added " + str(len(self.imgpoints)) + ' calib data frames; ' + str(
            len(files) - len(self.imgpoints)) + ' failed')
        self.calc_calibration_data(im_src)

    def capture_from_livefeed(self, camera_num=0):
        failed_frames = 0
        ret = None
        stop_capture = False
        cap = cv2.VideoCapture(camera_num)
        ret, im_src = cap.read()
        while not stop_capture:
            ret, im_src = cap.read()
            gray = cv2.cvtColor(im_src, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                     cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

            """
            If desired number of corner are detected,
            we refine the pixel coordinates and display 
            them on the images of checker board
            """
            if ret == True:
                # refining pixel coordinates for given 2d points.
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)

                # Draw and display the corners
                im_src = cv2.drawChessboardCorners(im_src, self.CHECKERBOARD, corners2, ret)
            else:
                failed_frames = failed_frames + 1

            cv2.imshow('img', im_src)
            k = cv2.waitKey(33)
            if k == 27:  # 'ESC' key to stop
                break
            elif k == 97:  # 'a' key to add new corners
                if ret:
                    self.objpoints.append(self.objp)
                    self.imgpoints.append(corners2)
                    print(datetime.fromtimestamp(datetime.timestamp(datetime.now())), end='')
                    print('\tadded new corners' + str() + '\tN_total: ' + str(len(self.imgpoints)))
                    corners2 = None
                else:
                    print(datetime.fromtimestamp(datetime.timestamp(datetime.now())), end='')
                    print('\tnothing to add, my friend!')
            elif k == 99:  # 'c' key to compare the latest corners
                if len(self.imgpoints) > 1:
                    a = self.imgpoints[-1]
                    b = self.imgpoints[-2]
                    L2_norm = []
                    for i in range(0, len(a)):
                        L2_norm.append(
                            math.sqrt(math.pow((a[i][0][0] - b[i][0][0]), 2) + math.pow((a[i][0][1] - b[i][0][1]), 2)))

                    fig = plt.figure()
                    ax = fig.add_axes([0, 0, 1, 1])
                    low = min(L2_norm)
                    high = max(L2_norm)
                    try:
                        plt.ylim([math.ceil(low - 0.5 * (high - low)), math.ceil(high + 0.5 * (high - low))])
                    except:
                        plt.ylim([0, math.ceil(high + 0.5 * (high - low))])

                    x = np.arange(len(L2_norm))
                    ax.bar(x, L2_norm)
                    # ax.plot([0., 4.5], [threshold, threshold], "k--")

                    plt.show()
                else:
                    print('not enough datapoints')

            elif k == -1:  # normally -1 returned,so don't print it
                continue
            else:
                print(k)
                pass
        cv2.destroyAllWindows()
        cap.release()
        print(datetime.fromtimestamp(datetime.timestamp(datetime.now())), end='')
        print(" added " + str(len(self.imgpoints)) + ' calib data frames; ' + str(failed_frames) + ' failed')
        self.calc_calibration_data(im_src)

    def capture_from_videofile(self, vid_path, skip_frames=25):
        if os.path.exists(vid_path):
            failed_frames = 0
            frame_count = 0
            ret = None
            cap = cv2.VideoCapture(vid_path)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            while (cap.isOpened()):
                ret, im_src = cap.read()

                if frame_count == length - 1:
                    break
                if frame_count % skip_frames != 0:
                    frame_count = frame_count + 1
                    continue

                frame_count = frame_count + 1

                try:
                    gray = cv2.cvtColor(im_src, cv2.COLOR_BGR2GRAY)
                except:
                    break
                ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                         cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

                """
                If desired number of corner are detected,
                we refine the pixel coordinates and display 
                them on the images of checker board
                """
                if ret == True:
                    self.objpoints.append(self.objp)
                    # refining pixel coordinates for given 2d points.
                    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                    self.imgpoints.append(corners2)
                    # Draw and display the corners
                    im_src = cv2.drawChessboardCorners(im_src, self.CHECKERBOARD, corners2, ret)
                else:
                    failed_frames = failed_frames + 1

                user32 = ctypes.windll.user32
                screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
                if im_src.shape[1] > screensize[0]:
                    im_src_ = cv2.resize(im_src, (0, 0), fx=screensize[0] / (2 * im_src.shape[0]),
                                         fy=screensize[0] / (2 * im_src.shape[0]))
                else:
                    im_src_ = im_src
                cv2.imshow('img', im_src_)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        else:
            print(datetime.fromtimestamp(datetime.timestamp(datetime.now())), end='')
            print(' 404 - file does not exist')

        print(datetime.fromtimestamp(datetime.timestamp(datetime.now())), end='')
        print(" added " + str(len(self.imgpoints)) + ' calib data frames; ' + str(failed_frames) + ' failed')
        try:
            self.calc_calibration_data(im_src)
        except:
            pass

    def calc_calibration_data(self, im_src):
        if len(self.imgpoints) > 0:
            h, w = im_src.shape[:2]
            gray = cv2.cvtColor(im_src, cv2.COLOR_BGR2GRAY)

            """
            Performing camera calibration by 
            passing the value of known 3D points (objpoints)
            and corresponding pixel coordinates of the 
            detected corners (imgpoints)
            """
            try:
                ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints,
                                                                                       gray.shape[::-1],
                                                                                       None, None)
                print("Camera matrix : \n")
                print(self.mtx)
                print("dist : \n")
                print(self.dist)
                print("rvecs : \n")
                print(self.rvecs)
                print("tvecs : \n")
                print(self.tvecs)

                del self.objpoints
                del self.imgpoints
            except:
                print("failed to calculate calibration matricies")
        else:
            print(datetime.fromtimestamp(datetime.timestamp(datetime.now())), end='')
            print(' failed due to lack of image data')

    def undistort_fisheye(img_path, DIM, K, D):
        img = cv2.imread(img_path)
        h, w = img.shape[:2]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        cv2.imshow("undistorted", undistorted_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def undistort_image(self, img_path):
        im = cv2.imread(img_path)[..., ::-1]
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im_undistorted = cv2.undistort(im, self.mtx, self.dist)
        result = cv2.hconcat([im, im_undistorted])
        res_small = cv2.resize(result, (0, 0), fx=0.125, fy=0.125)
        cv2.imshow('small_preview', res_small)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def undistort_live_feed(self):
        stop_capture = False
        cap = cv2.VideoCapture(0)
        while not stop_capture:
            ret, im = cap.read()
            im_undistorted = cv2.undistort(im, self.mtx, self.dist)
            result = cv2.hconcat([im, im_undistorted])
            cv2.imshow('small_preview', result)
            if cv2.waitKey(1) & 0xFF == 27:  # ord('q'):
                stop_capture = True

    def undistort_video_file(self, vid_path):
        if os.path.isfile(vid_path):
            cap = cv2.VideoCapture(vid_path)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            while (cap.isOpened()):
                ret, im_src = cap.read()
                im_undistorted = cv2.undistort(im_src, self.mtx, self.dist)
                result = cv2.hconcat([im_src, im_undistorted])
                res_small = cv2.resize(result, (0, 0), fx=0.25, fy=0.25)
                cv2.imshow('small_preview', res_small)
                cv2.waitKey(1)
            cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    calib = camera_calibration(6, 8)

    calib.capture_from_videofile('C:/Users/S8636452/PycharmProjects/Spielplatz/CameraCalibration/video/C0003.MP4')
    calib.undistort_video_file('C:/Users/S8636452/PycharmProjects/Spielplatz/CameraCalibration/video/C0004.MP4')

    # calib.capture_from_images('C:/Users/S8636452/PycharmProjects/Spielplatz/CameraCalibration/images1/')
    # calib.undistort_image('C:/Users/S8636452/PycharmProjects/Spielplatz/CameraCalibration/_DSC2533.JPG')

    calib.capture_from_livefeed()
    calib.undistort_live_feed()