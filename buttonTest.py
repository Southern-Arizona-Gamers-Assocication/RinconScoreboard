# buttonTest.py
# This script is designed to test the functionality of buttons connected to a Raspberry Pi.
# It counts the number of times each button is pressed and prints the count to the console.
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

import board # Adafruit board library
import adafruit_dotstar as dotstar # Adafruit DotStar library

def blue_effect_button_callback(channel):
    blue_effect_count += 1
    print("effect blue: {}".format(blue_effect_count))

def red_effect_button_callback(channel):
    red_effect_count += 1
    print("effect red: {}".format(red_effect_count))

def score_blue_button_callback(channel):
    deputies += 1
    print("real blue: {}".format(deputies))

def score_red_button_callback(channel):
    outlaws += 1
    print("real red: {}".format(outlaws))
    
# Start of main code
blue_effect_count = 0
red_effect_count = 0
outlaws = 0
deputies = 0

# Setup GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Ignore warning for now

# Red Effect Button
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 18 to be an input pin and set initial value to be pulled High (off)
GPIO.add_event_detect(18,GPIO.RISING,callback=red_effect_button_callback,bouncetime=50) # Setup event on GPIO 18 rising edge

# Blue Effect Button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 24 to be an input pin and set initial value to be pulled High (off)
GPIO.add_event_detect(24,GPIO.RISING,callback=blue_effect_button_callback,bouncetime=50) # Setup event on GPIO 24 rising edge

# Red Score Button
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 19 to be an input pin and set initial value to be pulled High (off)
GPIO.add_event_detect(19,GPIO.RISING,callback=score_red_button_callback,bouncetime=50) # Setup event on GPIO 19 rising edge

# Blue Score Button
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 16 to be an input pin and set initial value to be pulled High (off)
GPIO.add_event_detect(16,GPIO.RISING,callback=score_blue_button_callback,bouncetime=50) # Setup event on GPIO 16 rising edge

# Terminate
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
print("blue: {}, red: {}\n".format(deputies,outlaws))

