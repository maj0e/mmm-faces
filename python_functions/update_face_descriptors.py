#####################################################################
## This script is meant to generate the face encodings for all your training images                                             ##
## in $(PROJECT_DIRECTORY)/models/training_images. Create a directory in there, with the name of the user   ##
## and put the corresponding images in it. The naming of the files is not important                                            ##
## After that, just run this script                                                                                                                            ##
## It's also possible with this script to take same additional photos before generating the encodings                 ##
#####################################################################

import face
#import config

import pathlib
import os
import cv2

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
        
    
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top = detection.top() * 4
        right = detection.right() * 4
        bottom = detection.bottom() * 4
        left = detection.left() * 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

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
###### Beginn of Skript  ######
###############################

# Init face detection and recognition
# TODO: For know just use defaults, later on we should use the requested method from config 
face_detector = face.FaceDetector_HOG()
face_recognizer = face.FaceRecognizer_DLIB("../models/dlib_face_recognition_resnet_model_v1.dat")
face_recognizer.alignFace = True

#Initialize the config handler
#config =  config.ConfigHanlder()

print("\n####################################################################")
print("Welcome to the training script for MMM-Faces.")
print("This tool is used to generate the face encodings for the dlib face recognition algorithm.")
print("It's not meant to train the classic openCV algorithms.")
print("####################################################################\n")

# Get right directory
training_dir = "../models/training_images" #TODO:config.get("SOMETHING_IF_HAVE TO FIGURE_OUT")
if not os.path.isdir(training_dir):
    print("The training directory doesn't exist. Do you want to specify an alternative directory?    [y/n]")
    answer = input("--> ")
    if (answer == "y" or answer == "Y"):
        training_dir = input("Enter alternative directory --> ")
    else:
        exit()
    if not os.path.isdir(training_dir):
        print("This directory doesn't exist either. Terminating....\n")
        exit()

print("Do you want to take additional images with your webcam, before generating the encodings?    [y/n]")
takeImages = input("--> ")

if (takeImages == 'y' or takeImages == "Y"):
    print("\nEnter the name of the user? ")
    newUser = input("--> ")
    print("Images will be saved for User " + newUser + "\n")
    newUser_dir = training_dir + "/" +newUser
    pathlib.Path(newUser_dir).mkdir(exist_ok=True) #Make directory for user
    webcamSaveImages(newUser, newUser_dir, face_detector)
    


print("Generating Encodings of saved images...\n")

# For each directory in there create a user in user_list 
user_list = [user_dir[0] for user_dir in os.walk(training_dir)]


##### Measure time for comparison#####
detection_time = 0
detection_counter = 0
recognition_time = 0
recognition_counter = 0

for user in user_list:
    #Load list of images in there
    if len(images == 0):
        #TODO: remove user from user_list
        print("Skipping User " + user + ": No Images found\n")
        continue
    #elif len(images) == 1:
        #TODO: compute just one face encoding
    #else:
        #TODO:

    print("Processing images for User" + user + "...\n")

    face_encoding = np.zero([128])
    for img in images:
        face = face_detector.detect(img)
        face_encoding = face_encodings + face
        
    # Mean of all encodings
    face_encoding = face_encoding / len(images)
    
    # Save value pair: user_name - face_encoding in $(PROJECT_DIRECTORY)/models/face_encodings.dat

print("Done!\n")
if (takeImages == "y" or takeImages == "Y"):
    print("Do a check with current user: ...\n")
else:
    print("Do a little sanity check: Recognize training images again...\n")
    ###

    if (nFailures == 0):
        print("Check succesful!\n")
    else:
        print("Check failed. That's pretty bad")

print("####################################################################\n")
#Benchmarking results
detection_time = detection_time / detection_counter
recognition_time = recognition_time / recognition_counter

if (recognition_counter < detection_counter):
    print("There were more faces detected than images given. Make sure to only use images with one person!\n")

print("Timing results: \n")
print("     Average time for detection: " + detection_time + "\n")
print("     Average time for recognition: " + recognition_time + "\n")

print("A total number of " + recognition_counter + " images were processed. \n")

print("You're now able to use the face recognition with following users: \n")
print(*user_list, sep = ", ")
print("\n")
print("####################################################################\n")
