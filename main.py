import adafruit_dotstar
import board
from digitalio import DigitalInOut,Direction,Pull

from time import sleep, monotonic
def hex2rgb(hexcode):
    #added 1 to all for #
    red = int("0x"+hexcode[1:3], 16)
    green = int("0x"+hexcode[3:5], 16)
    blue = int("0x"+hexcode[5:7], 16)
    rgb = (red, green, blue)
    return rgb

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.8)

import SettingsParser
settings = SettingsParser.Settings()
settings.read('/settings.ini')

modeDelay = settings.globalSettings['modedelay']
repeatDelay = settings.globalSettings['repeatdelay']
modeSwitchCode = settings.globalSettings['modeswitches']
modeColor=hex2rgb(settings.getCurrentMode().settings.get("color","#555555"))

def handleLongPress(switchCode):
    global modeColor
    if (switchCode == modeSwitchCode):
        settings.nextMode()
        modeColor=hex2rgb(settings.getCurrentMode().settings.get("color","#555555"))
        dot[0]=modeColor

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
        for t in settings.getCurrentMode().triggers:
            if (t.switchCode == switchCode):
                for a in t.actions:
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
    sleep(repeatDelay)
    dot[0]=modeColor