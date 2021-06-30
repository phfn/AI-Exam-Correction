import cv2 as cv
import itertools
from PIL import Image


'''
This function will accept a picture as a numpy array.
You can load a picture as an array by using imageio.

'''
# get the big boxes out the little ones. 
def __checkbox_checker(boxes):
    if len(boxes) <= 1:
        return boxes
    tempbox = []
# checking if any boxes are intersecting to make big boxes out of them. 
    for box in boxes:
        add = True
        for rec in boxes:
            t = intersection(box, rec)
            if t == None or (t[0] == rec[0] and t[1] == rec[1] and t[2] == rec[2] and t[3] == rec[3]):
                continue
            else:
                box = union(box, rec)
                add = False
        if add:
            tempbox.append(box)
    sorted(tempbox)
    newbox = list(tempbox for tempbox,_ in itertools.groupby(tempbox))

    return newbox

# combines two rectangels to a bigger one. 
def union(a,b):
  x = min(a[0], b[0])
  y = min(a[1], b[1])
  w = max(a[0], b[2])
  h = max(a[3], b[3])
  return [x, y, w, h]

# function to check if two rectangels are intersecting. 
# the return value of x,y,w,h is just to be able to make something else with thie function.
def intersection(a,b):
  x = max(a[0], b[0])
  y = max(a[1], b[1])
  w = min(a[2], b[2])
  h = min(a[3], b[3])
  if w - x >= 0 and h - y >= 0:
      return [x, y, w, h]
  return

def find_checkboxes(picture, roi, margin=26):
    if margin == 0: margin = 1
    # cut the roi
    roim = picture[roi[1]:roi[3], roi[0]:roi[2]]
    image = roim.copy()

    # this is for detecting the checkboxes
    cksize =  3 * margin
    # to paint the rectangles of the checkboxes
    drawing = image.copy()

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    _, bin_img = cv.threshold(gray, 0, 255,  cv.THRESH_OTSU)
    bin_img = ~bin_img
    # x and y kernals to define the checkboxes
    line_min_width = margin
    kernal_h = cv.getStructuringElement(cv.MORPH_RECT, (1,line_min_width))
    kernal_v = cv.getStructuringElement(cv.MORPH_RECT, (line_min_width,1))
    # now use the kernals to find only the checkboxes
    bin_img_h = cv.morphologyEx(bin_img, cv.MORPH_OPEN, kernal_h)
    bin_img_v = cv.morphologyEx(bin_img, cv.MORPH_OPEN, kernal_v)
    # merge the x and y pictures
    bin_img_final = bin_img_h | bin_img_v
    # find the contours of the checkboxes
    contours, hierachy = cv.findContours(bin_img_final, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # list for the checkboxes
    checkboxes = []
    # iterate over all contours and check if it is a checkbox. 
    for i in range(len(contours)):
        color = (0,0,255)
        myvar1 = cv.arcLength(contours[i], True)
        approx = cv.approxPolyDP(contours[i], 0.02 * myvar1, True)
        (x,y,w,h) = cv.boundingRect(approx)
        aspect_ratio = float(w) / h
        if aspect_ratio >= 0.8 and aspect_ratio <= 1.2 and (w + h) < cksize:
            checkboxes.append([x,y,x+w,y+h])
    # used if there are some boxes inside boxes
    checkboxes = __checkbox_checker(checkboxes)
    # sorting the boxes
    checkboxes = sortCheckboxes(checkboxes)

    crossed_boxes = []
    i=1
    for box in checkboxes:
        cv.rectangle(drawing, (box[0],box[1]), (box[2], box[3]), (0,0,255),2)
        cv.putText(drawing, str(i), (box[0], box[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        b = countCheckboxPixels(box, drawing)
        if str(b) == 'x':
            crossed_boxes.append(i)
        cv.putText(drawing, str(b), (box[0]-int(margin), box[1]+int(margin)), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        i += 1
    drawing = cv.cvtColor(drawing, cv.COLOR_RGB2BGR)
    drawing = Image.fromarray(drawing)
    return crossed_boxes, drawing


def countCheckboxPixels(checkbox, img):
    # get the region of interest by cropping it out of the array
    roi = img[checkbox[1]:checkbox[3], checkbox[0]:checkbox[2]]
    # from coloful to gray
    roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    # from gray to black and white
    roi = cv.threshold(roi, 220, 255, cv.THRESH_BINARY_INV)[1]
    # counting the pixels in the roi
    (w,h) = roi.shape
    pixels = w*h
    # counting the white pixels. thanks to the THRESH_BINARY_INV white is now black :)
    white_pixels = cv.countNonZero(roi)
    # how much is filled and return the answer
    filled = white_pixels/pixels
    if filled <= 0.4:
        return 'o'
    elif  0.4 < filled < 0.85:
        return 'x'
    else:
        return 'm'


def sortCheckboxes(boxes):
    return sorted(boxes, key=lambda box: [box[1], box[0]])

