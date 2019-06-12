#!/usr/bin/python
# coding: utf8
"""MMM-Facial-Recognition - MagicMirror Module
Face Recognition Script
The MIT License (MIT)

Copyright (c) 2016 Paul-Vincent Roll (MIT License)
Based on work by Tony DiCola (Copyright 2013) (MIT License)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import json
import time
import face
import cv2
import config
import signal

to_node("status", "Facerecognition started...")

# Setup variables
current_user = None
last_match = None
detection_active = True
login_timestamp = time.time()
same_user_detected_in_row = 0

config = ConfigHandler()
interval = config.get("interval")

# Inital Detector and Recognizer
detector = config.get_detector()
recognizer =  config.get_recognizer()
to_node("status", "Facerecognition initialized...")

# get camera
camera = config.get_camera()
to_node("status", "Camera ready...")
signal.signal(signal.SIGINT, config.shutdown)

motion = MotionDetector

# sleep for a second to let the camera warm up
time.sleep(1)

#####Benchmark#######
time_detection = 0
time_recognition = 0
time_all = 0
###################

# Main Loop
while True:
    # Sleep for x seconds specified in module config
    time.sleep(interval)
    time_all = time.time() # BENCHMARK
    #Use PIR Sensor to 
    motionDetected = True # motion.IsMoving(camera);
    if (motionDetected == True):
        lastMotion = time.time()
        detection_active = True
    
    # if detecion is true, will be used to disable detection if you use a PIR sensor and no motion is detected
    if detection_active is True:
        # Get image
        image = camera.read()
        # Convert image to grayscale.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # Get coordinates of single face in captured image.
        time_detection = time.time() # BENCHMARK
        result = face.detect_single(image)
        time_detection = time_detection - time.time() # BENCHMARK
        # No face found, logout user?
        if result is None:
            counter_failed = counter_failed + 1
            # if last detection exceeds timeout and there is someone logged in -> logout!
            #if (current_user is not None and time.time() - login_timestamp > config.get("logoutDelay")):
            if (counter_failed > maxFails)
                # callback logout to node helper
                to_node("logout", {"user": current_user})
                same_user_detected_in_row = 0
                current_user = None
                detection_active = False
            continue
        
        # Set x,y coordinates, height and width from face detection result
        x, y, w, h = result
        # Crop image on face. If algorithm is not LBPH also resize because in all other algorithms image resolution has to be the same as training image resolution.
        #TODO: Move for appropriate algo into class
        if config.get("recognitionAlgorithm") == 1:
            crop = face.crop(image, x, y, w, h)
        else:
            crop = face.resize(face.crop(image, x, y, w, h))
        # Test face against model.
        time_recognition = time.time() # BENCHMARK
        label, confidence = model.predict(crop)
        time_recognition = time_recognition - time.time() # BENCHMARK
        # We have a match if the label is not "-1" which equals unknown because of exceeded threshold and is not "0" which are negtive training images (see training folder).
        if (label != -1 and label != 0):
            # Set login time
            login_timestamp = time.time()
            # Routine to count how many times the same user is detected
            if (label == last_match and same_user_detected_in_row < 2):
                # if same user as last time increment same_user_detected_in_row +1
                same_user_detected_in_row += 1
            if label != last_match:
                # if the user is diffrent reset same_user_detected_in_row back to 0
                same_user_detected_in_row = 0
            # A user only gets logged in if he is predicted twice in a row minimizing prediction errors.
            if (label != current_user and same_user_detected_in_row > 1):
                current_user = label
                # Callback current user to node helper
                to_node("login", {"user": label, "confidence": str(confidence)})
            # set last_match to current prediction
            last_match = label
            
        # if label is -1 or 0, current_user is not already set to unknown and last prediction match was at least 5 seconds ago
        # (to prevent unknown detection of a known user if he moves for example and can't be detected correctly)
        elif (current_user != 0 and time.time() - login_timestamp > 5):
            # Set login time
            login_timestamp = time.time()
            # set current_user to unknown
            current_user = 0
            # callback to node helper
            to_node("login", {"user": current_user, "confidence": None})
        else:
            continue
        
        time_all = time_all - time.time() # BENCHMARK

