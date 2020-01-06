# Is Someone in front of the mirror
# Either read status messages from PIR sensor -> Notifcation User Message
# Or from Motion Detector Camera Module -> > Notifcation Motion_detected
import numpy as np
from tf.lite import Interpreter

import cv2


# if max_area > config.get("detectionThreshold"):
#     if last_motion is None:
#         to_node("motion-detected", {})
#     last_motion = time.time()
# elif last_motion is not None and time.time() - last_motion > config.get(
#     "motionStopDelay"
# ):
#     last_motion = None
#     to_node("motion-stopped", {})


class MotionDetector_Simple:
    threshold = None
    frame_minus = None
    frame = None
    frame_plus = None

    def __init__(self, threshold, camera):
        self.threshold = threshold
        self.frame = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)
        self.frame_plus = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

    def detect(self, camera):
        self.frame_minus = self.frame
        self.frame = self.frame_plus
        self.frame_plus = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

        diffImg = diffImg(self.frame_minus, self.frame, self.frame_plus)

        return max > self.threshold


class MotionDetector_ContourArea:
    threshold = None
    frame_minus = None
    frame = None
    frame_plus = None
    threshImg = None

    def __init__(self, threshold, camera):
        self.threshold = threshold
        self.frame = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)
        self.frame_plus = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

    def detect(self, camera):
        self.frame_minus = self.frame
        self.frame = self.frame_plus
        self.frame_plus = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

        diffImg = diffImg(self.frame_minus, self.frame, self.frame_plus)
        self.threshImg = cv2.threshold(diffImg, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        self.threshImg = cv2.dilate(self.threshImg, None, iterations=2)
        (cnts, _) = cv2.findContours(
            self.threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        max_area = 0
        # loop over the contours
        for c in cnts:
            area = cv2.contourArea(c)
            if area > max_area:
                max_area = area

        return max_area > self.threshold


class PersonDetector:
    """ A Trigger class using a person detector model
    from the Visual Wake Words Challenge
    (Model from https://github.com/mit-han-lab/VWW) """

    model = None
    inputDetails = None
    outputDetails = None
    inputShape = None

    def __init__(self, model_path="../../model_quantized.tflite"):
        # Load TFLite model and allocate tensors.
        self.model = Interpreter(model_path)
        self.model.allocate_tensors()

        # Get input and output tensors.
        self.inputDetails = self.model.get_input_details()
        self.outputDetails = self.model.get_output_details()

        self.inputShape = self.inputDetails[0]["shape"]

    def detect(self, image):
        # Resize images to input dimension shape
        # image.resize((238, 208))
        image = image.resize(self.inputShape[0], self.inputShape[1])
        # needed? image should be some kind of numpy array
        # but python doc is sparse for opencv
        inputData = np.array(image)
        # TODO: Check if bgr <-> rgb format match!!!
        inputData = np.expand_dims(inputData, axis=0)

        # Call the interpreter to perform classification
        self.model.set_tensor(self.inputDetails[0]["index"], inputData)
        self.model.invoke()

        outputData = self.model.get_tensor(self.outputDetails[0]["index"])
        # Prob for Person Vs No Person
        return outputData[0][1] > outputData[0][0]
