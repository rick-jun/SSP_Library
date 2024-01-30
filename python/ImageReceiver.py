import time
import cv2
from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context, render_template
import threading

outputFrame = None
lock = threading.Lock()
frame = None
global cap
class ImageReceiver :

    def __init__(self, source):
        global cap

        self._source = source
        cap = cv2.VideoCapture(source)

    def camConn(self):
        global outputFrame, lock, frame, cap
        if cap.isOpened():

            while True:
                ret_val, frame = cap.read()
                if frame.shape:
                    frame = cv2.resize(frame, (1520,600))
                    with lock:
                        outputFrame = frame.copy()
                else:
                    continue 
        else:
            print('camera open failed')

    def generate(self):
        # grab global references to the output frame and lock variables
        global outputFrame, lock, frame
    
        # loop over frames from the output stream
        while True:
            # wait until the lock is acquired
            with lock:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if outputFrame is None:
                    continue
    
                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
    
                # ensure the frame was successfully encoded
                if not flag:
                    continue
    
            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')
    
    def capture(self) :
        global outputFrame, lock, frame

        try :
            cv2.imwrite('img/alarm2/img.bmp', frame)

            return 'success'
        except :
            return 'fail'

