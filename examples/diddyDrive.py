#!/usr/bin/env python
# coding: Latin-1

# Import library functions we need
import ThunderBorg
import time
import sys
import time
#import evdev
from evdev import InputDevice, categorize, ecodes




# Setup the ThunderBorg
TB = ThunderBorg.ThunderBorg()     # Create a new ThunderBorg object
#TB.i2cAddress = 0x15              # Uncomment and change the value if you have changed the board address
TB.Init()                          # Set the board up (checks the board is connected)


#creates object 'gamepad' to store the data
#you can call it whatever you like
wait = True
while wait:
	try:
		gamepad = InputDevice('/dev/input/event5')
		wait = False
	except:
		print ("Waiting for wii remote to connect...")
		time.sleep(5)
		

#prints out device info at start
print(gamepad)

# Wii keys

up = 103
down = 108
left = 105
right = 106
stop = 304


   
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == up:
                TB.MotorsOff()  
                TB.SetMotors(0.5) 
            elif event.code == down:
                TB.MotorsOff()  
                TB.SetMotors(-0.5)
            elif event.code == left:
                TB.MotorsOff()  
                TB.SetMotor1(-0.5)
                TB.SetMotor2(0.5)
            elif event.code == right:
                TB.MotorsOff()  
                TB.SetMotor1(0.5)
                TB.SetMotor2(-0.5)
            elif event.code == stop:
				TB.MotorsOff()


