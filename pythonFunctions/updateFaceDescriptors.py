#TODO: Add time measurements

###############################################################################
## This script is meant to generate the face encodings for all your          ##
## training images in $(PROJECT_DIRECTORY)/models/training_images.           ##
## Create a directory in there, with the name of the user and put the        ##
## corresponding images in it. The nameing of the files is not important.    ##
## After that, just run this script. It's also possible with this script to  ##
## take same additional photos before generating the encodings               ##
###############################################################################

import face
#import config

import pathlib
import os
import cv2
import pickle
import time
import numpy as np

def webcamSaveImages(name, path, detector):
    cap = cv2.VideoCapture("../../../Test_video_gesichterkennung.mp4") # 0 -> Standard Camera Device
    if not cap.isOpened():
        print ("Couldn't load video stream. Terminating...\n")
        exit()
        
    count = 0
    process_this_frame = True
    while(cap.isOpened()):
        # Grab a single frame of video
        success, frame = cap.read()
        if not success:
            continue
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[..., ::-1]
        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        detection = detector.detect(rgb_small_frame)

        process_this_frame = not process_this_frame
        
        drawFaceLocation(frame, detection, name, scaleFactor = 4)
        # Display the resulting image
        cv2.imshow('Webcam', frame)

        # Hit 'q' on the keyboard to quit!
        key = cv2.waitKey(1)
        if  key & 0xFF == ord(' '):
            # Save frame as training image
            file_name = name +"_VideoCapture_%" % count
            print("Saving frame as " + file_name + "\n")
            cv2.imwrite(path + file_name, frame)
            count +=1
        elif  key & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    cap.release()
    cv2.destroyAllWindows()
    print(count + " images were saved from Webcam for user" + name + "\n")

############################################################################

###############################
###### Begin of Skript   ######
###############################

##### Initialize  Face Recognition and Settings ######

#Initialize the config handler
#config =  config.ConfigHanlder() TODO: Add json path: MM specific?

# Init face detection and recognition
# TODO: For know just use defaults, later on we should use the requested method from config 
# TODO: Maybe provide fallback if config cant be used.
face_detector = face.FaceDetector_HOG()
face_recognizer = face.FaceRecognizer_DLIB("../models/dlib_face_recognition_resnet_model_v1.dat", "../models/shape_predictor_5_face_landmarks.dat")

# Get right directory
image_dir = "../models/trainingImages" #config.get("image_dir")
encodingsFile = "../models/face_encodings.pkl"

print("\n####################################################################")
print("Welcome to the training script for MMM-Faces.")
print("This tool is used to generate the face encodings for the dlib face recognition algorithm.")
print("It's not meant to train the classic openCV algorithms.")
print("####################################################################\n")

if not os.path.isdir(image_dir):
    print("The training directory doesn't exist. Do you want to specify an alternative directory?    [y/n]")
    answer = input("--> ")
    if (answer == "y" or answer == "Y"):
        image_dir = input("Enter alternative directory --> ")
        if not os.path.isdir(image_dir):
            print("This directory doesn't exist either. Terminating....\n")
            exit()
    else:
        exit()
    

print("Do you want to take additional images with your webcam, before generating the encodings?    [y/n]")
takeImages = input("--> ")

if (takeImages == 'y' or takeImages == "Y"):
    print("\nEnter the name of the user? ")
    currentUser = input("--> ")
    print("Images will be saved for User " + currentUser + "\n")
    currentUser_dir = image_dir + "/" + currentUser
    pathlib.Path(currentUser_dir).mkdir(exist_ok=True) #Make directory for user
    webcamSaveImages(currentUser, currentUser_dir, face_detector)
    
#####################################################################
print("Generating Encodings of saved images...\n")

##### Init benchmark variables #####
start_time = 0
detection_time = 0
detection_counter = 0
encoding_time = 0
encoding_counter = 0
recognition_time = 0
recognition_counter = 0
####################################

encodings = {} # Dictionary with user names as keys  
face_encoding = np.zeros([128])
#TODO: Do something different when more than one image is given 

# For each directory in there create a user in user_list 
user_list = [user_dir[1] for user_dir in os.walk(image_dir)][0] # user_dir[1]: first subfolder layer, [.....][0] of main dir

