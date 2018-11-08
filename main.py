# Trinket IO demo
# Welcome to CircuitPython :)

from digitalio import DigitalInOut,Direction,Pull
import board
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse


#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

#import adafruit_dotstar
from time import sleep

import SettingsParser
settings = SettingsParser.Settings()
settings.read('/settings.ini')

# Used if we do HID output, see below
# One pixel connected internally!
#dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.8)

#def hex2rgb(hexcode):
#    red = int("0x"+hexcode[0:2], 16)
#    green = int("0x"+hexcode[2:4], 16)
#    blue = int("0x"+hexcode[4:6], 16)
#    rgb = (red, green, blue)
#    print(rgb)
#    return rgb

pins = [ 
        DigitalInOut(board.D0),
        DigitalInOut(board.D1),
        DigitalInOut(board.D2),
        DigitalInOut(board.D3),
        DigitalInOut(board.D4)
        ]
for p in pins:
    p.direction = Direction.INPUT
    p.pull = Pull.UP

values = [False]*6

kbd = Keyboard()

while(True):
    #read the 5 switches
    num = 0
    for p in pins:
        num = num + 1
        values[num] = p.value
    for t in settings.currentMode.triggers:
        activate = True
        for s in t.switches:
            #If the value is True, it's not pressed
            if (values[s]):
                activate = False
                break
        if (activate):
            for a in t.actions:
                #print(a.codes)
                kbd.send(*a.codes)
            
    sleep(.1)