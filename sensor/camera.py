from time import sleep
from io import BytesIO
from picamera import PiCamera
from PIL import Image
from numpy import asarray

class Camera:
    """ Provide methods to access the visual input from the picamera"""
    def __init__(self):
        self.camera = PiCamera()
        self.imgstream = BytesIO()

        # Warmup the camera
        print("Warming up the camera - 2 second")
        self.camera.start_preview()
        sleep(2) # minimum warm-up time

    def captureImg(self, format='jpeg'):
        """ Capture a image from the camera
        
        Keyword Arguments:
            format {str} -- format of the captured image (default: {'jpeg'})
        
        Returns:
            [np.array] -- 2D array of the captured image
        """

        self.camera.capture(self.imgstream, format=format)
        self.imgstream.seek(0)
        return asarray(Image.open(self.imgstream))