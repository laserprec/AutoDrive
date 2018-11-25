from time import sleep
from picamera import PiCamera
from math import ceil
import numpy as np

# PI Camera round up resolution factor 
H_RES_ROUND_UP_FACTOR = 32
V_RES_ROUND_UP_FACTOR = 16

class Camera:
    """ Provide methods to access the visual input from the picamera"""
    def __init__(self, resolution=(320,240)):
        """ Initialize the Pi Camera API
        
        Keyword Arguments:
            resolution {tuple} -- desired image resolution (default: {(320,240)})
        """

        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.img_buffer = self.createImageBuffer(resolution)

        # Warmup the camera
        print("Warming up the camera - 2 second")
        self.camera.start_preview()
        sleep(2) # minimum warm-up time

    def createImageBuffer(self, resolution):
        """ Creates an np.array buffer with specified size for storing the captured image.
           
            NOTE: When outputting to unencoded formats (i.e. np.array), 
                  the camera rounds the requested resolution. 
                  The horizontal resolution is rounded up to the 
                  nearest multiple of 32 pixels, while 
                  the vertical resolution is rounded up to the 
                  nearest multiple of 16 pixels. 
                  
                  For example, if the requested resolution is 100x100,
                  the capture will actually contain 128x112 pixels worth 
                  of data, but pixels beyond 100x100 will be uninitialized.
 
        Arguments:
            resolution {tuple} -- desired pixel resolution of the image
        """
        h_resolution, v_resolution = resolution
        # Find out the minimum multiple of 32 greater than horizontal resolution
        h_multiple = ceil(h_resolution / H_RES_ROUND_UP_FACTOR)
        # Find out the minimum multiple of 16 greater than vertical resolution
        v_multiple = ceil(v_resolution / V_RES_ROUND_UP_FACTOR)
        buffer_size = (v_multiple * V_RES_ROUND_UP_FACTOR,
                        h_multiple * H_RES_ROUND_UP_FACTOR,
                        3)
        return np.empty(buffer_size, dtype=np.uint8)

    def captureImg(self, format='rgb'):
        """ Capture a image from the camera into 'self.img_buffer`
        
        Keyword Arguments:
            format {str} -- format of the captured image (default: {'rbg'})
        """
        self.camera.capture(self.img_buffer, format=format)