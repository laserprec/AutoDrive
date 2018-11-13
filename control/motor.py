import pigpio
from time import sleep

MAX_PULSE_WIDTH = 1200
MIN_PULSE_WDITH = 1469


class Motor:
    """ Control the longitudinal (forward) motion of the car"""
    def __init__(self, pin, pulseWidth=1450):
        self.raspberrypi = pigpio.pi()
        self.pin = pin
        self.pulseWidth = pulseWidth
        self.calibrate()
    
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



# class Motor:
#     def __init__(self, default_speed):
#         self.default_speed = default_speed
#         self.isReversed = False
#         self.speed = 0
#         self.max_speed = 100
#         self.min_speed = 0
        

#     def forward_cont(self):
#         self.isReversed = False
#         if self.is_in_safe_range():
#             self.speed += 5

#     def backward_cont(self):
#         self.isReversed = True
#         if self.is_in_safe_range():
#             self.speed += -5

#     def forward(self):
#         self.isReversed = False
#         self.speed = self.default_speed

#     def backward(self):
#         self.isReversed = True
#         self.speed = self.default_speed

#     def is_in_safe_range(self):
#         return self.min_speed <= self.speed <= self.max_speed