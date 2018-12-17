from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

kbd = Keyboard()
mouse = Mouse()

#States
READING_GLOBALS=1
READING_MODE=2


#ActionModes
KBD=1
MOUSE=2

class Mode:
    def __init__(self, name):
#        self.name=name
        self.settings = {}
        self.triggers = []

class Trigger:
    def __init__(self, defString):
        #self.defString = defString
        parts = defString.split(" ", 1)
        parts= [p.strip() for p in parts]
        switchString = parts[0]
        actionString = parts[1]
        switchStrings = switchString.split(",")
        self.switchCode = 0x00000
        for s in switchStrings:
            self.switchCode |= (1 << int(s))
        actionStrings = actionString.split(" ")
        actionStrings = [a.strip() for a in actionStrings]
        self.actions = []
        for aString in actionStrings:
            codeList = []
            actionType = KBD
            keys = aString.split("+")
            for key in keys:
                code = getattr(Keycode, key, 0)
                if (code == 0):
                    #debug("Checking Custom Code for %s" % key)
                    actionType=MOUSE
                    code = getattr(Action, key, 0)
                codeList.append(code)
            codes = tuple(codeList)
            self.actions.append(Action(actionType, codes))

class Action:
    #MouseCodes
    MOUSE_UP= 1
    MOUSE_DOWN= 2
    MOUSE_LEFT= 3
    MOUSE_RIGHT=4
    LEFT_CLICK=10
    RIGHT_CLICK=11
    MIDDLE_CLICK=12
    def __init__(self, actionMode, codes):
        self.actionMode = actionMode
        self.codes = codes
    def perform(self):
        if (self.actionMode == KBD):
            kbd.send(*self.codes)
        elif(self.actionMode == MOUSE):
            for c in self.codes:
                if (c == Action.MOUSE_UP):
                    mouse.move(0,-5)
                elif (c == Action.MOUSE_DOWN):
                    mouse.move(0,5)
                elif (c == Action.MOUSE_LEFT):
                    mouse.move(-5,0)
                elif (c == Action.MOUSE_RIGHT):
                    mouse.move(5,0)
                elif (c == Action.LEFT_CLICK):
                    mouse.click(Mouse.LEFT_BUTTON)
                elif (c == Action.RIGHT_CLICK):
                    mouse.click(Mouse.RIGHT_BUTTON)

class Settings:
    def __init__(self):
        self.globalSettings = {}
        self.modes = []
        self.currentModeIdx = 0

    def getCurrentMode(self):
        return self.modes[self.currentModeIdx]

    def nextMode(self):
        self.currentModeIdx = (self.currentModeIdx + 1) % len(self.modes)
    def read(self, filename=None):
        state=READING_GLOBALS
        modeName = None
        fp = open(filename, 'rt')
        curMode = None
        for line in fp:
            parts = line.split(";", 1)
            value = str(parts[0]).strip()
            if (value == ''):
                continue
            if (state == READING_GLOBALS):
                if (value[0]=='[' and value[-1]==']'): #new  mode name
                    modeName = value[1:-1]
                    state = READING_MODE
                    curMode = Mode(modeName)
                    self.modes.append(curMode)
                else:#reading global setting
                    settingParts = line.split("=",1)
                    self.globalSettings[settingParts[0].strip()] = settingParts[1].strip()
            elif (state == READING_MODE):
                if (value[0]=='[' and value[-1]==']'): #new  mode name
                    modeName = value[1:-1]
                    curMode = Mode(modeName)
                    self.modes.append(curMode)
                elif (value[0].isdigit()):#new triggers
                    curMode.triggers.append(Trigger(value))
                else:#setting
                    settingParts = line.split("=",1)
                    curMode.settings[settingParts[0].strip()] = settingParts[1].strip()
		#At this point, we've read the settings, we need to get some defaults in and do some cleanup
		if ('modedelay' in self.globalSettings):
			self.globalSettings['modedelay'] = float(self.globalSettings['modedelay'])
		else:
			self.globalSettings['modedelay'] = 1.0
		if ('repeatdelay' in self.globalSettings):
			self.globalSettings['repeatdelay'] = float(self.globalSettings['repeatdelay'])
		else:
			self.globalSettings['repeatdelay'] = .15
	defmodecode=0b000010
	if ('modeswitches' in self.globalSettings):
		val = self.globalSettings['modeswitches']
		if(isinstance(val, str)):
			switchStrings = val.split(",")
			defmodecode = 0b000000
			for s in switchStrings:
				defmodecode |= (1 << int(s))
		else:
			defmodecode = (0b00000001 << int(val))
	self.globalSettings['modeswitches']=defmodecode