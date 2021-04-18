import numpy as np
import argparse
import imutils
import cv2
import math

frame = cv2.imread('sample.JPG')

while True:
    canvasW = 800
    canvasH = 400
    frame = imutils.resize(frame, canvasW, canvasH)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Array Masker
    greenLower = np.array([54, 100, 100], np.uint8)
    greenUpper = np.array([179, 255, 255], np.uint8)
    red_lower = np.array([0, 71, 255], np.uint8)
    red_upper = np.array([81, 255, 255], np.uint8)

    # masking warna hijau
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours_green = frame.copy()
    contour_g, hierarchy_g = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # masking merah
    mask_r = cv2.inRange(hsv, red_lower, red_upper)
    mask_r = cv2.erode(mask_r, None, iterations=1)
    mask_r = cv2.dilate(mask_r, None, iterations=2)
    contours_red = frame.copy()
    contour_r, hierarchy_r = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    greenAr = []
    for i, it in enumerate(contour_g):
        hbox = cv2.boundingRect(it)
        x, y, w, h = hbox
        M = cv2.moments(it)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -3)
        mid = [cx, cy]
        greenAr.append(mid)

    # Bound Merah
    redAr = []
    for a, this in enumerate(contour_r):
        M2 = cv2.moments(this)
        cx2 = int(M2['m10'] / M2['m00'])
        cy2 = int(M2['m01'] / M2['m00'])
        rbox = cv2.boundingRect(this)
        x, y, w, h = rbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
        cv2.circle(frame, (cx2, cy2), 5, (0, 255, 255), -3)
        mid2 = [cx2, cy2]
        redAr.append(mid2)

    def getInBetween(allPoints, bottomMost, topMost):
        _res = [0 for i in range(canvasH)]
        _last = bottomMost
        for it in allPoints:
            x1 = _last[0]
            y1 = _last[1]
            x2 = it[0]
            y2 = it[1]
   #         print(x1, y1, x2, y2)
            for _y in range(_last[1], it[1] - 1, -1):
               # x = math.floor((((_y - y1) / (y2 - y1)) * (x2 - x1)) + x1)
               a = _y - y1
               b = y2 - y1
               c = x2 - y1
               print(f"y1 {y1} - y2 {y2}")
               compa = a/b
               idk = compa*c
               x = idk + x1
              # _res[_y] = x
            _last = it
        return _res

    _botMostMerah = (0, canvasH - 1)
    _botMostBiru = (canvasW - 1, canvasH - 1)
    _topMost = (canvasW // 2, 0)
    redX = getInBetween(greenAr, _botMostMerah, _topMost)
    biruX = getInBetween(redAr, _botMostBiru, _topMost)

    for _y in range(canvasH):
        xMerah = redX[_y]
        xBiru = biruX[_y]
        cv2.circle(frame, (xMerah, _y), 3, (255, 255, 255), 1)
        cv2.circle(frame, (xBiru, _y), 3, (255, 255, 255), 1)

    controlPoint = (canvasW // 2, 75)
    cv2.circle(frame, controlPoint, 2, (255, 255, 255), 1)
    a = abs(controlPoint[0] - redX[controlPoint[1]])
    b = abs(controlPoint[0] - biruX[controlPoint[1]])
    _err = (a - b) / 2
    _control = -1 * _err
    print(a, b, _err, _control)
    cv2.imshow("frame", frame)
    cv2.imshow("gren", mask)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
