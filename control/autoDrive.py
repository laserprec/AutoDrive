import h5py
from io import BytesIO
from PIL import Image
from time import sleep
from picamera import PiCamera
from keras.models import load_model
from keras import __version__ as keras_version

from motor import Motor
from servo import Servo

MOTOR_PIN = 13
SERVO_PIN = 19
TRAINED_WEIGHTS = ""

# Initialize global variables
model, motor, servo = None, None, None
camera, imgstream = None, None

def setup():
    """ Setup global variables"""
    camera = PiCamera()
    imgstream = BytesIO()
    servo = Servo(SERVO_PIN)
    motor = Motor(MOTOR_PIN)
    model = loadTrainedModel(TRAINED_WEIGHTS)
    
    # Warmup the camera
    camera.start_preview()
    sleep(2) # warm-up time

def loadTrainedModel(filename):
    """ Load in pretrained model
    Arguments:
        filename {str} -- filepath of the .h5 file containing the trained weights
    Returns:
        [keras.model] -- trained model
    """
    # check that model Keras version is same as local Keras version
    f = h5py.File(filename, mode='r')
    model_version = f.attrs.get('keras_version')
    keras_version = str(keras_version).encode('utf8')

    if model_version != keras_version:
        print('You are using Keras version ', keras_version,
              ', but the model was built using ', model_version)
    return load_model(filename)

def captureImg():
    """ Capture a image from the camera
    Returns:
        [PIL Image object] -- represents the captured image
    """
    camera.capture(imgstream, format='jpeg')
    imgstream.seek(0)
    return Image.open(imgstream)

def run():
    setup()
    # Keep the car moving forward
    motor.moveForward()
    while True:
        img = captureImg()
        # Run the e2e model to get steering commands
        steering = model.predict(img)
        servo.turn(steering)

if __name__ == "__main__":
    run()
    