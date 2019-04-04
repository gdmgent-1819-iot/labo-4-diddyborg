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
green = 257
red = 258
police = 316


TB.SetLedShowBattery(False)
def setPolice(state):
	while state:
		for x in range(0, 30):
			TB.SetLeds(255, 0, 0)
			time.sleep(0.25)
			TB.SetLeds(0, 0, 255)
			time.sleep(0.25)
		state = False
		TB.SetLedShowBattery(True)
	
	
			
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == green:
				TB.SetLeds(0, 255, 0)
            elif event.code == red:
				TB.SetLeds(255, 0, 0)
            elif event.code == police:
				setPolice(True) 
				



