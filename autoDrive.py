from time import time

from control.motor import Motor
from control.servo import Servo
from sensor.camera import Camera
from e2e.model import loadTrainedModel, preprocess

MOTOR_PIN = 13
SERVO_PIN = 19
TRAINED_WEIGHTS = "./e2e/model.h5"

""" Setup global variables"""
print("****** Setting up hardware API ******")
camera = Camera()
servo = Servo(SERVO_PIN)
motor = Motor(MOTOR_PIN)
model = loadTrainedModel(TRAINED_WEIGHTS)

def run(max_iterations=float('inf')):
    # Keep the car moving forward
    motor.moveForward()
    i = 0
    while i < max_iterations:
        i += 1
        # Record execution time
        start_time = time()
        # Record time to capture image
        camera.captureImg()
        print("Time to capture img:        {:1.4f} sec".format(time() - start_time))
        # Record time to preprocess img
        preprocess_start = time()
        img = preprocess(camera.img_buffer)
        print("Time to preprocess img:     {:1.4f} sec".format(time() - preprocess_start))
        # Record end-to-end neural network execution time
        e2e_start = time()
        # Run the end-to-end model to get steering commands
        steering = float(model.predict(img[None, :, :, :], batch_size=1))
        print("Time to execute e2e CNN:    {:1.4f} sec".format(time() - e2e_start))
        # Validate that the steering angle is in acceptable range
        steering = servo.validate(steering, unit='radian')
        servo.turn(steering)
        print("Time to execute full cycle: {:1.4f} sec".format(time() - start_time))
        print("Steering Command:           {:1.4f} radian ".format(steering))
    motor.stop()

if __name__ == "__main__":
    run(max_iterations=50)
    
