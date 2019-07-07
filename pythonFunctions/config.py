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
    _config_storage = None
    
    def __init__(config_json):
        self.config_storage = json.loads(config_json)#(sys.argv[1])
    
    def get(key):
        return config_storage[key]
    
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
        detectorModel = get("DETECTION_ALGORITHM")
        if detectorModel == "haar":
            return FaceDetector_HAAR(self.get("HAAR_FACES_LOCATION"), self.get("HAAR_DETECTOR_ARGS")
        elif detectorModel == "ocv_dnn":
            return FaceDetector_DNN(self.get("DNN_DETECTOR_MODEL_LOCATION"), self.get("DNN_DETECTOR_CONFIG_LOCATION")):
        elif detectorModel == "dlib_cnn":
            return FaceDetector_DLIB_CNN(self.get("DLIB_CNN_MODEL_LOCATION"), self.get("DLIB_CNN_DETECTOR_ARGS"))
        else:
            detector = FaceDetector_HOG()
            detector.function_args = self.get("HOG_DETECTOR_ARGS")
            return detector
        
    def get_recognizer():
        recognizerModel = ("RECOGNITION_ALGORITHM")
        if  recognizerModel == "dlib_face_encoding":
            recognizer = FaceRecognizer_DLIB_CNN(self.get("DLIB_RECOGNITION_MODEL_LOCATION"), self.get("FACE_DESCRIPTOR_LOCATION"))
            recognizer.tolerance = self.get("DLIB_RECOGNITION_TOLERANCE")
            return recognizer
        else:
            return FaceRecognizer_Classic(config.get("CLASSIC_TRAINING_FILE"))
        
