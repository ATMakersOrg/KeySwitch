class Mode(object):
    """Represents one of several interface modes"""

    KEY_PRESS=1
    MOUSE_MOVE=2
    MOUSE_CLICK=3

    LEFT_BUTTON=1
    RIGHT_BUTTON=2
    MIDDLE_BUTTON=3

    def __init__(self, name, color="#FFFFFF"):
        """Make an instance.
        :param string name: Name for reference and reporting
        :param string color: HEX code (hash optional) to light up on key presses on this mode
        """
        self.name=name
        self.color=color
        self.actions = {}

    def _addAction(self, switches, action):
        switchBits = 0x0
        if type(switches) is int:
            switchBits = 0x1 << switches
        elif isinstance(switches, (list, tuple)):
            for s in switches:
                sBits = 0x1 << s
                switchBits |= sBits
        self.actions[switchBits]= action

    def keyPress(self, switches, action,longPress=False):
        self._addAction(switches, (Mode.KEY_PRESS, action, longPress))

    def mouseMove(self, switches, x, y , w=0):
        self._addAction(switches, (Mode.MOUSE_MOVE, x, y, w))

    def mouseClick(self, switches, button):
        self._addAction(switches, (Mode.MOUSE_CLICK, button))