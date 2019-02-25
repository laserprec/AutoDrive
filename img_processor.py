import io
import threading
import picamera
import numpy as np
from time import time, sleep
from PIL import Image
from matplotlib import pyplot as plt
from control.motor import Motor
from control.servo import Servo
from e2e.model import loadTrainedModel, preprocess

# Create a pool of image processors
done = False
pool = []
lock = threading.Lock()
img = None

MOTOR_PIN = 13
SERVO_PIN = 19
TRAINED_WEIGHTS = "./e2e/model.h5"

""" Setup global variables"""
print("****** Setting up hardware API ******")
servo = Servo(SERVO_PIN)
motor = Motor(MOTOR_PIN)
model = loadTrainedModel(TRAINED_WEIGHTS)
# Hack to resolve keras bug when predicting after loading a pretrained model
model.predict(np.zeros((1,64,200,3)))

class ImageProcessor(threading.Thread):
    def __init__(self, duration=float("inf")):
        super(ImageProcessor, self).__init__()
        self.duration = duration
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        start_time = time()
        global done
        print("running")
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                print("About to try")
                try:
                    # Record time to retrieve each frame
                    cur_time = time()
                    self.stream.seek(0)
                    # Read the image and do some processing on it
                    img = np.asarray(Image.open(self.stream))
                    print("Time to retrieve a frame   {:1.4f} sec".format(time() - cur_time)) 
                    # Record time to preprocess img
                    preprocess_start = time()
                    img = preprocess(img)
                    print("Time to preprocess a frame {:1.4f} sec".format(time() - preprocess_start))
                    # Record time to process img
                    process_start = time()
                    # Record end-to-end neural network execution time
                    e2e_start = time()
                    # Run the end-to-end model to get steering commands
                    steering = float(model.predict(img[None, :, :, :], batch_size=1))
                    print("Time to execute e2e CNN:    {:1.4f} sec".format(time() - e2e_start))
                    # Validate that the steering angle is in acceptable range
                    steering = servo.validate(steering, unit='radian')
                    servo.turn(steering)
                    print("Time to execute full cycle: {:1.4f} sec".format(time() - cur_time))
                    print("Steering Command:           {:1.4f} radian ".format(steering))
                    # Set done to True if you want the script to terminate
                    if (cur_time - start_time) > self.duration:
                        done = True
                finally:
                    print("Resetting stream")
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            print("pool is starved, sleeping for 0.6 sec")
            sleep(0.6)

with picamera.PiCamera() as camera:
    pool = [ImageProcessor(duration=15) for i in range(5)]
    camera.resolution = (320, 240)
    camera.framerate = 14
    camera.start_preview()
    sleep(2)
    print("Begin to capture img")
    camera.capture_sequence(streams(), use_video_port=True)
    motor.moveForward()

# Shut down the processors in an orderly fashion
motor.stop()
servo.neutral()

while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
