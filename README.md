# AutoDrive: Building a self-driving toy car

## Materials:
1. Toy Car
2. Raspberry Pi 3b
3. Raspberry Pi Camera
4. HC-SR05 Ultrasonic Sensor
5. Breadboard
6. Wires

## Ongoing List of Problems Encountered and (Working) Solutions:

### Inital Setup
1. Troublesome Remote Access (SSH) to Raspberry Pi due to dynamic IP

        Create a .local domain name via mDNS and/or configure static IP through configuring DHCP request (See ITEM #1-2 in List of Resources)    

2. Stream video from Raspberry Cam

        Host webserver or open socket from VLC (See ITEM #3-4)

## List of Resources and Solution References:
1. [Setup mDNS for assigning .local domain to Raspberry Pi](https://www.howtogeek.com/167190/how-and-why-to-assign-the-.local-domain-to-your-raspberry-pi/)
2. [Setup static IP through DHCP](https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address/74428#74428)
3. [Setup video streaming in various methods](https://raspberrypi.stackexchange.com/questions/27082/how-to-stream-raspivid-to-linux-and-osx-using-gstreamer-vlc-or-netcat)
4. [Compile FFmpeg in Raspberry Pi to stream video over web server](https://johnvoysey.wordpress.com/2014/05/07/raspberry-pi-camera-live-streaming/)
