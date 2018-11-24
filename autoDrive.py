from time import time

from control.motor import Motor
from control.servo import Servo
from sensor.camera import Camera
from e2e.model import loadTrainedModel, preprocess

MOTOR_PIN = 13
SERVO_PIN = 19
TRAINED_WEIGHTS = ""

# Initialize global variables
camera, model, motor, servo = None, None, None, None
def setup():
    """ Setup global variables"""
    camera = Camera()
    servo = Servo(SERVO_PIN)
    motor = Motor(MOTOR_PIN)
    model = loadTrainedModel(TRAINED_WEIGHTS)

def run():
    setup()
    # Keep the car moving forward
    motor.moveForward()
    while True:
        # Record execution time
        start_time = time()
        img = camera.captureImg()
        img = preprocess(img)
        # Record end-to-end neural network execution time
        e2e_start = time()
        # Run the end-to-end model to get steering commands
        steering = model.predict(img[None, :, :, :], batch_size=1)
        print("Time to execute e2e CNN:    {:1.4f} sec".format(time() - e2e_start))
        # Validate that the steering angle is in acceptable range
        steering = servo.validate(steering, unit='radian')
        servo.turn(float(steering))
        print("Time to execute full cycle: {:1.4f} sec".format(time() - start_time))
        print("Steering Command:           {:1.4f} radian ".format(steering))
if __name__ == "__main__":
    run()
    