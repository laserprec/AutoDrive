from math import degrees, radians
import pigpio

MAX_LEFT_ANGLE = -18   # In unit degree
MAX_RIGHT_ANGLE = 18   # In unit degree
MAX_LEFT_RADIAN = radians(MAX_LEFT_ANGLE)   # In unit radian
MAX_RIGHT_RADIAN = radians(MAX_RIGHT_ANGLE) # In unit radian
MAX_LEFT_PULSE = 1200
MAX_RIGHT_PULSE = 1780
NEUTRAL_PULSE = 1500

# NOTE: To produce a desired steering angle, the linear relationship
#       between steering angle (in degree) and pulse width is defined as follow:
ANGLE_TO_PWM = lambda x: 17.9 * x + 1439 # Left Turns

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
            steer_angle = degrees(steer_angle)
        if steer_angle == 0:
            pulse_width = NEUTRAL_PULSE
        # If left turn
        elif steer_angle < 0:
            # Calculate the desire PWM to induce the steering angle
            pulse_width = ANGLE_TO_PWM(steer_angle)
            # Restraint the pulse width within the safety range [1200, 1780]
            pulse_width = max(MAX_LEFT_PULSE, pulse_width)
        else:
            # Calculate the desire PWM to induce the steering angle
            pulse_width = ANGLE_TO_PWM(steer_angle)
            # Restraint the pulse width within the safety range [1200, 1780]
            pulse_width = pulse_width = min(MAX_RIGHT_PULSE, pulse_width)

        self.raspberrypi.set_servo_pulsewidth(self.pin, pulse_width)
        self.steer_angle = steer_angle

    def validate(self, steer_angle, unit="radian"):
        if unit == 'radian':
            return self._validate_radian(steer_angle)
        elif unit == 'degree':
            return self._validate_degree(steer_angle)
        else:
            raise ValueError("Error: value units are either in 'radian' or 'degree'")

    def _validate_radian(self, steer_angle):
        if steer_angle < MAX_LEFT_RADIAN or steer_angle > MAX_RIGHT_RADIAN:
            print("Out of bound steering command: {}".format(steer_angle))
            if steer_angle < MAX_LEFT_RADIAN:
                steer_angle = MAX_LEFT_RADIAN
            else:
                steer_angle = MAX_RIGHT_RADIAN
        return steer_angle

    def _validate_degree(self, steer_angle):
        if steer_angle < MAX_LEFT_ANGLE or steer_angle > MAX_RIGHT_ANGLE:
            print("Out of bound steering command: {}".format(steer_angle))
            if steer_angle < MAX_LEFT_ANGLE:
                steer_angle = MAX_LEFT_ANGLE
            else:
                steer_angle = MAX_RIGHT_ANGLE
        return steer_angle