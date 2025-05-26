from time import sleep
import time

# Still need FTDI drivers 
# from ftdi.dmx_controller.OpenDmxUsb import OpenDmxUsb

from PyDMXControl.controllers import OpenDMXController

from PyDMXControl.profiles.Pulse import Compact_LED_Par

def blue():
    print('blue')
    t_end = time.time() + .25
    while time.time() < t_end:
         t.send_dmx([255,0,0,255])
    t_end = time.time() + .5
    while time.time() < t_end:
        t.send_dmx([255,0,0,255])

def red():
    print('red')
    t_end = time.time() + .25 
    while time.time() < t_end:
        t.send_dmx([255,255,0,0])
    t_end = time.time() + .5
    while time.time() < t_end:
        t.send_dmx([255,255,0,0])

dmx = OpenDMXController()
fixture = dmx.add_fixture(Compact_LED_PAR_8Ch, name="lightBar")
