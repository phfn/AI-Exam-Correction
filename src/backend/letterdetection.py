from typing import Text
import cv2 as cv
import numpy as np
import math
from numpy.lib.function_base import append
import predict_interface as pi
from task_types import Task_type


def letter_slicer(image, roi, task_types):
    ''' 
    This function is used to find letters and return them as a string.

    Parameters:
        image (opencv image): The picture or image to get analysed
        roi (list): the region of interest inside the given picture
        task_types(Task_types): this will be given to the KI interface
    '''
    # minimal letter hight
    min_letter = (28 / 1654) * image.shape[1]
    erosion_val = int(abs(min_letter / 14))

    erosion_val = erosion_val if erosion_val > 0 else 1

    # cut the region of interest
    roim = image[roi[1]:roi[3], roi[0]:roi[2]]


    # the shape of the ROI
    heigth = roim.shape[0]
    # from color to grayscale
    gray = cv.cvtColor(roim, cv.COLOR_BGR2GRAY)
    # threshold the picture to get the inverted colors with out error pixels
    _, thresh1 = cv.threshold(gray.copy(), 125, 225, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
    # for better seperation of the letters first a little erode
    erode_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (erosion_val, erosion_val))
    erosion = cv.erode(thresh1, erode_kernel)

    # now get the seperated lines
    rect_kernal = cv.getStructuringElement(cv.MORPH_RECT, (heigth * 2 ,1))

    # dilate all pixels to left and right so I can seperate the lines. 
    dilatation = cv.dilate(erosion,rect_kernal)

    # finding the contours of the dilated lines
    dilate_cont, dilate_hierachy = cv.findContours(dilatation.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # list for the rectangles around the dilated areas
    dilate_rectangles = []
    for i in range(len(dilate_cont)):
        if dilate_hierachy[0][i][3] == -1 and cv.boundingRect(dilate_cont[i])[3] > (min_letter // 2):
            (x,y,w,h) = cv.boundingRect(dilate_cont[i])
            dilate_rectangles.append([x,y,x+w,y+h])

    # sort the lines by y
    dilate_rectangles = sorted(dilate_rectangles, key=lambda box: box[1])

    # list for the 28*28 letters
    letters_as_arrays = []
    for rect in dilate_rectangles:
        letters_as_arrays.append(letters_from_line(thresh1, rect, task_types, erosion_val))
        letters_as_arrays.append(" ")

    str_letters = ""
    for line in letters_as_arrays:
        for char in line:
            str_letters += str(char).lower()

    return str_letters

# -----------------------------------------------------------------------

""" returns the letters from the given line """
def letters_from_line(image, roi, task_types, erosion_val):
    '''
    After the roi of the image has been seperated into several lines
    this function will 
    '''

    # get the new region of interesst
    line = image[roi[1]:roi[3], roi[0]:roi[2]]
    line_heigth, line_width = line.shape[:2]

    # erode the picture again so th contours will be sharper
    erode_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (erosion_val, erosion_val))
    erosion = cv.erode(line, erode_kernel)
    # cut the upper part of the picture to dilate it downwards
    upper_heigth = line_heigth // 3 * 2
    upper_line = erosion[0:upper_heigth]
    
    upper_heigth, upper_width = upper_line.shape[:2]


    # dilate the upper part of the picture
    kernal = cv.getStructuringElement(cv.MORPH_RECT, ksize=(1, 2 * upper_heigth))

    upper_dilate = cv.dilate(upper_line, kernal, anchor=(0, 2 * upper_heigth - 1))

    dilate_line = erosion.copy()

    dilate_line[0:upper_heigth, 0:upper_width] = upper_dilate
    
    # give the image some blur so all parts should stick together
    dilate_line = cv.blur(dilate_line,(5,5))
    # find the outlaying contours
    contours, _ = cv.findContours(dilate_line, cv.RETR_EXTERNAL , cv.CHAIN_APPROX_NONE)
    
    # sorting from left to right 
    cnts = sorted(contours, key=lambda cnt: cv.boundingRect(cnt)[0])
    f = lambda x, y: abs(x-y)
    rectangles = [cv.boundingRect(x) for x in cnts]

    # for seperating the letters
    mean, sigma = mean_and_std_deviation(cnts, image.shape[1])

    # sadly I cant return the list from the function without an error. IDK y so I have to recalc it here. 
    dist = []
    for i in range(len(rectangles)-1):
        dist.append(abs(rectangles[i+1][0] - (rectangles[i][0] + rectangles[i][2])))
    dist.append(0)
    dist = [x if x < dilate_line.shape[1] * 0.6 else mean for x in dist ]
    
    # list for the found letter in 28*28 pixels
    letters = []

    # loop over the contours and for each contour create a mask. 
    # The masks will be used as a negative to write on. 
    for i in range(len(cnts)):
        mask = np.zeros_like(line)
        cv.drawContours(mask, cnts, i, (255,255,255), -1)
        _, mask = cv.threshold(mask, 125, 255, cv.THRESH_OTSU | cv.THRESH_BINARY)


        image_copy = line.copy()
        image_copy = cv.bitwise_and(image_copy, mask)
        (x,y,w,h) = cv.boundingRect(cnts[i])
        if line_width * 0.8 < w:
            continue
        # cut the individual character out of the image
        roi = image_copy[y:y+h, x:x+w]
        _, thresh = cv.threshold(roi, 125,255, cv.THRESH_BINARY)
        
        roi_pixels = h * w
        white_pixels = cv.countNonZero(roi)

        # dots will be ignored
        if white_pixels / roi_pixels > 0.75:
            continue
        
        # a nice blur so the pictures of the letters are smoother
        thresh = cv.blur(thresh, (5,5))


        resized = enlarge_image(thresh)
        padded = resized.reshape(-1,28,28)
        padded = padded.astype(np.float32)
        # send the preprocesssed pictures to the KI interface
        letter = pi.ocr_pre(padded, task_types)
        letters.append(letter)
        # trying to seperate the words. still not working perfect but still better than before
        if dist[i] > mean + sigma:
            letters.append(" ")


    return letters

# -----------------------------------------------------------------------

""" Gauss-distribution """
def mean_and_std_deviation(contours, width):
    # there is none if there are less than 2 items
    if len(contours) <= 2: return 0,0

    # get the rectangle for each contour
    rectangles = [cv.boundingRect(x) for x in contours]
    rectangles_dist = []
    # get the absolute distance between following rectangles
    for i in range(len(rectangles)-1):
        rectangles_dist.append(abs(rectangles[i+1][0] - (rectangles[i][0] + rectangles[i][2])))
    rectangles_dist = [x if x < width * 0.6 else 1 for x in rectangles_dist]
    
    # calc the mean
    rects_len = len(rectangles)
    mean = sum(rectangles_dist) / rects_len
    # calc the varianz and return the sqrt
    f = lambda x : (x - mean)**2
    varianz = sum([f(x) for x in rectangles_dist]) / (rects_len - 1)
    rectangles_dist.append(0)
    return mean, varianz**0.5


# -----------------------------------------------------------------------

""" please move this function to the KI Interface """
def enlarge_image(image):
    rows, cols = image.shape
    if rows > cols:
        factor = 20.0 / rows
        rows = 20
        cols = int(round(cols * factor))
        image = cv.resize(image, (cols, rows))
    else:
        factor = 20.0 / cols
        cols = 20
        rows = int(round(rows * factor))
        image = cv.resize(image, (cols, rows), interpolation=cv.INTER_CUBIC)
    colsPadding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
    rowsPadding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
    image = np.lib.pad(image, (rowsPadding, colsPadding), 'constant')
    padded = image.reshape(-1,28,28)
    padded = padded.astype(np.float32)

    return padded

# -----------------------------------------------------------------------

