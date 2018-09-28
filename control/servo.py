import pigpio

LEFT_PULSE = 1150
RIGHT_PULSE = 1850
NEUTRAL_PULSE = 1500

class Servo:
    def __init__(self, pin):
        self.pi = pigpio.pi()
        self.pin = pin

    def left(self):
        self.pi.set_servo_pulsewidth(self.pin, LEFT_PULSE)

    def right(self):
        self.pi.set_servo_pulsewidth(self.pin, RIGHT_PULSE)

    def neutral(self):
        self.pi.set_servo_pulsewidth(self.pin, NEUTRAL_PULSE)

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