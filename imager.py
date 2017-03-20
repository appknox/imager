import argparse
import cv2
from matplotlib import pyplot as plt

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True,
                help="input image's path")

args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# blur, to remove sharp edges
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# adaptively thresholding to make binary
thresholded = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# OPTIONAL - use edge detection
edged = cv2.Canny(thresholded, 30, 200)

# find countours in the image
im2, contours, hierarchy = cv2.findContours(
    thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

rects = []
peris = []

for c in contours:
    # approximating the contour
    peri = cv2.arcLength(c, True)
    peris.append(peri)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # check if the approximated contour has four points
    # if so, it can be labelled as a rectangle
    if len(approx) == 4:
            rects.append(approx)

# drawing the countours
countered = cv2.drawContours(image.copy(), rects, -1, (255, 0, 0), 3)

# plotting the images
images = [image, thresholded, edged, countered]
titles = ["original", "thresholded", "edge detection", "result"]

for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
