# Is Someone in front of the mirror
# Either read status messages from PIR sensor -> Notifcation User Message
# Or from Motion Detector Camera Module -> > Notifcation Motion_detected

class MotionDetector_Simple:
    treshold = None
    frame_minus = None
    frame = None
    frame_plus

    def __init__(self, threshold, camera):
        self.threshold = threshold
        self.frame = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)
        self.frame_plus = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

    def checkMotion(camera)
        self.frame_minus = self.frame
        self.frame       = self.frame_plus
        self.frame_plus  = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

        diff = diffImg(t_minus, t, t_plus)

        if max > config.get("detectionThreshold"):
            if last_motion is None:
                to_node("motion-detected", {})
            last_motion = time.time()
        elif last_motion != None and time.time() - last_motion > config.get("motionStopDelay"):
            last_motion = None
            to_node("motion-stopped", {})

class MotionDetector_ContourArea:
    treshold = None
    frame_minus = None
    frame = None
    frame_plus = None
    diff = None
    thresh = None

    def __init__(self, threshold, camera):
        self.threshold = threshold
        self.frame = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)
        self.frame_plus = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

    def checkMotion(camera)
        self.frame_minus = self.frame
        self.frame       = self.frame_plus
        self.frame_plus  = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

        self.diff = diffImg(t_minus, t, t_plus)
        self.thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        self.thresh = cv2.dilate(self.thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        # loop over the contours
        for c in cnts:
            area = cv2.contourArea(c)
            if area > max_area:
                max_area = area

        if max_area > config.get("detectionThreshold"):
            if last_motion is None:
                to_node("motion-detected", {})
            last_motion = time.time()
        elif last_motion != None and time.time() - last_motion > config.get("motionStopDelay"):
            last_motion = None
            to_node("motion-stopped", {})

class MotionDetector_PIR:
    """ This class is meant to be used with some PIR module and only listens to the message emited from the corresponding module"""
    config = None
    
    def __init__(self, config):
        #set config handler
        self.config = config
            

    def checkMotion(camera):
        #liste to messages from config

