import cv2
import glob, math, os, ctypes, logging
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def setup_logger(name, log_file, level=logging.DEBUG):
    """Function setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')#'%(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


import os