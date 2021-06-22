import cv2 as cv
import numpy as np
import math
from numpy.lib.function_base import append
import predict_interface as pi
from task_types import Task_type


def lettercropping(image, roi, task_types):

    # minimal letter hight
    min_letter = 28

    # cut the region of interest
    roim = image[roi[1]:roi[3], roi[0]:roi[2]]
    # the shape of the ROI
    (width, _, _) = roim.shape
    # from color to grayscale
    gray = cv.cvtColor(roim, cv.COLOR_BGR2GRAY)
    # threshold the picture to get the inverted colors with out error pixels
    _, thresh1 = cv.threshold(gray.copy(), 0, 225, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)

    # now get the seperated lines
    rect_kernal = cv.getStructuringElement(cv.MORPH_RECT, (width,1))

    # dilate all pixels to left and right so I can seperate the lines. 
    dilatation = cv.dilate(thresh1,rect_kernal,iterations=3)

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
        letters_as_arrays.append(letters_from_line(thresh1, rect, task_types))
        letters_as_arrays.append('\n')

    str_letters = ""
    for line in letters_as_arrays:
        for char in line:
            str_letters += str(char)

    print(str_letters)
    return str_letters

#-----------------------------------------------------

def letters_from_line(image, roi, task_types):

    # get the new region of interesst
    line = image[roi[1]:roi[3], roi[0]:roi[2]]

    # find the outlaying contours
    contours, _ = cv.findContours(line.copy(), cv.RETR_EXTERNAL , cv.CHAIN_APPROX_NONE)

    # sorting from left to right 
    cnts = sorted(contours, key=lambda cnt: cv.boundingRect(cnt)[0])

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
        # cut the individual character out of the image
        roi = image_copy[y:y+h, x:x+w]
        _, thresh = cv.threshold(roi, 125,255, cv.THRESH_BINARY)

        resized = enlarge_image(thresh)
        padded = resized.reshape(-1,28,28)
        padded = padded.astype(np.float32)

        letters.append(pi.ocr_pre(padded, task_types))



    return letters

# -----------------------------------------------------------------------

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
        image = cv.resize(image, (cols, rows))
    colsPadding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
    rowsPadding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
    image = np.lib.pad(image, (rowsPadding, colsPadding), 'constant')
    return image
