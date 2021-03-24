import cv2
import imutils

glower = (37, 53, 102)
gupper = (98, 255, 255)
rlower = (0, 155, 62)
rupper = (9, 245, 255)

camera = cv2.VideoCapture(1)

while True:
    (grabed, frame) = camera.read()
    frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    gmask = cv2.inRange(hsv,glower, gupper)
    gmask = cv2.erode(gmask, None, iterations=2)
    gmask = cv2.dilate(gmask, None, iterations=2)

    rmask = cv2.inRange(hsv, rlower, rupper)
    rmask = cv2.erode(rmask, None, iterations=2)
    rmask = cv2.dilate(rmask, None, iterations=2)

    gcount = cv2.findContours(gmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    rcount = cv2.findContours(rmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len (gcount) > 0:
        c = max(gcount, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        __M = cv2.moments(c)
        cx = int(__M['m10'] / __M['m00'])
        cy = int(__M['m01'] / __M['m00'])

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -3)

            if len (rcount) > 0:
                d = max(rcount, key= cv2.contourArea)
                ((x2, y2) , radius2) = cv2.minEnclosingCircle(d)
                __M = cv2.moments(d)
                cx2 = int(__M['m10'] / __M['m00'])
                cy2 = int(__M['m01'] / __M['m00'])

                if radius2 > 10:
                    cv2.circle(frame, (int(x2), int(y2)), int(radius2), (0, 255, 255), 2)
                    cv2.circle(frame, (cx2, cy2), 5, (0, 255, 255), -3)

                line = cv2.line(frame, (cx, cy), (cx2, cy2), (0, 255, 255), 3)



    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

