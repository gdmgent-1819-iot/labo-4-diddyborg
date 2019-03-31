<<<<<<< HEAD
# Research rapport

## Controlling Diddyborg v2 with a Wiimote - Jeroen Vervaeck en Yoram Platteeuw

## Table of content

1. Intro

2. Diddyborg inisalising

3. Installing the ThunderBorg

4. Connecting Wii controller with Raspberry Pi

5. Mapping Wiimote input with python

6. Adressing Thunderborg

7. Starting program on boot

8. Sources

See assets/images/Diddyborg.JPG && assets/images/Wiimote1.JPG

### 1. Intro

The **Diddyborg v2** is a robot kit from PiBorg. It&#39;s a mount which is controlled by six motors. De power comes from AA batteries. It&#39;s possible to attach extra tools to the robot to make it more functional.

### 2. Diddyborg inisalising

**step 1**

Connect the Raspberry Pi from the Diddyborg to a screen (Or via SSH). Make sure the SD cart contains the newest version of Raspbian.

**Step 2**

Connect the batterie pack to the Thunderborg.

**Step 3**

Hdmi kabel aansluiten op een scherm

Connect the HDMI cable to a screen.

A Keyboard and mouse to control the RaspberryPi is also recommended.

### 3. Installing the ThunderBorg:

