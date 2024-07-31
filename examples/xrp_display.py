#
#-----------------------------------------------------------------------------
# xrp_display.py
#

import sys
import time

from xrp_config import read_config
import Qwiic.qwiic_oled_display as qwiic_oled_display

'''
For font type of 0, the maximum line length is 21 characters, the line height is 12
and there are 3 display lines with 0 padding space.

For font type of 1, the maximum line length is 14 characters, the line height is 15
and there are 2 display lines with 4 padding space.

'''
DISPLAY_TYPES = {
    'small': {
        'font_type': 0,
        'line_length': 21,
        'line_height': 12,
        'padding_type': 0,
        'num_lines': 3
    },
    'medium': {
        'font_type': 1,
        'line_length': 14,
        'line_height': 15,
        'padding_type': 4,
        'num_lines': 2
    },

    'end' : {}
}
DEFAULT_DISPLAY_TYPE = DISPLAY_TYPES['small']

class XrpDisplay(qwiic_oled_display.QwiicOledDisplay):
    def __init__(self, display_type=DEFAULT_DISPLAY_TYPE):
        super().__init__()
        
        self.line_buffer = []
        
        
        if not self.connected:
            print("The Qwiic OLED Display isn't connected to the system. Please check your connection", \
                file=sys.stderr)
            return
    
        self.begin()
        self.display()
        time.sleep(1)
        
        self.set_display_type(display_type)

        #  clear(ALL) will clear out the OLED's graphic memory.
        self.clear(self.ALL) #  Clear the display's memory (gets rid of artifacts)
        self.clear(self.PAGE)  #  Clear the display's buffer
        self.display()  #  Display buffer contents

    def clear_display(self):
        self.clear(self.PAGE)
        self.display()
        
    def set_display_type(self,display_type):
        try:
            display_cfg = DISPLAY_TYPES[display_type.lower()]
        except KeyError:
            print( 'Unsupported Display Type: %s' % display_type )
            display_cfg = DEFAULT_DISPLAY_TYPE

        self.set_font_type(display_cfg['font_type'])
        self.line_height = display_cfg['line_height']
        self.line_length = display_cfg['line_length']
        self.padding_top = display_cfg['padding_type']
        self.num_lines = display_cfg['num_lines']
        
    def hello(self):
        #  Print "Hello World"
        #  ---------------------------------------------------------------------------
        #  Add text
        self.set_cursor(0,0)
        self.print("Hello XRP!")
        self.display()
            
    def print_ln(self, line):
        self.clear(self.PAGE)  #  Clear the display's buffer
        self.line_buffer.append(line[:self.line_length])
        if len(self.line_buffer) > self.num_lines:
            self.line_buffer.pop(0)
        
        line_index = self.padding_top
        for i in range(0,len(self.line_buffer)):
            self.set_cursor(0,line_index)
            self.print(self.line_buffer[i])
            line_index += self.line_height
        self.display()
        

if __name__ == '__main__':
    display_type = DEFAULT_DISPLAY_TYPE

    # attempt to read any defined config for the display
    config = read_config(section='oled_display')
    if config:
        display_type = config.get('display_type', display_type)

    try:
        xrp_display = XrpDisplay(display_type=display_type)
        
        xrp_display.hello()
        time.sleep(1)
        
        xrp_display.print_ln( 'Test Line 1')
        xrp_display.print_ln( 'Test Line 2')
        xrp_display.print_ln( 'Test Line 3')
        xrp_display.print_ln( 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
        xrp_display.print_ln( 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ')
        xrp_display.print_ln( '1234567890123456789012345678901234567890')
        
        time.sleep(2)
        xrp_display.clear_display()

    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding XRP Display Example")
        sys.exit(0)
