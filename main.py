# Trinket IO demo
# Welcome to CircuitPython :)

from digitalio import DigitalInOut,Direction,Pull
import board

#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

import adafruit_dotstar
from time import sleep, monotonic

import SettingsParser
settings = SettingsParser.Settings()
settings.read('/settings.ini')

# Used if we do HID output, see below
# One pixel connected internally!
dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.8)

def hex2rgb(hexcode):
    #added 1 to all for #
    red = int("0x"+hexcode[1:3], 16)
    green = int("0x"+hexcode[3:5], 16)
    blue = int("0x"+hexcode[5:7], 16)
    rgb = (red, green, blue)
    return rgb

def handleLongPress(switchCode):
    if (switchCode == 0b000110):
        settings.nextMode()

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


black = (0, 0, 0)
modeColor = hex2rgb("#444400")
white=hex2rgb("#555555") 
modeDelay = 1

lastCode = 0
codeStartTime = monotonic()

while(True):
    #read the 5 switches
    num = 0
    switchCode = 0x00
    readTime = monotonic()
    for p in pins:
        num = num + 1
        if(p.value == False):
            switchCode |= (1 << num)
    if (switchCode != 0):
        for t in settings.getCurrentMode().triggers:
            if (t.switchCode == switchCode):
                for a in t.actions:
                    dot[0] = white
                    #print(a.codes)
                    a.perform()
                break
        if (switchCode != lastCode):
            lastCode = switchCode
            codeStartTime = readTime
        else:
            if (readTime > (codeStartTime + modeDelay)):
                handleLongPress(switchCode)
                codeStartTime = readTime
    lastCode = switchCode


    sleep(.15)
    dot[0] = modeColor