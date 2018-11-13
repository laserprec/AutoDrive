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
        self.steer_angle = 0

    def left(self):
        """ Turn servo left"""
        self.raspberrypi.set_servo_pulsewidth(self.pin, MAX_LEFT_PULSE)
        self.steer_angle = MAX_LEFT_ANGLE

    def right(self):
        """ Turn servo right"""
        self.raspberrypi.set_servo_pulsewidth(self.pin, MAX_RIGHT_PULSE)
        self.steer_angle = MAX_RIGHT_ANGLE

    def neutral(self):
        """ Reset servo to neutral position"""
        self.raspberrypi.set_servo_pulsewidth(self.pin, NEUTRAL_PULSE)
        self.steer_angle = 0

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
            # Restraint the pulse width within the safety range [1200, 1800]
            pulse_width = max(MAX_LEFT_PULSE, pulse_width)
        else:
            # Calculate the desire PWM to induce the steering angle
            pulse_width = POS_ANGLE_TO_PWM(steer_angle)
            # Restraint the pulse width within the safety range [1200, 1800]
            pulse_width = pulse_width = min(MAX_RIGHT_PULSE, pulse_width)

        self.raspberrypi.set_servo_pulsewidth(self.pin, pulse_width)
        self.steer_angle = steer_angle