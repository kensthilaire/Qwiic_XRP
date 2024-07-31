#
#-----------------------------------------------------------------------------
# xrp_led_strip.py
#

import math
import sys
import time

from xrp_config import read_config
import Qwiic.qwiic_led_stick as qwiic_led_stick

# dictionary of RGB values for a set of standard colors 
COLORS = {
    'red':    0xFF0000,
    'green':  0x00FF00,
    'blue':   0x0000FF,
    'yellow': 0xFFFF00,
    'purple': 0x9D00FF,

    'white':  0xFFFFFF,
    'off':    0x000000
}

class XrpLedStrip(qwiic_led_stick.QwiicLEDStick):
    def __init__(self, num_leds=10, brightness=1):
        super().__init__()
        
        self.num_leds=num_leds
        self.set_brightness(brightness)
        
        self.red_array = [None] * num_leds
        self.blue_array = [None] * num_leds
        self.green_array = [None] * num_leds

        if self.begin() == False:
            print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", file=sys.stderr)
            return

    def turn_off(self):
        self.set_rgb(0)
        
    def set_brightness(self, level):
        self.set_all_LED_brightness(level)
        
    def set_color(self, color):
        try:
            color_rgb = COLORS[color.lower()]
            self.set_rgb( color_rgb )
        except KeyError: 
            if color.lower() == 'rainbow':
                self.set_rainbow()
                return
            print( 'Unknown color specified: %s' % color )
        
    def set_rgb( self, rgb_value):
        red = (rgb_value >> 16) & 0xFF
        green = (rgb_value >> 8) & 0xFF
        blue = rgb_value & 0xFF
        self.set_all_LED_color( red, green, blue )
            
    def set_rainbow(self, num_colors=0, color_offset=0):
        if num_colors:
            rainbow_length = num_colors
        else:
            rainbow_length = self.num_leds
        
        for i in range(0, self.num_leds):
            # There are n colors generated for the rainbow
            # The value of n determins which color is generated at each pixel
            n = i + 1 - color_offset

            # Loop n so that it is always between 1 and rainbow_length
            if n <= 0:
                n = n + rainbow_length

            # The nth color is between red and yellow
            if n <= math.floor(rainbow_length / 6):
                self.red_array[i] = 255
                self.green_array[i] = int(math.floor(6 * 255 / rainbow_length * n))
                self.blue_array[i] = 0
            
            # The nth color is between yellow and green
            elif n <= math.floor(rainbow_length / 3):
                self.red_array[i] = int(math.floor(510 - 6 * 255 / rainbow_length * n))
                self.green_array[i] = 255
                self.blue_array[i] = 0
            
            # The nth color is between green and cyan
            elif n <= math.floor(rainbow_length / 2):
                self.red_array[i] = 0
                self.green_array[i] = 255
                self.blue_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 510))
            
            # The nth color is between blue and magenta
            elif n <= math.floor(5 * rainbow_length / 6):
                self.red_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 1020))
                self.green_array[i] = 0
                self.blue_array[i] = 255
            
            # The nth color is between magenta and red
            else:
                self.red_array[i] = 255
                self.green_array[i] = 0
                self.blue_array[i] = int(math.floor(1530 - (6 *255 / rainbow_length * n)))

        # Set all the LEDs to the color values accordig to the arrays
        self.set_all_LED_unique_color(self.red_array, self.green_array, self.blue_array, self.num_leds)
        
    def walk_rainbow(self, num_colors=40, speed=0.05):
        for i in range(0,num_colors):
            self.set_rainbow(num_colors, i)
            time.sleep(speed)
            

if __name__ == '__main__':
    # set default values for the LED strip
    num_leds = 10
    brightness = 1
    
    # attempt to read any defined config for the LED strip
    config = read_config(section='led_strip')
    if config:
        num_leds = config.get('num_leds', num_leds)
        brightness = config.get('brightness', brightness)

    # instantiate the LED strip and run through some colors
    try:
        xrp_strip = XrpLedStrip(num_leds=num_leds, brightness=brightness)
        
        # a set of standard colors have been defined about in COLORS 
        xrp_strip.set_color('red')
        time.sleep(2)
        xrp_strip.set_color('green')
        time.sleep(2)
        xrp_strip.set_color('blue')
        time.sleep(2)
        xrp_strip.set_color('yellow')
        time.sleep(2)

        # colors can be set by RGB value, too
        xrp_strip.set_rgb( 0x9D00FF)
        time.sleep(2)

        # how about a walking rainbow, too
        xrp_strip.walk_rainbow()

        # turn off the LEDs as we end
        xrp_strip.turn_off()
        
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
