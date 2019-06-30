"""
Different face detection and recognition algorithms from dlib and openCV wrapped in classes with a similar interface.


"""

import cv2
import dlib
import pickle
#import config

##### Face Detection ################################################
class FaceDetector_HOG:
    """ FaceDetector class, which wraps the HoG Method from dlib.
         Use this if you can't use a cuda enabled device and you encounter only frontal and slightly tilted faces.
    """
    model = None                                                                  # Detection Model: Set in Init
    function_args = { "number_of_times_to_upsample" : 1} # Argument Dictionary passed to detect func
    
    def __init__(self):
        self.model = dlib.get_frontal_face_detector() #fastest on CPU
        
    def detect(self, image): 
        faces =  self.model(image, 1)#**self.function_args)
        return chooseFace_dlib(faces)
    
class FaceDetector_HAAR:
    """FaceDetector class, which wraps the classic Haar Cascade Method from openCV.
        LEGACY: There is not really a reason to use this anymore. HOG is faster and probably more accurate. 
        OpenCV's DNN detector is more accurate and just as fast.
    """
    model = None                                    # Detection Model: Set in Init
    function_args = { "scaleFactor" : 1.3, "minNeighbors" : 4, "minSize" : (30, 30), "flags": cv2.CASCADE_SCALE_IMAGE } # Argument Dictionary passed to detector_function   
    
    def __init__(self, haar_faces_location):
        try:
            self.model = cv2.CascadeClassifier(haar_faces_location)
            if self.model == None:
                raise ValueError
        except ValueError:
            print("Could not load Haar Cascade Classifier!\n")
    
    def detect(self, image): 
        faces = model.detectMultiScale(image, **self.function_args)
        return chooseFace(faces)

class FaceDetector_DNN:
    """FaceDetector class, which wraps the detection method from OpenCv's dnn module.
        This Detector has state-of-the-art accuracy and is pretty fast on CPUs.
        Use this if you have more computational power than a Raspberry Pi."""
    model = None                                    # Detection Model: Set in Init
    function_args = None                        # Argument Dictionary passed to detector_function
        
    def __init__(self, modelFile, configFile):
        try:
            DNN="TF"
            if DNN == "CAFFE":
                #modelFile = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
                #configFile = "deploy.prototxt"
                self.model = cv2.dnn.readNetFromCaffe(configFile, modelFile)
            else:
                #modelFile = "opencv_face_detector_uint8.pb"
                #configFile = "opencv_face_detector.pbtxt"
                self.model = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
                
            if self.model == None:
                raise ValueError
        except ValueError:
            print("Could not load openCV DNN model!\n")
    
    # Wrapper for the different detection methods
    def detect(self, image): 
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)
 
        self.model.setInput(blob)
        detections = self.model.forward()
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
    
        return chooseFace(faces)


class FaceDetector_DNN_DLIB:
    """FaceDetector class, which wraps DLIBs CNN face detector.
        This Detector has state-of-the-art accuracy and is very fast on cuda enabled GPUs.
    """
    model = None                                                                    # Detection Model: Set in Init
    function_args = { "number_of_times_to_upsample" : 1}   # Argument Dictionary passed to detector_function
        
    def __init__(self, model_location):
        try: 
            self.model = dlib.cnn_face_detection_model_v1(model_location)
            
            if self.model == None:
                raise ValueError
        except ValueError:
            print("Could not load dlib cnn model!\n")
    
    # Wrapper for the different detection methods
    def detect(self, image): 
        faces =  self.model(img, **self.function_args)
        return chooseFace_dlib(faces)
 

##### Face Recognition ##############################################
class FaceRecognizer_CLASSIC:
    model = None
    function_args = None
    face_descriptors = None
    list_of_names = None
    recognitionAlgorithm = 1
    def __init__(self, trainingFile, recognitionAlgorithm, threshold):
        #Choose from the classic Recognizer algorithms
        if recognitionAlgorithm == 1:
            self.model = cv2.createLBPHFaceRecognizer(threshold=threshold)
        elif recognitionAlgorithm == 2:
            self.model = cv2.createFisherFaceRecognizer(threshold=threshold)
        else:
            self.model = cv2.createEigenFaceRecognizer(threshold=threshold)
        #Load Training file
        self.model.load(trainingFile)        
        
    def predict(self, face):
        
        # Crop image on face. If algorithm is not LBPH also resize because in all other algorithms image resolution has to be the same as training image resolution.
        #TODO: Move for appropriate algo into class
        if self.recognitionAlgorithm == 1:
            crop = face.crop(image, x, y, w, h)
        else:
            crop = face.resize(face.crop(image, x, y, w, h))
        
class FaceRecognizer_DLIB:
    """Face Recognition class, which wraps Dlib's face recognizer."""
    model = None
    #function_args = None
    face_descriptors = None
    alignFace = True
    tolerance = 0.6
    
    def __init__(self, model_location, descriptor_location = None):
        self.model = dlib.face_recognition_model_v1(model_location)
        # Load the descriptors for all known faces
        if descriptor_location != None:
            self.loadDescriptors(descriptor_location)
    
    def loadDescriptors(fileName):
        # load data from pkl file
        with open(fileName, "rb") as dataFile:
            self.face_descriptors = pickle.load(dataFile)
   
    def faceEncoding(self, face):
        if alignFace == False:
            return self.model.compute_face_descriptor(img, shape)
        else:
            face_chip = dlib.get_face_chip(img, shape)        
            return self.model.compute_face_descriptor(face_chip)    
        
    def predict(self, face):
        face_descriptor_in = self.faceEncoding(face)
            
        #Compare the obtained face descriptor to the list of descriptors and return the minimum
        distances = np.linalg.norm(self.face_descriptors - face_descriptor_in, axis=1)
        if (np.min(distances) < self.tolerance):
                return np.argmin(distances)
        else:
            return "Unknown"

#TODO: Immplement this. Either use some predifined recognizer like openFace via openCV or write this such that, some custom model can be used
class FaceRecognizer_DNN:
    """Face Recognition class, which wraps the OpenFace Dnn from OpenCV"""
    model = None
    function_args = None
    face_descriptors = None
    list_of_names = None
    alignFace = True
    tolerance = 0.6
    
    def __init__(self):
        #TODO: Immplement this
        print("implement this")
        
    def predict(self,):
        return "Unknown"

##### Utility functions #####

def chooseFace_dlib(faces):
    if len(faces) == 1:
        return faces[0]
    elif len(faces) == 0:
        return None
    else:   # Return the face with highest confidence
       # return rect_ocv2dlib(max(faces, lambda f: f.confidence))
        return max(faces, lambda f: f.confidence)

def chooseFace(faces):
    if len(faces) == 1:
        return faces[0]
    elif len(faces) == 0:
        return None
    else:   # Return the largest face if several faces are detected
        return max(faces, lambda f: (f.height * f.width))

def rect_ocv2dlib(dlib_rect):
    rect = cv2.rect()
    rect.x = dlib_rect.left()
    rect.y = dlib_rect.top()
    rect.width = dlib_rect.left() - dlib_rect.right()
    rect.height = dlib_rect.top() - dlib_rect.bottom()
    return rect


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

def drawFaceLocation(image, detection, text = None, scaleFactor = 1):
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top = detection.top() * scaleFactor
    right = detection.right() * scaleFactor
    bottom = detection.bottom() * scaleFactor
    left = detection.left() * scaleFactor
    
    #TODO: Beautify location makrer. Maybe rounded corners etc
    # Draw a box around the face
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

    if text != None:
        # Draw a label with a name below the face
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, text, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


