import dlib


class FaceRecognizer_DLIB:
    """Face Recognition class, which wraps Dlib's face recognizer."""

    _model = None
    _shape_predictor = None
    _tolerance = 0.6
    _useAlign = True

    face_descriptors = None  # Dictionary of all known face encodings

    def __init__(
        self,
        model_location,
        shape_predictor_location,
        descriptor_location=None,
        useAlign=False,
    ):
        self._useAlign = useAlign
        try:
            self._model = dlib.face_recognition_model_v1(model_location)
            self._shape_predictor = dlib.shape_predictor(
                shape_predictor_location
            )

            if self._model == None or self._shape_predictor == None:
                raise ValueError
        except ValueError:
            print("Could not load dlib recognizer models!\n")

        # Load the descriptors for all known faces
        if descriptor_location != None:
            self.loadDescriptors(descriptor_location)

    def loadDescriptors(self, fileName):
        # load data from pkl file
        with open(fileName, "rb") as dataFile:
            self.face_descriptors = pickle.load(dataFile)

    def faceEncoding(self, image, face):
        shape = self._shape_predictor(image, face)

        if self._useAlign:
            face_chip = dlib.get_face_chip(image, shape)
            return self._model.compute_face_descriptor(face_chip)
        else:
            return self._model.compute_face_descriptor(image, shape)

    def predict(self, image, face):
        face_descriptor_in = self.faceEncoding(image, face)

        # Compare the obtained face descriptor to the list of descriptors and return the minimum
        min_distance = sys.float_info.max
        current_user = "Unknown"
        for name in self.face_descriptors.keys():
            distance = np.linalg.norm(
                np.subtract(self.face_descriptors[name], face_descriptor_in)
            )
            if distance < min_distance:
                min_distance = distance
                current_user = name

            if min_distance < self._tolerance:
                return current_user
            else:
                return "Unknown"


# TODO: Immplement this. Either use some predifined recognizer
# like openFace via openCV or write this such that, some custom model can be used
class FaceRecognizer_DNN:
    """Face Recognition class, which wraps the OpenFace Dnn from OpenCV"""

    _model = None
    _function_args = None
    _tolerance = 0.6
    face_descriptors = None

    def __init__(self):
        # TODO: Implement this
        print("implement this")

    def predict(self):
        return "Unknown"
