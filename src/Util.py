'''
Mentor - Mr.Prashant Kaushik 
Author - Hrishikesh Singh & Shivan Trivedi
'''

# Import Libraries
import time, math, cProfile, numpy, cv2, subprocess
import cv2 as cv
from collections import deque
from PIL import Image , ImageOps , ImageEnhance
from scipy.cluster import vq
import matplotlib
import matplotlib.pyplot as plt

# Constants
CAMERA_INDEX = 0
SCALE_FACTOR = 10  # video size will be 1/SCALE_FACTOR
FACE_CLASSIFIER_PATH = "classifiers/haar-face.xml"
EYE_CLASSIFIER_PATH = "classifiers/haar-eyes.xml"
FACE_MIN_SIZE = 0.2
EYE_MIN_SIZE = 0.03

DISPLAY_SCALE = 0.3333
FACE_SCALE = 0.25
EYE_SCALE = 0.33333

class Util:
    def __init__(self):
        print('0')
    
    @staticmethod
    def contrast(img, amount='auto'):
        """
		Modify image contrast
		Args:
			img (numpy array)			Input image array
			amount (float or string)  	Either number (e.g. 1.3) or 'auto'
		"""
        pilIMG = Image.fromarray(img)

        if amount is 'auto':
            pilEnhancedIMG = ImageOps.autocontrast(pilIMG, cutoff=0)
            return numpy.asarray(pilEnhancedIMG)
        else:
            pilContrast = ImageEnhance.Contrast(pilIMG)
            pilContrasted = pilContrast.enhance(amount)
            return numpy.asarray(pilContrasted)

    @staticmethod
    def threshold(img, thresh):
        """Threshold an image"""

        pilIMG1 = Image.fromarray(img)
        pilInverted1 = ImageOps.invert(pilIMG1)
        inverted = numpy.asarray(pilInverted1)
        r, t = cv2.threshold(inverted, thresh, 0, type=cv2.THRESH_TOZERO)
        pilIMG2 = Image.fromarray(t)
        pilInverted2 = ImageOps.invert(pilIMG2)
        thresholded = numpy.asarray(pilInverted2)
        return thresholded

    @staticmethod
    def equalizeHSV(img, equalizeH=False, equalizeS=False, equalizeV=True):
        """
		Equalize histogram of color image using BSG2HSV conversion
		"""
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(imgHSV)

        if equalizeH:
            h = cv2.equalizeHist(h)
        if equalizeS:
            s = cv2.equalizeHist(s)
        if equalizeV:
            v = cv2.equalizeHist(v)

        hsv = cv2.merge([h, s, v])
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return bgr

