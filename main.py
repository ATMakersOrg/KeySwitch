import adafruit_dotstar
import board
from digitalio import DigitalInOut,Direction,Pull
from time import sleep, monotonic

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from mode import Mode

def hex2rgb(hexcode):
    #added 1 to all for #
    red = int("0x"+hexcode[1:3], 16)
    green = int("0x"+hexcode[3:5], 16)
    blue = int("0x"+hexcode[5:7], 16)
    rgb = (red, green, blue)
    return rgb

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

mouse = Mouse()
kbd = Keyboard()
layout = KeyboardLayoutUS(kbd)

import settings

print(settings.modes)

modeDelay = settings.modeDelay
repeatDelay = settings.repeatDelay

modeSwitchCode = 0x0

for num in settings.modeSwitches:
    modeSwitchCode |= (1 << num)

modeNum = 0
currentMode = settings.modes[modeNum]

modeColor=hex2rgb(currentMode.color)


def handleLongPress(switchCode):
    global modeColor
    global modeNum
    global currentMode
#################
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

lastCode = 0
codeStartTime = monotonic()

while(True):
    num = 0
    switchCode = 0x00
    readTime = monotonic()
    for p in pins:
        num = num + 1
        if(p.value == False):
            switchCode |= (1 << num)
    if (switchCode != 0):
        if (switchCode in currentMode.actions):
            a = currentMode.actions[switchCode]
            if a[0] == Mode.KEY_PRESS:
                (actionType, keys, longPress) = a
                print(keys)
                if type(keys) is str:
                    layout.write(keys)
                else:
                    kbd.send(keys)
        if (switchCode != lastCode):
            print("NewCode")
            lastCode = switchCode
            codeStartTime = readTime
        else:
            if (readTime > (codeStartTime + modeDelay)):
                print("longPress")
                if (switchCode == modeSwitchCode):
                    numOfModes = len(settings.modes)
                    modeNum = (modeNum + 1) % numOfModes
                    currentMode = settings.modes[modeNum]
                    modeColor=hex2rgb(currentMode.color)
                    dot[0]=modeColor
                codeStartTime = readTime
    lastCode = switchCode
    sleep(repeatDelay)
    dot[0]=modeColor