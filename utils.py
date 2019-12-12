import cv2
import numpy as np
from  more_itertools import unique_everseen



def most_frequent(arr):

    (values, counts) = np.unique(arr, return_counts=True)
    most_freq = values[np.argmax(counts)] 

    if most_freq == 0:
        arr = arr[ arr != most_freq]
        (values, counts) = np.unique(arr, return_counts=True)
        most_freq = values[np.argmax(counts)] 


    return most_freq

def display_image(label, image):
    cv2.imshow(label, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def convert_to_binary(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return thresh


def convert_to_binary_and_invert(image):
    # convert to greyscale then flip black and white
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh


def get_distance_between_words(distances):

    distances_soreted = sorted(distances, key=distances.count,reverse=True)
    distances_soreted = list(unique_everseen(distances_soreted))
    distance = max(distances_soreted[:3])
    return distance

    

def thin_image(img):
    # img = convert_to_binary(img)
    
    # ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    skel = np.zeros(img.shape, np.uint8)
    size = np.size(img)
    done = False
    while (not done):
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

    return skel

#TODO: test this template with letters like R
def match_template(image):
    height = 8
    width = 8
    template = np.zeros((height, width))
    for i in range(2, height):
        for j in range(3, width):
            if (i == 2 and j == 3) or (i == 2 and j == 4):
                continue
        template[(i, j)] = 255

        
            
