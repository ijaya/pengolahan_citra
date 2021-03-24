from collections import deque
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())




if not args.get("video", False):
    camera = cv2.VideoCapture(1)
else:
    camera = cv2.VideoCapture(args["video"])

while True:
    (grabbed, frame) = camera.read()

    if args.get("video") and not grabbed:
        break

    frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    greenLower = np.array([51, 55, 102], np.uint8)
    greenUpper = np.array([98, 255, 255], np.uint8)


    #masking warna hijau
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations= 2)
    contours_green = frame.copy()
    contours_g, hierarchy_g = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # masking merah
    red_lower = np.array([0, 155, 62], np.uint8)
    red_upper = np.array([9, 255, 255], np.uint8)
    mask_r = cv2.inRange(hsv, red_lower, red_upper)
    mask_r = cv2.erode(mask_r, None, iterations=2)
    mask_r = cv2.dilate(mask_r, None, iterations=10)
    contours_red = frame.copy()
    cotour_r, hierarchy_r = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



    #Bound Hijau
    for i, it in enumerate(contours_g):
        bbox = cv2.boundingRect(it)
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
        __M = cv2.moments(it)
        cx = int(__M['m10'] / __M['m00'])
        cy = int(__M['m01'] / __M['m00'])
        cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -3)

        if len(bbox) < 2:
            continue

        for i in range(0, len(bbox) - 1):
            a = bbox[i]
            b = bbox[i + 1]
            cv2.line(frame, (a*cx, a*cy), (b*cx, b*cy), (0, 255, 266), 3)


    for a, this in enumerate(cotour_r):
        M2 = cv2.moments(this)
        cbox = cv2.boundingRect(this)
        x, y, w, h = cbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
        cx2 = int(M2['m10'] / M2['m00'])
        cy2 = int(M2['m01'] / M2['m00'])
        cv2.circle(frame, (cx2, cy2), 5, (0, 255, 255), -3)


    cv2.imshow("frame", frame)
    cv2.imshow("G Mask", mask)
    cv2.imshow("R mask",mask_r)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

