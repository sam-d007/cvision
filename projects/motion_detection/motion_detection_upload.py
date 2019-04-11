# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import datetime


vs = VideoStream(src=0).start()
time.sleep(2.0)

#initialize the static variables
frames_array =[]
(h, w) = (None, None)
fourcc = cv2.VideoWriter_fourcc(*"DIVX")
writer = None
avg = None
firstFrame = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
i = 0 
name = ""

#read the video stream

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    timestamp = datetime.datetime.now()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    text = "Unouccupied"
    (h, w) = frame.shape[:2]

     # if the first frame is None, initialize it
    if firstFrame is None:
    	firstFrame = gray
    	continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 120, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 1000:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    if text == "Occupied":
        if (timestamp - lastUploaded).seconds >= 1:
            (h, w) = frame.shape[:2]
            frames_array.append(frame) 
            i += 1
            name = str(i) + ".avi"
               

    # draw the text and timestamp on the frame

    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


    # frames_array = []

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
            break   


# writer = cv2.VideoWriter("custom.avi", fourcc, 30 ,(w , h ), True)
writer = cv2.VideoWriter(name, fourcc, 30 ,(w , h ), True)
for j in range(len(frames_array)):
    # writing to a image array
    writer.write(frames_array[j])

key = cv2.waitKey(1) & 0xFF
# print(frames_array)
# for i in range(len(frames_array)):
#     # writing to a image array
#     writer.write(frames_array[i])  

writer.release()
# cleanup the camera and close any open windows
vs.stop()
vs.release()
cv2.destroyAllWindows()
