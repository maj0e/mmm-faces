#!/usr/bin/python
# coding: utf8
"""MMM-Facial-Recognition - MagicMirror Module
Face Recognition script config
The MIT License (MIT)

Copyright (c) 2016 Paul-Vincent Roll (MIT License)
Based on work by Tony DiCola (Copyright 2013) (MIT License)
"""
import inspect
import os
import json
import sys
import platform

class ConfigHandler:
    _platform = platform.uname()[4]
    path_to_file = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    # Size (in pixels) to resize images for training and prediction.
    # Don't change this unless you also change the size of the training images.
    FACE_WIDTH = 92
    FACE_HEIGHT = 112

    # Face detection cascade classifier configuration.
    # You don't need to modify this unless you know what you're doing.
    # See: http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html
    HAAR_FACES = path_to_file + '/haarcascade_frontalface.xml'
    HAAR_SCALE_FACTOR = 1.3
    HAAR_MIN_NEIGHBORS = 4
    HAAR_MIN_SIZE = (30, 30)

    CONFIG = json.loads(sys.argv[1]);
    
    def get(key):
        return CONFIG[key]
    
    def to_node(type, message):
        # convert to json and print (node helper will read from stdout)
        try:
            print(json.dumps({type: message}))
        except Exception:
            pass
        # stdout has to be flushed manually to prevent delays in the node helper communication
        sys.stdout.flush()


    def shutdown(self, signum):
        to_node("status", 'Shutdown: Cleaning up camera...')
        camera.stop()
        quit()


    def get_camera():
        to_node("status", "-" * 20)
        try:
            if get("useUSBCam") == False:
                import picam
                to_node("status", "PiCam ausgewählt...")
                cam = picam.OpenCVCapture()
                cam.start()
                return cam
            else:
                raise Exception
        except Exception:
            import webcam
            to_node("status", "Webcam ausgewählt...")
            return webcam.OpenCVCapture(device_id=0)
            to_node("status", "-" * 20)
    
    def get_detector():
        if get("detectorModel") == 1:
            return FaceDetector_DLIB_CNN()
        else
            return FaceRecognizer_Classic()
    
    def get_recognizer():
        if get("recognizerModel") == 1:
            return FaceRecognizer_DLIB_CNN()
        else
            return FaceRecognizer_Classic()
        
