# scoreboard.py

import sys
import time
import os
import random
import math
import subprocess
import threading

from sbSounds import sbSounds
from time import sleep

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

import pygame # for audio files

import board # Adafruit board library
import adafruit_dotstar as dotstar # Adafruit DotStar library

# Still need FTDI drivers 
# from ftdi.dmx_controller.OpenDmxUsb import OpenDmxUsb

# button callback functions
def button_blue_effect(channel):
    global bluesounds
    rand = random.randint(0,len(bluesounds) - 1)
    if  (not pygame.mixer.get_busy()):
        bluesounds[rand].play()
    print('blue')
    t_end = time.time() + .25
    # while time.time() < t_end:
    #     t.send_dmx([255,0,0,255])
    t_end = time.time() + .5
    # while time.time() < t_end:
    #     t.send_dmx([255,0,0,255])

def button_red_effect(channel):
    global redsounds
    rand = random.randint(0,len(redsounds) - 1)
    if  (not pygame.mixer.get_busy()):
        redsounds[rand].play()
    print('red')
    t_end = time.time() + .25 
    # while time.time() < t_end:
    #     t.send_dmx([255,255,0,0])
    t_end = time.time() + .5
    # while time.time() < t_end:
    #     t.send_dmx([255,255,0,0])

def score_blue_button_callback(channel):
    global scoreRed
    global scoreBlue
    scoreBlue += 1
    print("real blue: {}".format(scoreBlue))
    outf = open('./scores.txt','w')
    outf.write('{}\n{}\n'.format(scoreRed,scoreBlue))
    outf.close()
    update_LEDs()

def score_red_button_callback(channel):
    global scoreRed
    global scoreBlue
    scoreRed += 1
    print("real red: {}".format(scoreRed))
    outf = open('./scores.txt','w')
    outf.write('{}\n{}\n'.format(scoreRed,scoreBlue))
    outf.close()
    update_LEDs()

# LED functions
def update_LEDs(initialize=False):
    global scoreRed
    global scoreBlue
    global dots
    global threshold_blue
    global threshold_red
    currBlue = int(math.log(scoreBlue) * 14)
    currRed = int(math.log(scoreRed) * 14)
    print("current: red: {}  blue: {}".format(currRed,currBlue))
    if currBlue > threshold_blue or initialize == True:
        print('in changing lights')
        for i in range(currBlue):
            dots[i] = (0,0,255)
        threshold_blue = currBlue
    if currRed > threshold_red or initialize == True:
        print('in changing lights2')
        for i in range(288-currRed,288):
            dots[i] = (255,0,0)
        threshold_red = currRed
        
def test_LEDs(blue, red):
    global scoreRed
    global scoreBlue
    scoreBlue = blue
    scoreRed = red
    update_LEDs(True)

def reset_LEDs():
    for i in range(288):
        dots[i] = (0,0,0)

#load audio files for buttons
def sounds_load(dirname):
    sounds = []
    soundsnames = []
    for f in os.listdir(dirname):
        sounds.append(pygame.mixer.Sound('{}/'.format(dirname) + f))
        soundsnames.append(f)
    return sounds,soundsnames

# Test sounds 
def sounds_test(soundList):
    for sound in soundList:
        sound.play()
        while(pygame.mixer.get_busy()):
            time.sleep(0.1)

def sounds_init(redSoundList, blueSoundList):
    print("Starting the initialization of the red and blue sounds.")
    # Set Volume
    cmd = subprocess.run(["/usr/bin/amixer","set","Master","30%"])
    sounds_test(redSoundList)
    sounds_test(blueSoundList)
    cmd = subprocess.run(["/usr/bin/amixer","set","Master","100%"])
    print("Finished the initialization of the red and blue sounds.")


# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    # Defining Globals
    global scoreRed
    global scoreBlue
    global dots
    global threshold_blue
    global threshold_red
    global bluesounds
    global redsounds
    # This GlobaLS section should be removed as Globals are moved into the classes and are passed deliberatly.

    # Read in existing scores
    inf = open('./scores.txt','r').readlines()
    scoreRed = int(inf[0].strip())
    scoreBlue = int(inf[1].strip())

    # read in sounds
    pygame.init()
    bluesounds,bluesoundsnames = sounds_load('blue_sounds')
    redsounds,redsoundsnames = sounds_load('red_sounds')
    print("Calling the sound initialization Function.")
    sounds_init(bluesounds, redsounds)
    print("Returned from the sound initialization Function.")

    # prepare DMX
    # t = OpenDmxUsb()

    # initialize dots (LEDs) 2 strings of 144 RGB LEDs = 288 LEDs
    dots = dotstar.DotStar(board.SCK, board.MOSI, 288, brightness=0.1)
    reset_LEDs()
    dots[0] = (0,0,255)
    dots[287] = (255,0,0)

    threshold_blue = int(math.log(scoreBlue) * 14)
    threshold_red = int(math.log(scoreRed) * 14)
    update_LEDs(initialize = True)

    # Setup GPIO for buttons
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False) # Ignore warning for now

    # Red Effect Button
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 18 to be an input pin and set initial value to be pulled High (off)
    GPIO.add_event_detect(18,GPIO.RISING,callback=button_red_effect,bouncetime=50) # Setup event on GPIO 18 rising edge

    # Blue Effect Button
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 24 to be an input pin and set initial value to be pulled High (off)
    GPIO.add_event_detect(24,GPIO.RISING,callback=button_blue_effect,bouncetime=50) # Setup event on GPIO 24 rising edge

    # Red Score Button
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 19 to be an input pin and set initial value to be pulled High (off)
    GPIO.add_event_detect(19,GPIO.RISING,callback=score_red_button_callback,bouncetime=50) # Setup event on GPIO 19 rising edge

    # Blue Score Button
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 16 to be an input pin and set initial value to be pulled High (off)
    GPIO.add_event_detect(16,GPIO.RISING,callback=score_blue_button_callback,bouncetime=50) # Setup event on GPIO 16 rising edge

    # Terminate
    message = input("Press enter to quit\n\n") # Run until someone presses enter
    GPIO.cleanup() # Clean up
    reset_LEDs()
    print("blue: {}, red: {}\n".format(scoreBlue,scoreRed))

    # End Main Function and Return 0 
    # 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main())  
