import numpy as np
import cv2
import matplotlib.pyplot as plt
from utils import display_image, most_frequent


def get_baseline_y_coord(horizontal_projection):

    baseline_y_coord = np.where(horizontal_projection == np.amax(horizontal_projection))
    return baseline_y_coord[0][0]


def get_horizontal_projection(image):

    h, w = image.shape
    horizontal_projection = cv2.reduce(src=image, dim=-1, rtype=cv2.REDUCE_SUM, dtype=cv2.CV_32S)
    plt.plot(range(h), horizontal_projection.tolist())
    plt.savefig("./figs/horizontal_projection.png")
    return horizontal_projection


def get_vertical_projection(image):

    h, w = image.shape
    vertical_projection = []
    vertical_projection = cv2.reduce(src=image, dim=0, rtype=cv2.REDUCE_SUM, dtype=cv2.CV_32S)
    plt.plot(range(w), vertical_projection[0])
    plt.savefig("./figs/vertical_projection.png")
    return vertical_projection[0]


def deskew(image):
    # get all white pixels coords (the foreground pixels)
    coords = np.column_stack(np.where(image > 0))
    # minAreaRect computes the minimum rotated rectangle that contains the entire text region.
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    # now rotate the image with the obtained angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    # calculate rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated


def get_largest_connected_component(image):
    # image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=1)
    # image = cv2.dilate(image,  np.ones((2,2), np.uint8), iterations=1)

    # image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, np.ones((2,2), np.uint8))
    # image = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((2,2), np.uint8))

    # display_image("after erode+dilate", image)
    number_of_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
    sizes = stats[:, -1]

    max_label = 1
    max_size = sizes[1]
    for i in range(2, number_of_components):
        if sizes[i] > max_size:
            max_label = i
            max_size = sizes[i]
    print("max label is: ", max_label)
    image2 = np.zeros(output.shape)

    image2[output == max_label] = 255
    image2 = image2.astype(np.uint8)
    display_image("Biggest component", image2)

    return image2


def get_pen_size(image):

    vertical_projection = get_vertical_projection(image)
    most_freq_vertical = most_frequent(vertical_projection)

    horizontal_projection = get_horizontal_projection(image)
    most_freq_horizontal = most_frequent(horizontal_projection)

    
    # print("most frq hor: ", most_freq_horizontal)

    if most_freq_horizontal > most_freq_vertical:
        return most_freq_vertical
    return most_freq_horizontal
    

def segment_character(image):

    pen_size = get_pen_size(image)
    vertical_projection = get_vertical_projection(image)

    positions = np.where(vertical_projection == pen_size)
    print("pen size is: ", pen_size)
    print("positions is: ", positions[0], sep='\n')
    positions = positions[0]

    count = 0
    consective = False
    length_consective = []
    point_positions = []
    for i in range(1, len(positions)):

        if not consective:
            if positions[i-1] + 1 == positions[i]:
                count  = 1
                consective = True

        else:
            if positions[i-1] + 1 != positions[i]:
                consective = False
                length_consective.append(count+1)
                point_positions.append(i)


            else:
                count += 1

    print("point positions is", point_positions)
    print("length_consective is", length_consective)
    print("postions is: ", positions)

    segmenataion_points = []
    for i in range(len(length_consective)):
        temp = positions[point_positions[i] - length_consective[i]:point_positions[i]]
        print("final point positions",temp)
        if len(temp) != 0:
            segmenataion_points.append(int(sum(temp)/len(temp)))

    print("final seg points", segmenataion_points)

    previous_width = 0
    (h,w) = image.shape
    for i in segmenataion_points:
        cv2.line(image, (i, 0), (i, h), (255, 255, 255), 1)

    # cv2.line(image, (segmenataion_points[-1], 0), (segmenataion_points[-1], h), (255, 255, 255), 1)
    display_image("char seg",image)