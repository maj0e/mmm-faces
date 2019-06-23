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
                cam = PiCam_OpenCVCapture()
                cam.start()
                return cam
            else:
                raise Exception
        except Exception:
            import webcam
            to_node("status", "Webcam ausgewählt...")
            return WebCam_OpenCVCapture(device_id=0)
            to_node("status", "-" * 20)
    
    def get_detector():
        detectorModel = get("detectorModel")
        if detectorModel == "HAAR":
            return FaceDetector_HAAR(self.get("HAAR_FACES_LOCATION"), self.get("HAAR_DETECTOR_ARGS")
        elif detectorModel == "OCV_DNN":
            return FaceDetector_DNN(self.get("DNN_DETECTOR_MODEL_LOCATION"), self.get("DNN_DETECTOR_CONFIG_LOCATION")):
        elif detectorModel == "DLIB_CNN":
            return FaceDetector_DLIB_CNN(self.get("DLIB_CNN_MODEL_LOCATION"), self.get("DLIB_CNN_DETECTOR_ARGS"))
        else:
            detector = FaceDetector_HOG()
            detector.function_args = self.get("HOG_DETECTOR_ARGS")
            return detector
        
    
    def get_recognizer():
        recognizerModel = ("recognizerModel")
        if  recognizerModel == "DLIB_CNN":
            recognizer = FaceRecognizer_DLIB_CNN(self.get("DLIB_RECOGNITION_MODEL_LOCATION"), self.get("FACE_ENCODINGS_LOCATION"))
            recognizer.tolerance = self.get("DLIB_RECOGNITION_TOLERANCE")
            return recognizer
        else:
            return FaceRecognizer_Classic(config.get("trainingFile"))
        
