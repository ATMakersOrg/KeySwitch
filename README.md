# KeySwitch
This is a simple AT Switch Interface based on the ATMakers PCB design and a Feather Trinket M0

This allows keystrokes to be sent to a PC, MAC, or any USB HID central device based on the code and configuration files
on the Trinket device itself.

This is a CircuitPython project and many thanks to Adafruit and its staff and community for their help.

## Update KeySwitch code

### Method 1

*	Download the necessary files from KeySwitch github repository.
  1. Visit KeySwitch github repository at https://github.com/ATMakersOrg/KeySwitch
  2. Click on “Clone or download” button” in green.
  3. Click on “Download Zip” to download the necessary file.
  4. Extract “KeySwitch-master.zip” to the directory of your choice.
*	Tap the reset button twice to enter the bootloader. If it doesn't work on the first try, don't be discouraged. The rhythm of the taps needs to be correct and sometimes it takes a few tries.
*	The name of the drive will change from CIRCUITPY to TRINKETBOOT.
*	Drag and drop the KEYSWITCH_TRINKET.uf2 file to TRINKETBOOT drive.
* The led color should now change to blue to indicate color of the first mode.

### Method 2

#### Update uf2 bootloader

*	Download the latest version of CircuitPython (Version 5.0) for Adafruit Trinket M0 called something similar to adafruit-circuitpython-trinket_m0-en_US-5.0.0.uf2 file from https://circuitpython.org/board/trinket_m0/

*	Example: Download adafruit-circuitpython-trinket_m0-en_US-5.0.0-beta.4.uf2 file from https://circuitpython.org/board/trinket_m0/

*	Download drivers if you are using windows 7. You will not need to install drivers on Mac, Linux or Windows 10. https://github.com/adafruit/Adafruit_Windows_Drivers/releases/download/2.3.4/adafruit_drivers_2.3.4.0.exe 
*	Tap the reset button twice to enter the bootloader. If it doesn't work on the first try, don't be discouraged. The rhythm of the taps needs to be correct and sometimes it takes a few tries.
*	The name of the drive will change from CIRCUITPY to TRINKETBOOT.
*	Drag and drop the adafruit-circuitpython-trinket_m0-en_US-5.0.0.uf2 file to TRINKETBOOT drive.
*	The lights should flash again, BOOT will disappear and a new drive will show up on your computer called CIRCUITPY.
*	Now you can just change the code.

#### Update Software 

*	Download the necessary files from KeySwitch github repository.
  1. Visit KeySwitch github repository at https://github.com/ATMakersOrg/KeySwitch
  2. Click on “Clone or download” button” in green.
  3. Click on “Download Zip” to download the necessary file.
  4. Extract “KeySwitch-master.zip” to the directory of your choice.
*	Drag and drop lib library files from extracted “KeySwitch-master” folder in lib file under CIRCUITPY drive. 

*	The structure of lib directory:
* lib
  * adafruit_dotstar.mpy
  * adafruit_hid   
    * __init__.py
    * Keyboard.mpy
    * keyboard_layout_us.mpy
    * keycode.mpy
    * mouse.mpy   
* Drag and drop following files from extracted “KeySwitch-master” folder to CIRCUITPY drive:

  * main.py
  * mode.py
  * settings.py
  * README.md

*	You may need to press reset button to make it start functioning.

### Modes

Press and hold switch 5 to switch modes.

 <table style="width:100%">
  <tr>
    <th>Modes</th>
    <th>Switch actions</th>
    <th>Led Color</th>
  </tr>
    <tr>
    <td>Scanning</td>
<td>1 ONE
2 TWO
3 THREE
4 FOUR
1,2 FIVE
</td>
    <td>#0000FF (Blue)</td>
  </tr>
  <tr>
    <td>Common</td>
<td>1 SPACE
2 ENTER
3 LEFT_CLICK
4 RIGHT_CLICK
</td>
    <td>#FF0000</td>
  </tr>
  <tr>
    <td>Mouse</td>
<td>1 MOUSE_LEFT
2 MOUSE_RIGHT
3 MOUSE_UP
4 MOUSE_DOWN
</td>
    <td>#00FF00</td>
  </tr>
  <tr>
    <td>Arrows</td>
<td>1 UP_ARROW
2 DOWN_ARROW
3 LEFT_ARROW
4 RIGHT_ARROW
</td>
    <td>#FF00FF</td>
  </tr>
  <tr>
    <td>Browser</td>
<td>1 SPACE
2 TAB
3 SHIFT+TAB
4 PAGE_DOWN
</td>
    <td>#FFFF00</td>
  </tr>
</table> 

### Change Modes and switches 
*	settings.mpy file can be edited to change the modes and functionality of switches 
