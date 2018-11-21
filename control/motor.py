import pigpio
from time import sleep

MAX_PULSE_WIDTH = 1200
MIN_PULSE_WDITH = 1469

class Motor:
    """ Control the longitudinal (forward) motion of the car"""
    def __init__(self, pin, initPulseWidth=1450):
        self.raspberrypi = pigpio.pi()
        self.pin = pin
        self.pulseWidth = initPulseWidth
        # self.calibrate() # Uncomment it when motor doesn't respond
    
    def calibrate(self):
        """ Calibrate the motor before motion"""
        self.raspberrypi.set_servo_pulsewidth(self.pin, 2000)
        sleep(2)
        self.raspberrypi.set_servo_pulsewidth(self.pin, 1000)
        sleep(2)

    def moveForward(self):
        """ Move forward """
        self.raspberrypi.set_servo_pulsewidth(self.pin, self.pulseWidth)

    def stop(self):
        """ Stop the car """
        self.raspberrypi.set_servo_pulsewidth(self.pin, 0)
