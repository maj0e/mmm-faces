# Is Someone in front of the mirror
# Either read status messages from PIR sensor -> Notifcation User Message
# Or from Motion Detector Camera Module -> > Notifcation Motion_detected
def motion(camera)
    t_minus = t
    t       = t_plus
    t_plus  = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

    diff = diffImg(t_minus, t, t_plus)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    max = 0
    # loop over the contours
    for c in cnts:
        area = cv2.contourArea(c)
        if area > max:
            max = area

    if max > config.get("detectionThreshold"):
        if last_motion is None:
            to_node("motion-detected", {})
        last_motion = time.time()
    elif last_motion != None and time.time() - last_motion > config.get("motionStopDelay"):
        last_motion = None
to_node("motion-stopped", {})


