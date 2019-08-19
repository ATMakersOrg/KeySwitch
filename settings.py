from mode import Mode
from adafruit_hid.keycode import Keycode

#This global section sets how to change modes
#By default you hold down switches 1&2 for 2 seconds to switchmodes

modeSwitches=(5,) #which switches do you hold down to change modes
modeDelay=2.0 #And how many seconds does it wait when they're down

repeatDelay=.2

#Modifiers - these keys stay down while the other keys in the sequence are pressed
modifierKeys = (Keycode.SHIFT, Keycode.ALT, Keycode.CONTROL)
#For a single switch user, you might choose
#modeswitches=1
#modedelay=3.0
modes = {}

#This is a section for AAC Device Scanning
#It sends keycodes for 1-4 & Backspace and lights up blue
modes[0] = Mode("Scanning", "#0000ff")
modes[0].keyPress(1, "1")
modes[0].keyPress(2, "2")
modes[0].keyPress(3, "3")
modes[0].keyPress(4, "4")
#modes[0].keyPress(5, Keycode.BACKSPACE)
# default modeswitches will cycle through modes, but you can set a direct one
#modes[0].modeChange((1,2),"Windows",True)
#####

# A section for common usage - might be better off first so it is the default
modes[1] = Mode("Common","#FF0000")
modes[1].keyPress(1, Keycode.SPACE)
modes[1].keyPress(2, Keycode.ENTER)
modes[1].mouseClick(3, Mode.LEFT_BUTTON)
modes[1].mouseClick(4, Mode.RIGHT_BUTTON)
#modes[1].mouseClick(5, (Mode.LEFT_BUTTON, Mode.LEFT_BUTTON))

# One for moving the mouse
modes[2] = Mode("Mouse", "#00FF00")
modes[2].mouseMove(1, 0, -5)
modes[2].mouseMove(2, 0, 0)
modes[2].mouseMove(3, 5, 0)
modes[2].mouseMove(4, -5, 0)
#modes[2].mouseClick(5, Mode.LEFT_BUTTON)

#One for Arrows (disabled by defalut)
modes[3] = Mode("Arrows", "#FF00FF")
modes[3].keyPress(1, Keycode.UP_ARROW)
modes[3].keyPress(2, Keycode.DOWN_ARROW)
modes[3].keyPress(3, Keycode.LEFT_ARROW)
modes[3].keyPress(4, Keycode.RIGHT_ARROW)
#modes[3].keyPress(5, Keycode.CAPS_LOCK)

#And one that would be useful in a browser (Disabled)
modes[3] = Mode("Browser", "#FFFF00")
modes[3].keyPress(1, Keycode.SPACE)
modes[3].keyPress(2, Keycode.TAB)
modes[3].keyPress(3, (Keycode.SHIFT, Keycode.TAB))
modes[3].keyPress(4, Keycode.PAGE_DOWN)
#modes[3].keyPress(5, Keycode.PAGE_UP)