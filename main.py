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

def stringPress(string,modifier):
    for char in string:
        keycode = layout._char_to_keycode(char)
        if keycode & layout.SHIFT_FLAG:
            keycode &= ~layout.SHIFT_FLAG
            kbd.press(Keycode.SHIFT)
        for m in modifier:
            kbd.press(m)
        kbd.press(keycode)

def keyPress(keycode,modifier):
        for m in modifier:
            kbd.press(m)
        kbd.press(keycode)

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
repeat = 0
codeStartTime = monotonic()
modifiersOn = []
modifiers = {}

for i in range(len(settings.modifierKeys)):
    modifiers[settings.modifierKeys[i]] = 0

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
                if type(keys) is int:
                    print("KeyPressed=",keys)
                    if keys in settings.modifierKeys:
                        modifiersOn.append(keys) if modifiers[keys]==0 else modifiersOn.remove(keys)
                        modifiers[keys] = not modifiers[keys]
                        print("Modifier",keys,"is:",modifiers[keys])
                    else:
                        keyPress(keys,modifiersOn)
                else:
                    for k in keys:
                        print("KeyPressed=",k)
                        if type(k) is str:
                            stringPress(k,modifiersOn)
                        elif type(k) is int and k in settings.modifierKeys:
                            modifiersOn.append(k) if modifiers[k]==0 else modifiersOn.remove(k)
                            modifiers[k] = not modifiers[k]
                            print("Modifier",k,"is:",modifiers[k])
                        else:
                            keyPress(k,modifiersOn)
            elif a[0] == Mode.MOUSE_MOVE:
                (actionType, x, y ,w) = a
                print("MouseMove x=",x,",y=",y,",w=",w)
                mouse.move(x,y,w)
            elif a[0] == Mode.MOUSE_CLICK:
                (actionType, button) = a
                print("MouseClick=", button)
                mouse.click(button)
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
    else:
        kbd.release_all()
    lastCode = switchCode
    sleep(repeatDelay)
    dot[0]=modeColor