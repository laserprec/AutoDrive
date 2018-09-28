# AutoDrive: Building a self-driving toy car

![hardware](./img/hardware.jpg)

## Materials:
1. Toy Car (Tamiya TT02)
1. Raspberry Pi 3b
1. Raspberry Pi Camera
1. HC-SR05 Ultrasonic Sensor
1. Power Bank
1. Breadboard
1. Wires

## Hardwire Specs:

1. **540j Motor (Comes with Tamiya TT02)**
*Motor Output Voltage*: 6.03V
*Motor Pulse Width Range:* 1200-1469 ms

1. **Tactic TSX40 High-Torque Servo**
*Input Voltage:* 4.8/6.0V
*Output Torque (@ 60 degree):* 0.16/0.13 sec
*Servo Pulse Width Range:* 1150 - 1850 (1500 is Neutral)

## Circuit Schematics
### Raspberry Pi GPIO Pin

![gpio](./img/pi_gpio.png)

- MOTOR_PIN = 13
- SERVO_PIN = 19

## Components of an Self-driving Car
1. Perception (Computer Vision, ML)
2. Sensor Fusion (LIDAR, Kalman, Particle Filters, and Mapping)
3. Motion Planning and Decision Making (Incremental Search Alg (D*), Sampling Planninng Alg, Planning w/ uncertainty)
4. Control
5. System Integration

## Ongoing List of Problems Encountered and (Working) Solutions:

### Inital Setup
1. Troublesome Remote Access (SSH) to Raspberry Pi due to dynamic IP

        Create a .local domain name via mDNS and/or configure static IP through configuring DHCP request (See ITEM #1-2 in List of Resources)    

2. Stream video from Raspberry Cam

        Host webserver or open socket from VLC (See ITEM #3-4)

3. Controlling RC Car with Raspberry Pi

        Connect Raspberry Pi's GPIO with the motor and servo of the RC car according to the hardwire schematics

4. Develop Software-Hardware Interface

        Build principle software foundation by mapping the tolerable pulse-width range of the hardware to measurable actions on the hardware. For example, turning the servo 15 degree left or run the motor on 50% power.

## List of Resources and Solution References:
1. [Setup mDNS for assigning .local domain to Raspberry Pi](https://www.howtogeek.com/167190/how-and-why-to-assign-the-.local-domain-to-your-raspberry-pi/)
1. [Setup static IP through DHCP](https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address/74428#74428)
1. [Setup video streaming in various methods](https://raspberrypi.stackexchange.com/questions/27082/how-to-stream-raspivid-to-linux-and-osx-using-gstreamer-vlc-or-netcat)
1. [Compile FFmpeg in Raspberry Pi to stream video over web server](https://johnvoysey.wordpress.com/2014/05/07/raspberry-pi-camera-live-streaming/)
1. [Raspberry Pi Controlled ESC and Motor](https://www.youtube.com/watch?v=br_Xv9X7YZc)
1. [PWM Frequency for Controlling Servo Rotation Angle](https://electronics.stackexchange.com/questions/129961/how-to-get-the-pwm-frequency-and-duration-of-each-pulse)