**DiddyBorg v2** uses a [**ThunderBorg**](https://www.piborg.org/thunderborg) to drive the motors. We will connect the board later, for now we simply need to install the software to control it. **DiddyBorg** requires **I2C** to be enabled. If you have not done this before you can do this by:

Enter the following command in a terminal: _sudo raspi-config_

Move down to option 5 Interfacing Options and press ENTER

Move down to **option P5 I2C** and press ENTER

Make sure  **Yes**  is highlighted and press ENTER

When the dialog says **I2C is enabled** press ENTER

Move right until  **Finish**  is highlighted, then press ENTER

---

To run through the automatic installer just use this one line in a terminal:

_bash \&lt;(curl_ [_https://www.piborg.org/installer/install-diddyborg-v2.txt_](https://www.piborg.org/installer/install-diddyborg-v2.txt)_)_

---

If you would prefer to manually run through the steps use the commands below:

_mkdir ~/thunderborg_

_cd ~/thunderborg_

_wget http://www.piborg.org/downloads/thunderborg/examples.zip_

_unzip examples.zip_

_chmod +x install.sh_

_./install.sh_

_mkdir ~/diddyborgv2_

_cd ~/diddyborgv2_

_wget http://www.piborg.org/downloads/diddyborgv2/examples.zip_

_unzip examples.zip_

_chmod +x install.sh_

_./install.sh_

Once you have done this you will have two sets of examples:

ThunderBorg examples in _~/thunderborg_ The basic motor output and LED control examples will have links on the desktop

DiddyBorg v2 examples in _~/diddyborgv2_ This includes some standard examples such as remote control using a gamepad or joystick

This step will download some filles to the RaspberryPi. They will be used later on.

## 4. Connecting Wii controller with Raspberry Pi

[https://www.instructables.com/id/Wiimote-Controller-Configuration-for-Raspberry-Pi-/](https://www.instructables.com/id/Wiimote-Controller-Configuration-for-Raspberry-Pi-/)

Update the existing software on your Raspberry Pi. We will be using the Linux Command line to perform all of the commands.

_sudo apt-get update_

_sudo apt-get upgrade_

---

The packages &quot;cwiid&quot; and &quot;wminput&quot; were created to interface the Wiimote and Raspberry Pi via bluetooth. The &quot;cwiid&quot; package is the Linux to Nintendo Wiimote interface. The &quot;wminput&quot; is a Linux event, mouse, and joystick driver for the wiimote using the uinput system.

_sudo apt-get install python-cwiid_

_sudo apt-get install wminput_

---

We need to change the udev rules so the uinput device will work with non-root users. We will do this by adding wiimote.rules to /etc/udev/rules.d.

_sudo nano /etc/udev/rules.d/wiimote.rules_

Copy and paste the following into the file. Then save this file.

_KERNEL==&quot;uinput&quot;, MODE=&quot;0666&quot;    _

---

In order to implement the changes that you made to the rules file, you must either reboot the Raspberry Pi or restart the udev service.

_sudo shutdown -r now_

---

We will be using the bluetooth to connect to the Wiimotes. Check the status by typing the following:

_/etc/init.d/bluetooth status_

See assets/images/bluethoothStatus.PNG

---

**Configuring Wiimote Buttons in Wminput.**

Each Wiimote will need its own controller mapping. My configuration file will have controller mappings for the Wiimote and Nunchuk Buttons.

Create the file with the following command:

_sudo nano /home/pi/mywinput_

Next, Copy and paste this into the file:

_#WiiMote_

_Wiimote.A  = BTN\_A_

_Wiimote.B = BTN\_B_

_Wiimote.Dpad.X = ABS\_Y_

_Wiimote.Dpad.Y = -ABS\_X_

_Wiimote.Minus = BTN\_SELECT_

_Wiimote.Plus = BTN\_START_

_Wiimote.Home = BTN\_MODE_

_Wiimote.1 = BTN\_X_

_Wiimote.2 = BTN\_Y_

_# Nunchuk_

_Nunchuk.C = BTN\_C_

_Nunchuk.Z = BTN\_Z_

**---**

**Activate the LED&#39;s on the Wiimote**

The Wiimote will work without this step, but if you would like to see that your Wiimote is connected or which controller mapping is currently mapped to that Wiimote, follow this step.

Add the following to the bottom of the file you just created:

_sudo nano /home/pi/myinput_

_#Plugin.led.Led1 = 1_

_#Plugin.led.Led2 = 1_

_#Plugin.led.Led3 = 1_

_#Plugin.led.Led4 = 1_

Remove the &quot;# &quot;on the line for the LED&#39;s you want to light up. You can go from no LED&#39;s lit to all LED&#39;s lit to everything in between.

---

**Get Wiimote Addresses**

**Scan for Wiimotes by typing:**

_hcitool scan_

See assets/images/hcitoolScan.PNG

**This will give you an address in form: XX:XX:XX:XX:XX:XX**

**Keep the address for later.**

---

**Create a Shell Script to Connect the Wiimotes**

Now we need to create a script that will connect the Wiimotes when we run it.

Create a directory and file for the script.

Make a directory by typing:

_mkdir /home/pi/bin_

Create the file by typing:

_sudo nano /home/pi/bin/connectwii.sh_

Copy and paste this into the file:

_#!/bin/bash_

_sleep 1 # Wait until Bluetooth services are fully initialized_

_hcitool dev | grep hci \&gt;/dev/null_

_if test $? -eq 0 ; then_

_wminput -d -c  /home/pi/mywminput 00:19:1D:48:D8:FD &amp;_

_wminput -d -c  /home/pi/mywminput 00:22:D7:C2:A6:B9 &amp;_

_else_

_echo &quot;Blue-tooth adapter not present!&quot;_

_exit 1_

_fi_

Note: you need a wminput line for each wiimote you are using.

Replace the addresses above with the addresses of your wiimotes.

If you have different controller mappings for different Wiimotes, replace &quot;mywminput&quot; with your controller mapping.

**Make the script just created executable by typing:**

_sudo chmod 775 /home/pi/connectwii.sh_

---

**Reboot your Raspberry Pi and test your script**

_sudo shutdown –r now_

_sudo modprobe uinput_

_/home/pi/connectwii.sh_

**Reconnect Wiimode to Bluethoot on RaspberryPi**

When you need to reconnect the Wiimote to the RaspberryPi, you need to use the sync button on the back of the Wiimote.

See assets/images/Wiimote2.JPG && assets/images/Wiimote3.JPG

---

**Test the Wiimote**

See assets/images/previeuwScreen_jktest-gtk.PNG

Install jstest-gtk to test your Wiimote as a controller.

_sudo apt-get install jstest-gtk_

_jstest-gtk_

You should see a gui that shows all valid inputs to test.

Select the Wiimote.

Press the buttons to see the Button Presses Register. In the picture, I am pressing the A button. You can see it register because the &quot;Buttons 4&quot; box transitions from white to black.

The Wiimote is configured!

### 5. Mapping Wiimote input with python

[https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html](https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html)


Every controller has different codes for their buttons.

First, we will need to write a code to see the bulk information about a buttonpress.

This first script will print all of the data to the shell, so be sure to make a note of the event codes and types for each button:

_#import evdev_

_from evdev import InputDevice, categorize, ecodes_

_#creates object &#39;gamepad&#39; to store the data_

_#you can call it whatever you like_

_wait = True_

_while wait:_

_gamepad = InputDevice('/dev/input/event3')_

_wait = False_

_except:_

_print(“waiting for wii remote to connect…”)_

_time.sleep(5)_

_#prints out device info at start_

_print(gamepad)_

_#evdev takes care of polling the controller in a loop_

_for event in gamepad.readloop():_

_print(categorize(event))_

See assets/images/raw-data-evdev-test.PNG

In the line &quot;event at ##########.#####, code ##, type ##, val #####.

The part you will need is the code. Every button has a different code. So by pressing every button on your Wiimote, the corresponding code will appear. Take notes of the pressed button and their code. In the next step you will need them.

---

This code will print the pressed button to the shell. You will need to fill in your code number with the corresponding button:

_#import evdev_

_from evdev import InputDevice, categorize, ecodes_

_#creates object &#39;gamepad&#39; to store the data_

_#you can call it whatever you like_

_wait = True_

_while wait:_

_gamepad = InputDevice('/dev/input/event3')_

_wait = False_

_except:_

_print(“waiting for wii remote to connect…”)_

_time.sleep(5)_

_#button code variables (change to suit your device)_

_aBtn = ##_

_up = ##_
_down = ##_
_left = ##_
_right = ##_

_#prints out device info at start_

_print(gamepad)_

_#loop and filter by event code and print the mapped label_

_for event in gamepad.read\_loop():_

_if event.type == ecodes.EV\_KEY:_

_if event.value == 1:_

_if event.code == aBtn:_

_print(&quot;A&quot;)_

_elif event.code == up:_

_print(&quot;up&quot;)_

_elif event.code == down:_

_print(&quot;down&quot;)_

_elif event.code == left:_

_print(&quot;left&quot;)_

_elif event.code == right:_

_print(&quot;right&quot;)_

See assets/images/mapped-data-evdev-test.PNG

Now the buttons are mapped, and you are ready to script your Diddyborg.

### 6. Adressing Thunderborg

[https://www.piborg.org/blog/thunderborg-getting-started](https://www.piborg.org/blog/thunderborg-getting-started)

The library from Thunderborg must be installed.

**install Library**

_mkdir ~/thunderborg_

_cd ~/thunderborg_

_wget http://www.piborg.org/downloads/thunderborg/examples.zip_

_unzip examples.zip_

_chmod +x install.sh_

_./install.sh_

In the snippet of code, we download the folder **examples.zip.** This foldercontains the file **Thunderborg.py.** This file needs to **be replaced to the root folder** of your project.



**Python Library**

_# Setup the library ready for use_

_import ThunderBorg                      # Load the library_

_TB = ThunderBorg.ThunderBorg()          # Create a board object_

_TB.Init()                               # Setup the board_

_# Setting motor speeds_

_TB.SetMotor1(power)                     # Set motor 1 speed – waarde tussen 0 en 1_

_TB.SetMotor2(power)                     # Set motor 2 speed – waarde tussen 0 en 1_

_TB.SetMotors(power)                     # Set speed of both motors_

_TB.MotorsOff()                          # Stop both motors_

_# Reading motor speeds_

_TB.GetMotor1()                          # Read motor 1 speed_

_TB.GetMotor2()                          # Read motor 2 speed_

_# Controlling the LED_

_TB.SetLed1(r, g, b)                     # Set the colour of the ThunderBorg LED (values from 0.0 to 1.0)_

_TB.GetLed1()                            # Read the colour of the ThunderBorg LED (values from 0.0 to 1.0)_

_TB.SetLed2(r, g, b)                     # Set the colour of the ThunderBorg Lid LED (values from 0.0 to 1.0)_

_TB.GetLed2()                            # Read the colour of the ThunderBorg Lid LED (values from 0.0 to 1.0)_

_TB.SetLeds(r, g, b)                     # Set the colour of both LEDs (values from 0.0 to 1.0)_

_# Battery monitoring_

_TB.SetLedShowBattery(enabled)           # Set if the LEDs reflect the current battery reading_

_TB.GetLedShowBattery()                  # Read if the LEDs reflect the current battery reading_

_TB.GetBatteryReading()                  # Read the current voltage level from the battery_

_TB.SetBatteryMonitoringLimits(min, max) # Set the limits for the LED based battery monitoring_

_TB.GetBatteryMonitoringLimits()         # Read the limits for the LED based battery monitoring_

_# Controlling the failsafe_

_TB.SetCommsFailsafe(enabled)            # Set if the communications failsafe is active_

_TB.GetCommsFailsafe()                   # Read if the communications failsafe is active_

_# Testing for faults_

_TB.GetDriveFault1()                     # See if there is a fault reported for M1_

_TB.GetDriveFault2()                     # See if there is a fault reported for M2_

_# RasPiO InsPiRing control_

_TB.SetExternalLedColours([[r,g,b], [r,g,b], [r,g,b], ..., [r,g,b]])_

_# Set the colour of each LED on the InsPiRing (values from 0.0 to 1.0)_

_# Setting parameters (before Init)_

_TB.i2cAddress = address                 # Set the address of the board to use_

_TB.printFunction = function             # Re-route / disable diagnostic messages_

_# Reading parameters (after Init)_

_print TB.busNumber                      # Shows which I²C bus the board is connected on_

_print TB.foundChip                      # See if the board is found / not found_

_# Other functions_

_ThunderBorg.ScanForThunderBorg()        # Sweep the I²C bus for available boards_

_ThunderBorg.SetNewAddress(address)      # Configure the attached board with a new address_

_TB.Help()                               # Get help on the available functions_

### 7. Starting program on boot

#### Run program on boot

[https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

All lines in rs.local get executed on boot:

_sudo nano /etc/rc.local_

To start diddy.py on boot add the line:

_sudo python PATH TO YOUR FILE &_

was added to /etc/rc.local
Now the program will execute without entering a screen first.



### 8. Sources

[https://www.piborg.org/blog/build/rpi-ps3-help](https://www.piborg.org/blog/build/rpi-ps3-help)

[https://www.piborg.org/robots/diddyborg-v2](https://www.piborg.org/robots/diddyborg-v2)

[https://www.instructables.com/id/Wiimote-Controller-Configuration-for-Raspberry-Pi-/](https://www.instructables.com/id/Wiimote-Controller-Configuration-for-Raspberry-Pi-/)

[https://www.piborg.org/blog/thunderborg-getting-started](https://www.piborg.org/blog/thunderborg-getting-started)

[https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html](https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html)

[https://www.instructables.com/id/Auto-Connection-of-the-Bluetooth-and-Auto-Running-/](https://www.instructables.com/id/Auto-Connection-of-the-Bluetooth-and-Auto-Running-/)

[https://pimylifeup.com/raspberry-pi-wiimote-controllers/](https://pimylifeup.com/raspberry-pi-wiimote-controllers/)

[https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

=======
# labo-4-diddyborg
Jeroen Vervaeck, Yoram Platteeuw

## Examples
### Move DiddyBorg 
### Control LED     (unfinished)
### Use webcam      (unfinished)
>>>>>>> 824b0a63d4c3a3d1d459be149b39818a06d3ca18
