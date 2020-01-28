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
modes[0] = Mode("Retropie", "#0000ff")
modes[0].keyPress(1, "1")
modes[0].keyPress(2, "2")
modes[0].keyPress(3, Keycode.LEFT_ARROW)
modes[0].keyPress(4, Keycode.RIGHT_ARROW)

#One for Arrows (disabled by defalut)
modes[1] = Mode("Arrows", "#FF0000")
modes[1].keyPress(1, Keycode.UP_ARROW)
modes[1].keyPress(2, Keycode.DOWN_ARROW)
modes[1].keyPress(3, Keycode.LEFT_ARROW)
modes[1].keyPress(4, Keycode.RIGHT_ARROW)

# A section for common usage - might be better off first so it is the default
modes[2] = Mode("Common","#00FF00")
modes[2].keyPress(1, Keycode.SPACE)
modes[2].keyPress(2, Keycode.ENTER)
modes[2].keyPress(3, (Keycode.SPACE,Keycode.ENTER))
modes[2].keyPress(4, Keycode.SHIFT)