for user in user_list:
    #Load list of images in there
    user_dir = image_dir + "/" + user
    imageFiles = [imageFile for imageFile in os.listdir(user_dir)]
    images = [cv2.imread(user_dir + "/" + img) for img in imageFiles]
    
    print("Processing images for User " + user + "...")
    if len(images) == 0:
        print("Skipping User " + user + ": No images found")
        #user_list.remove(user)
        continue
    elif len(images) == 1:
        print("One image found")
        start_time = time.time()
        face = face_detector.detect(images[0])
        detection_time += time.time() - start_time
        detection_counter += 1
        
        start_time = time.time()
        face_encoding = face_recognizer.faceEncoding(images[0], face)
        encoding_time += time.time() - start_time
        encoding_counter += 1
    else:
        print("Several images found")
        for img in images:
            start_time = time.time()
            face = face_detector.detect(img)
            detection_time += time.time() - start_time
            detection_counter += 1
        
            start_time = time.time()
            face_encoding = face_recognizer.faceEncoding(img, face)
            encoding_time += time.time() - start_time
            encoding_counter += 1
    
    # Save value pair: user_name - face_encoding in $(PROJECT_DIRECTORY)/models/face_encodings.dat
    encodings.update({user : face_encoding})

print("Done!\n")
#####################################################################

#Do some checks
face_recognizer.face_descriptors = encodings
nFailures = 0
print("Do you want to perform some tests, if everything worked?    [y/n]")
performTests = input("--> ")
if (performTests != "y" and performTests != "Y"):
    print("Skipping tests!")
elif (takeImages == "y" or takeImages == "Y"):
    print("Do a check with current user: ...\n")
    cap = cv2.VideoCapture("../../../Test_video_gesichterkennung.mp4") # 0 -> Standard Camera Device
    while(cap.isOpened()):
        # Grab a single frame of video
        success, frame = cap.read()
        if not success:
            continue
        #TODO: Compare downsize to normal. Decide if we should downsample in facerecognition.py
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[..., ::-1]
        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        start_time = time.time()
        detection = face_detector.detect(rgb_small_frame)
        detection_time += time.time() - start_time
        detection_counter += 1
        
        start_time = time.time()
        predictedUser = face_recognizer.predict(face)
        recognition_time += time.time() - start_time
        recognition_counter += 1
        
        if (predictedUser != currentUser):
            nFailures += 1
            message = "Failure: " + predictedUser
        else:
            message = "Success: " + currentUser
            
        drawFaceLocation(frame, detection, message, scaleFactor = 4)
        
        # Display the resulting image
        cv2.imshow('Webcam', frame)

        # Hit 'q' on the keyboard to quit!
        key = cv2.waitKey(1)
        if  key & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    cap.release()
    cv2.destroyAllWindows()
    if (nFailures == 0):
        print("Check succesful!")
    else:
        print("Check failed. That's pretty bad")

else:
    print("Do a little sanity check: Recognize training images again...")
    for user in user_list:
        #Load list of images in there
        user_dir = image_dir + "/" + user
        imageFiles = [file for file in os.listdir(user_dir)]
        images = [cv2.imread(user_dir + "/" *img) for img in imageFiles]
        
        for img in images:
            start_time = time.time()
            face = face_detector.detect(img)
            detection_time += time.time() - start_time
            detection_counter += 1
            
            start_time = time.time()
            predictedUser = face_recognizer.predict(face)
            recognition_time += time.time() - start_time
            recognition_counter += 1
            
            if (predictedUser != user):
                nFailures += 1
                print("Mismatch when recognizing " + user + ". Prediction was " + predictedUser + "!!!")
    
    if (nFailures == 0):
        print("Check succesful!")
    else:
        print("Check failed. That's pretty bad")
        
#####################################################################        

print("Saving results to " + encodingsFile)
with open(encodingsFile, 'wb') as dataFile:
    # Save Dictionary with pickle.
    pickle.dump(encodings, dataFile)

print("####################################################################\n")
#Benchmarking results
if (detection_counter != 0):
    detection_time = detection_time / detection_counter
if (encoding_counter != 0):
    encoding_time = encoding_time / encoding_counter
if (recognition_counter != 0):
    recognition_time = recognition_time / recognition_counter

print("Timing results: ")
print("     Average time for detection: " + detection_time + "(" + detection_counter + " detections)")
print("     Average time for generating encodings: " + encoding_time + "(" + encoding_counter + " encodings)")
print("     Average time for recognition: " + recognition_time + "(" + recognition_counter + " recognized faces)")
print("####################################################################\n")

print("\nYou're now able to use the face recognition with following users: \n")
print(*user_list, sep = ", ")
print("\n")
