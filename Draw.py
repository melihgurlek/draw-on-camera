from configparser import SafeConfigParser
from winreg import HKEY_LOCAL_MACHINE
import cv2 as cv
import numpy as np

frameWidth = 800
frameHeight = 600
capture = cv.VideoCapture(0)

capture.set(3, frameWidth)
capture.set(4, frameHeight)
capture.set(10, 140)

Colors = [[101, 114, 69, 130, 255, 255],
          [139, 139, 168, 174, 255, 255]]

ColorValues = [[188, 16, 56],
               [196, 72, 251]]

Points = []


def FindColor(img, Colors, ColorValues):
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for color in Colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv.circle(imgResult, (x, y), 10, ColorValues[count], cv.FILLED)
        if x != 0 and y != 0:
            new_points.append([x, y, count])
        count += 1
    return new_points


def getContours(img):
    contours, hierarchy = cv.findContours(
        img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500:
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv.boundingRect(approx)
    return x + w // 2, y


def DrawOnScreen(Points, ColorValues):
    for point in Points:
        cv.circle(imgResult, (point[0], point[1]),
                  10, ColorValues[point[2]], cv.FILLED)


while True:
    success, img = capture.read()
    imgResult = img.copy()
    new_points = FindColor(img, Colors, ColorValues)

    if len(new_points) != 0:
        for points in new_points:
            Points.append(points)

    if len(Points) != 0:
        DrawOnScreen(Points, ColorValues)

    cv.imshow("Result", imgResult)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
