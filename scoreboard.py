from time import sleep
import time
import os
import random
import math

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

import pygame # for audio files

import board # Adafruit board library
import adafruit_dotstar as dotstar # Adafruit DotStar library

# Still need FTDI drivers 
# from ftdi.dmx_controller.OpenDmxUsb import OpenDmxUsb

# deputies = Blue
# outlaws = Red

# button callback functions
def blue_button_callback(channel):
    global bluesounds
    rand = random.randint(0,len(bluesounds) - 1)
    bluesounds[rand].play()
    print('blue')
    t_end = time.time() + .25
    # while time.time() < t_end:
    #     t.send_dmx([255,0,0,255])
    t_end = time.time() + .5
    # while time.time() < t_end:
    #     t.send_dmx([255,0,0,255])

def red_button_callback(channel):
    global redsounds
    rand = random.randint(0,len(redsounds) - 1)
    redsounds[rand].play()
    print('red')
    t_end = time.time() + .25 
    # while time.time() < t_end:
    #     t.send_dmx([255,255,0,0])
    t_end = time.time() + .5
    # while time.time() < t_end:
    #     t.send_dmx([255,255,0,0])

def real_blue_button_callback(channel):
    global outlaws
    global deputies
    deputies += 1
    print("real blue: {}".format(deputies))
    outf = open('./scores.txt','w')
    outf.write('{}\n{}\n'.format(outlaws,deputies))
    outf.close()
    update_LEDs()

def real_red_button_callback(channel):
    global outlaws
    global deputies
    outlaws += 1
    print("real red: {}".format(outlaws))
    outf = open('./scores.txt','w')
    outf.write('{}\n{}\n'.format(outlaws,deputies))
    outf.close()
    update_LEDs()

# LED functions
def update_LEDs(initialize=False):
    global outlaws
    global deputies
    global dots
    global deputythreshold
    global outlawthreshold
    currdeputy = int(math.log(deputies) * 14)
    curroutlaw = int(math.log(outlaws) * 14)
    print("current: red: {}  blue: {}".format(curroutlaw,currdeputy))
    if currdeputy > deputythreshold or initialize == True:
        print('in changing lights')
        for i in range(currdeputy):
            dots[i] = (0,0,255)
        deputythreshold = currdeputy
    if curroutlaw > outlawthreshold or initialize == True:
        print('in changing lights2')
        for i in range(288-curroutlaw,288):
            dots[i] = (255,0,0)
        outlawthreshold = curroutlaw
        
def test_LEDs(blue, red):
    global outlaws
    global deputies
    deputies = blue
    outlaws = red
    update_LEDs(True)

def reset_LEDs():
    for i in range(288):
        dots[i] = (0,0,0)

#load audio files for buttons
def load_sounds(dirname):
    sounds = []
    soundsnames = []
    for f in os.listdir(dirname):
        sounds.append(pygame.mixer.Sound('{}/'.format(dirname) + f))
        soundsnames.append(f)
    return sounds,soundsnames
    
# Start of main code

# Read in existing scores
inf = open('./scores.txt','r').readlines()
outlaws = int(inf[0].strip())
deputies = int(inf[1].strip())

# read in sounds
pygame.init()
bluesounds,bluesoundsnames = load_sounds('blue_sounds')
redsounds,redsoundsnames = load_sounds('red_sounds')

# prepare DMX
# t = OpenDmxUsb()

# initialize dots (LEDs)
dots = dotstar.DotStar(board.SCK, board.MOSI, 288, brightness=0.1)
reset_LEDs()
dots[0] = (0,0,255)
dots[287] = (255,0,0)

deputythreshold = int(math.log(deputies) * 14)
outlawthreshold = int(math.log(outlaws) * 14)
update_LEDs(initialize = True)

# Setup GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 15 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 3 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 19 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 26 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(15,GPIO.RISING,callback=red_button_callback,bouncetime=800) # Setup event on pin 15 rising edge
GPIO.add_event_detect(3,GPIO.RISING,callback=blue_button_callback,bouncetime=800) # Setup event on pin 3 rising edge
GPIO.add_event_detect(19,GPIO.RISING,callback=real_red_button_callback,bouncetime=800) # Setup event on pin 19 rising edge
GPIO.add_event_detect(26,GPIO.RISING,callback=real_blue_button_callback,bouncetime=800) # Setup event on pin 26 rising edge

# Terminate
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
reset_LEDs()
print("blue: {}, red: {}\n".format(deputies,outlaws))

