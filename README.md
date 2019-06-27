# MMM-Face-Recognition
This an extension for the [MagicMirror](https://github.com/MichMich/MagicMirror) and a fork of [MMM-Facial-Recognition](https://github.com/paviro/MMM-Facial-Recognition). Similar to the original work it provides module swapping according to the detected user.
Several things were added:
- More face detection algorithms:
    - Dlib's Frontal Face Detector: Pretty good accuracy and very fast on CPU (default)
    - OpenCv's DNN face detector: Highest accuracy (probably) and reasonable fast (even on CPU)
    - Dlib's CNN based Face detector: High accuracy (Use on Cuda enabled devices like Nvidia Jetson)
- More face recognition algorithms:
    - Most Notable Dlib's face Descriptor: Should work with only one example Image per user.
- Option to check for messages from [MMM-PIR-Sensor](https://github.com/paviro/MMM-PIR-Sensor): Stop searching for faces if there is nobody around.
- Incorporates the [Motion Detection module](https://github.com/dmcinnes/MMM-Motion-Detection), which is also a fork of [MMM-Facial-Recognition](https://github.com/paviro/MMM-Facial-Recognition)


## Usage
To train the needed model use the [MMM-Facial-Recognition](https://github.com/paviro/MMM-Facial-Recognition).

The entry in config.js can look like the following. (NOTE: You only have to add the variables to config if want to change its standard value.)

```
{
	module: 'MMM-Facial-Recognition',
	config: {
		// 1=LBPH | 2=Fisher | 3=Eigen
		recognitionAlgorithm: 1,
		// Threshold for the confidence of a recognized face before it's considered a
		// positive match.  Confidence values below this threshold will be considered
		// a positive match because the lower the confidence value, or distance, the
		// more confident the algorithm is that the face was correctly detected.
		lbphThreshold: 50,
		fisherThreshold: 250,
		eigenThreshold: 3000,
		// force the use of a usb webcam on raspberry pi (on other platforms this is always true automatically)
		useUSBCam: false,
		// Path to your training xml
		trainingFile: 'modules/MMM-Facial-Recognition/training.xml',
		// recognition intervall in seconds (smaller number = faster but CPU intens!)
		interval: 2,
		// Logout delay after last recognition so that a user does not get instantly logged out if he turns away from the mirror for a few seconds
		logoutDelay: 15,
		// Array with usernames (copy and paste from training script)
		users: [],
		//Module set used for strangers and if no user is detected
		defaultClass: "default",
		//Set of modules which should be shown for every user
		everyoneClass: "everyone",
		// Boolean to toggle welcomeMessage
		welcomeMessage: true
	}
}
```

In order for this module to do anything useful you have to assign custom classes to your modules. The class `default` (if you don't change it) is shown if no user is detected or a stranger. The class `everyone` (if you don't change it) is shown for all users. To specify modules for a certain user, use their name as classname.

```
{
	module: 'example_module',
	position: 'top_left',
	//Set your classes here seperated by a space.
	//Shown for all users
	classes: 'default everyone'
},
{
	module: 'example_module2',
	position: 'top_left',
	//Only shown for me
	classes: 'Paul-Vincent'
}
```

## Dependencies
- [python-shell](https://www.npmjs.com/package/python-shell) (installed via `npm install`)
- [OpenCV](http://opencv.org) (`sudo apt-get install libopencv-dev python-opencv`)
- [Dlib]()

## Optimization



