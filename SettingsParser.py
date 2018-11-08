from adafruit_hid.keycode import Keycode

DEBUG=0

#States
READING_GLOBALS=1
READING_MODE=2

def debug(value):
    if (DEBUG == 1):
        print(value)

class Mode:
    def __init__(self, name):
        self.name=name
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
        self.switches = [int(a) for a in switchStrings]
        actionStrings = actionString.split(" ")
        actionStrings = [a.strip() for a in actionStrings]
        self.actions = []
        for aString in actionStrings:
            codeList = []
            actionType = Action.KBD
            keys = aString.split("+")
            for key in keys:
                code = getattr(Keycode, key, 0)
                if (code == 0):
                    #debug("Checking Custom Code for %s" % key)
                    actionType=Action.MOUSE
                    code = 0
                codeList.append(code)
            codes = tuple(codeList)
            self.actions.append(Action(actionType, codes))
            
class Action:
    def __init__(self, actionMode, codes):
        self.actionMode = actionMode
        self.codes = codes
    KBD=1
    MOUSE=2

class Settings:
    def __init__(self):
        self.globalSettings = {}
        self.modes = {}
        self.currentMode=None

    def read(self, filename=None, fp=None):
        state=READING_GLOBALS
        modeName = None
#      """Read and parse a filename or a list of filenames."""
        if not fp and not filename:
            print("ERROR : no filename and no fp")
            raise
        elif not fp and filename:
            fp = open(filename, 'rt')
        for line in fp:
            #remove the comment
            parts = line.split(";", 1)
            value = str(parts[0]).strip()
            if (value == ''):
                continue
            #debug(value)
            if (state == READING_GLOBALS):
                if (value[0]=='[' and value[-1]==']'): #new  mode name
                    modeName = value[1:-1]
                    state = READING_MODE
                    self.modes[modeName] = Mode(modeName)
                    if (self.currentMode is None):
                        self.currentMode = self.modes[modeName]
                else:#reading global setting
                    settingParts = line.split("=",1)
                    self.globalSettings[settingParts[0].strip()] = settingParts[1].strip()
            elif (state == READING_MODE):
                if (value[0]=='[' and value[-1]==']'): #new  mode name
                    #debug(self.modes[modeName].settings)
                    #debug(self.modes[modeName].triggers)
                    modeName = value[1:-1]
                    self.modes[modeName] = Mode(modeName)
                elif (value[0].isdigit()):#new triggers
                    self.modes[modeName].triggers.append(Trigger(value))
                else:#setting
                    settingParts = line.split("=",1)
                    self.modes[modeName].settings[settingParts[0].strip()] = settingParts[1].strip()

HIGHEST_PROTOCOL = 0

def dumps(obj, proto=0):
    return repr(obj).encode()

def loads(s):
    d = {}
    s = s.decode()
    if "(" in s:
        qualname = s.split("(", 1)[0]
        if "." in qualname:
            pkg = qualname.rsplit(".", 1)[0]
            mod = __import__(pkg)
            d[pkg] = mod
    return eval(s, d)