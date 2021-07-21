import cv2 as cv
import itertools
from PIL import Image
import Task

'''
This function will accept a picture as a numpy array.
You can load a picture as an array by using imageio.

'''

def find_checkboxes(picture, roi, task:Task, correcting:bool): 
    red = (0,0,255)
    green = (0,255,0)
    blue = (255,0,0)

    dynamic_thickness = (2 / 1654) * picture.shape[1]
    line_thickness = int(abs(dynamic_thickness))
    # line_thickness = line_thickness if line_thickness > 1 else 2
    line_thickness = (2, line_thickness)[line_thickness > 1]
    font_scale = 0.9 * line_thickness

    # cut the roi
    roim = picture[roi[1]:roi[3], roi[0]:roi[2]]
    image = roim.copy()

    # to paint the rectangles of the checkboxes
    drawing = image.copy()

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.blur(gray, (5,5))

    _, bin_img = cv.threshold(gray, 120, 255,  cv.THRESH_OTSU)
    bin_img = ~bin_img



    contours, _ = cv.findContours(bin_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # list for the checkboxes
    checkboxes = []
    # iterate over all contours and check if it is a checkbox. 
    for i in range(len(contours)):
        arcLength = cv.arcLength(contours[i], True)
        approx = cv.approxPolyDP(contours[i], 0.02 * arcLength, True)
        (x,y,w,h) = cv.boundingRect(approx)
        aspect_ratio = float(w) / h
        if aspect_ratio >= 0.8 and aspect_ratio <= 1.2 :
            checkboxes.append([x,y,x+w,y+h])
    # used if there are some boxes inside boxes
    checkboxes = __checkbox_checker(checkboxes)
    # sorting the boxes
    checkboxes = sortCheckboxes(checkboxes)

    expected = []



    if correcting:
        answer = task.expected_answer.split(",")
        for i in answer:
            expected.append(int(i))


    crossed_boxes = []
    i=1
    for box in checkboxes:
        # cv.putText(drawing, str(i), (box[0], box[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        b = countCheckboxPixels(box, drawing)
        if str(b) == 'x':
            crossed_boxes.append(i)
        if correcting:
            # correct answer
            if i in expected and i in crossed_boxes:
                cv.rectangle(drawing, (box[0],box[1]), (box[2], box[3]), green, line_thickness)
                cv.putText(drawing, b, (box[0], box[1]+ (box[3] - box[1]) // 2), cv.FONT_HERSHEY_SIMPLEX, font_scale, green, line_thickness) 
            # checkbox missed 
            elif i in expected and i not in crossed_boxes:
                cv.rectangle(drawing, (box[0],box[1]), (box[2], box[3]), red, line_thickness)
                cv.putText(drawing, 'x', (box[0], box[1]+ (box[3] - box[1]) // 2), cv.FONT_HERSHEY_SIMPLEX, font_scale, red, line_thickness) 
            # wring checkbox
            elif i not in expected and i in crossed_boxes:
                cv.rectangle(drawing, (box[0],box[1]), (box[2], box[3]), red, line_thickness)
                cv.putText(drawing, '_', (box[0], box[1]+ (box[3] - box[1]) // 2), cv.FONT_HERSHEY_SIMPLEX, 2, red, line_thickness) 
            # not wrong just empty or filled
            else:
                cv.rectangle(drawing, (box[0],box[1]), (box[2], box[3]), blue, line_thickness)
                cv.putText(drawing, b, (box[0], box[1]+ (box[3] - box[1]) // 2), cv.FONT_HERSHEY_SIMPLEX, font_scale, blue, line_thickness) 
        else:
            cv.rectangle(drawing, (box[0],box[1]), (box[2], box[3]), blue, line_thickness)
            cv.putText(drawing, b, (box[0], box[1]+ (box[3] - box[1]) // 2), cv.FONT_HERSHEY_SIMPLEX, font_scale, green, line_thickness) 
        i += 1

    drawing = cv.cvtColor(drawing, cv.COLOR_RGB2BGR)
    drawing = Image.fromarray(drawing)
    my_answer = [str(i) for i in crossed_boxes]
    answer = ",".join(my_answer)
    return answer, drawing


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







