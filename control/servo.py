from math import pi as PI
import pigpio

MAX_LEFT_ANGLE = 18.5   # In unit degree
MAX_RIGHT_ANGLE = -18.5 # In unit degree
MAX_LEFT_PULSE = 1200
MAX_RIGHT_PULSE = 1800
NEUTRAL_PULSE = 1500

# NOTE: To produce a desired steering angle, the linear relationship
#       between steering angle (in degree) and pulse width is defined as follow:
POS_ANGLE_TO_PWM = lambda x: 15.9 * x + 1561 # Right Turns
NEG_ANGLE_TO_PWM = lambda x: 17.9 * x + 1439 # Left Turns

class Servo:
    """ Control the transverse (left and right) motion of the car """
    def __init__(self, pin):
        self.raspberrypi = pigpio.pi()
        self.pin = pin

    def left(self):
        """ Turn servo left"""
        self.raspberrypi.set_servo_pulsewidth(self.pin, MAX_LEFT_PULSE)

    def right(self):
        """ Turn servo right"""
        self.raspberrypi.set_servo_pulsewidth(self.pin, MAX_RIGHT_PULSE)

    def neutral(self):
        """ Reset servo to neutral position"""
        self.raspberrypi.set_servo_pulsewidth(self.pin, NEUTRAL_PULSE)

    def turn(self, steer_angle, radian=True):
        """ Turn the servo to the desired steering angle (default in unit radian)
        Arguments:
            steer_angle {float} -- desired steering angle (negative angles are left turns)
        Keyword Arguments:
            radian {bool} -- True if steer_angle is in unit radian.
                             False if in unit degree (default: {True})
        """
        # If steering angle is in unit radian
        if radian:
            # Convert to unit degree
            steer_angle = steer_angle * 180 / PI
        # If left turn
        if steer_angle < 0:
            # Calculate the desire PWM to induce the steering angle
            pulse_width = NEG_ANGLE_TO_PWM(steer_angle)
        else:
            # Calculate the desire PWM to induce the steering angle
            pulse_width = POS_ANGLE_TO_PWM(steer_angle)

        self.raspberrypi.set_servo_pulsewidth(self.pin, pulse_width)



# class Steering ():
#     def __init__(self, config):
#         self.conf = config
#         self.angle = 0
#         self.max_angle = 45
#         self.min_angle = -45

#     def left_cont(self):
#         if self.is_in_safe_range():
#             self.angle += -5

#     def right_cont(self):
#         if self.is_in_safe_range():
#             self.angle += 5

#     def left(self):
#         self.angle = -45

#     def right(self):
#         self.angle = 45

#     def is_in_safe_range(self):
#         return self.min_angle <= self.angle <= self.max_angle