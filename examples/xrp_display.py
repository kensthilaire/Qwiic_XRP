#
#-----------------------------------------------------------------------------
# xrp_display.py
#

import Qwiic.qwiic_oled_display as qwiic_oled_display
import sys
import time

'''
For font type of 0, the maximum line length is 21 characters, the line height is 12
and there are 3 display lines with 0 padding space.

For font type of 1, the maximum line length is 14 characters, the line height is 15
and there are 2 display lines with 4 padding space.

'''

class XrpDisplay(qwiic_oled_display.QwiicOledDisplay):
    def __init__(self, font_type=0):
        super().__init__()
        
        self.line_buffer = []
        self.font_type = font_type
        
        self.set_font(font_type)
        
        if not self.connected:
            print("The Qwiic OLED Display isn't connected to the system. Please check your connection", \
                file=sys.stderr)
            return
    
        self.begin()
        self.display()
        time.sleep(1)

        #  clear(ALL) will clear out the OLED's graphic memory.
        self.clear(self.ALL) #  Clear the display's memory (gets rid of artifacts)
        self.clear(self.PAGE)  #  Clear the display's buffer
        self.display()  #  Display buffer contents

    def clear_display(self):
        self.clear(self.PAGE)
        self.display()
        
    def set_font(self,font_type):
        self.set_font_type(font_type)
        if font_type == 0:
            self.line_height = 12
            self.line_length = 21
            self.padding_top = 0
            self.num_lines = 3
        elif font_type ==1:
            self.line_height = 15
            self.line_length = 14
            self.padding_top = 4
            self.num_lines = 2
        
    def hello(self):
        #  Print "Hello World"
        #  ---------------------------------------------------------------------------
        #  Add text
        self.set_font(1)
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
    try:
        xrp_display = XrpDisplay(font_type=0)
        
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
