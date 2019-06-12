"""Raspberry Pi Face Recognition Treasure Box
Face Detection Helper Functions
Copyright 2013 Tony DiCola

Functions to help with the detection and cropping of faces.
"""

import cv2
import dlib

import config

##### Face Detection ################################################
class FaceDetector_HOG:
    """ FaceDetector class, which should wrap all detectors to follow the same api"""
    model = None                                    # Detection Model: Set in Init
    function_args = None                        # Argument Dictionary passed to detector_function
        
    def _init_():
            self.model = dlib.get_frontal_face_detector() #fastest on CPU
            self.function_args = { "number_of_times_to_upsample" : config.DLIB_CNN_UPSAMPLING }
    
    # Wrapper for the different detection methods
    def detect(image): 
        faces =  self.model(img, **self.function_args)
        return chooseFace_dlib(faces)
    
class FaceDetector_HAAR:
    """ FaceDetector class, which should wrap all detectors to follow the same api"""
    model = None                                    # Detection Model: Set in Init
    function_args = None                        # Argument Dictionary passed to detector_function
        
    def _init_():
        self.model cv2.CascadeClassifier(config.HAAR_FACES)
        self.function_args = { "scaleFactor" : config.HAAR_SCALE_FACTOR, "minNeighbors" : config.HAAR_MIN_NEIGHBORS, "minSize" : config.HAAR_MIN_SIZE, "flags": cv2.CASCADE_SCALE_IMAGE }
    
    # Wrapper for the different detection methods
    def detect(image): 
        faces = model.detectMultiScale(image, **self.function_args)
        return chooseFace(faces)

   
class FaceDetector_DNN:
    """ FaceDetector class, which should wrap all detectors to follow the same api"""
    model = None                                    # Detection Model: Set in Init
    function_args = None                        # Argument Dictionary passed to detector_function
        
    def _init_():
        self.model cv2.CascadeClassifier(config.OCV_DNN_MODEL_LOCATION)
        self.function_args = { }
    
    # Wrapper for the different detection methods
    def detect(image): 
        faces = model.detectMultiScale(image, **self.function_args)
        return chooseFace(faces)


class FaceDetector_DNN_DLIB:
    """ FaceDetector class, which should wrap all detectors to follow the same api"""
    model = None                                    # Detection Model: Set in Init
    function_args = None                        # Argument Dictionary passed to detector_function
        
    def _init_():
        self.model = dlib.cnn_face_detection_model_v1(config.DLIB_DETECTION_MODEL_LOCATION)
        self.function_args = { "number_of_times_to_upsample" : config.DLIB_CNN_UPSAMPLING }
    
    # Wrapper for the different detection methods
    def detect(image): 
        faces =  self.model(img, **self.function_args)
        return chooseFace_dlib(faces)
 

##### Face Recognition ##############################################
class FaceRecognizer_CLASSIC:
    model = None
    function_args = None
    face_descriptors = None
    list_of_names = None
    def _init_():
        self.model = getClassicRecognizerModel()
        self.model.load(config.get("trainingFile"))
        
    def predict(image):
        
class FaceRecognizer_DLIB_CNN:
    model = None
    function_args = None
    face_descriptors = None
    list_of_names = None
    
    def _init_():
        self.model = dlib.face_recognition_model_v1(config.DLIB_RECOGNITION_MODEL_LOCATION)
        # Load the descriptors for all known faces
        self.face_descriptors, self.list_of_names = loadDescriptors(config.DLIB_RECOGNITION_MODEL_LOCATION)
        self.function_args = {"tolerance" : config.DLIB_PREDICTION_TOLERANCE }
        
    def predict(image):
        face_descriptor_in = self.model.compute_face_descriptor(img, shape)
        #Compare the obtained face descriptor to the list of descriptors and return the minimum
        return  np.argmin(np.linalg.norm(face_encodings - face_to_compare, axis=1))

class FaceRecognizer:
        model = None
        recognize_function = None
        function_args = None
        
    def __init__(self, method ='cnn', custom_model_location = None):
        if (method = 'cnn')
            self.model = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)
        else if (method == 'cnn_tf')
        else if (method == 'custom') # You can provide a custom Dnn model via custom_model_location
            face_detector_location = 
            self.model = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)
        else: #Fallback to one of the Classical openCV recognizer (Eigen, etc)
            
    def predict(image):
    """Return bounds (x, y, width, height) of detected face in grayscale image.
    If no face or more than one face are detected, None is returned.
    """
    faces = self.recognize_function(image, function_args)
    if len(faces) != 1:
        return None
    return faces[0]

##### Utility functions #####
def chooseFace_dlib(face_list):
    if len(faces) == 1:
        return rect_ocv2dlib(faces[0])
    else if len(faces) == 0:
        return None
    else:   # Return the face with highest confidence
        return rect_ocv2dlib(max(faces, lambda f: f.confidence))

def chooseFace(face_list):
    if len(faces) == 1:
        return faces[0]
    else if len(faces) == 0:
        return None
    else:   # Return the largest face if several faces are detected
        return max(faces, lambda f: (f.height * f.width))

def rect_ocv2dlib(dlib_rect):
    rect.x = dlib_rect.left()
    rect.y = dlib_rect.top()
    rect.width = dlib_rect.left() - dlib_rect.right()
    rect.height = dlib_rect.top() - dlib_rect.bottom()
    return rect

def getClassicRecognizerModel():
# set algorithm to be used based on setting in config.js
    if config.get("recognitionAlgorithm") == 1:
        model = cv2.createLBPHFaceRecognizer(threshold=config.get("lbphThreshold"))
    elif config.get("recognitionAlgorithm") == 2:
        model = cv2.createFisherFaceRecognizer(threshold=config.get("fisherThreshold"))
    else:
        model = cv2.createEigenFaceRecognizer(threshold=config.get("eigenThreshold"))
    return model

def crop(image, x, y, w, h):
    """Crop box defined by x, y (upper left corner) and w, h (width and height)
    to an image with the same aspect ratio as the face training data.  Might
    return a smaller crop if the box is near the edge of the image.
    """
    crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
    midy = y + h / 2
    y1 = max(0, midy - crop_height / 2)
    y2 = min(image.shape[0] - 1, midy + crop_height / 2)
    return image[y1:y2, x:x + w]

def resize(image):
    """Resize a face image to the proper size for training and detection.
    """
    return cv2.resize(image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
