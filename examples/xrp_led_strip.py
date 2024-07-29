#
#-----------------------------------------------------------------------------
# xrp_led_strip.py
#

import Qwiic.qwiic_led_stick as qwiic_led_stick
import math
import sys
import time

class XrpLedStrip(qwiic_led_stick.QwiicLEDStick):
    def __init__(self, num_leds=10):
        super().__init__()
        
        self.num_leds=10
        
        self.red_array = [None] * num_leds
        self.blue_array = [None] * num_leds
        self.green_array = [None] * num_leds

        if self.begin() == False:
            print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", file=sys.stderr)
            return

    def turn_off(self):
        self.set_brightness(0)
        
    def set_brightness(self, level):
        self.set_all_LED_brightness(level)
        
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
        
    def walk_rainbow(self, num_colors=20, delay=0.05):
        for i in range(0,num_colors):
            self.set_rainbow(num_colors, i)
            time.sleep(delay)
            
    def set_color(self, color):
        red = 0
        green = 0
        blue = 0
        color = color.lower()
        if color == 'red':
            red = 0xff
        elif color == 'green':
            green = 0xff
        elif color == 'blue':
            blue = 0xff
        elif color == 'rainbow':
            self.set_rainbow()
            return
            
        self.set_all_LED_color( red, green, blue )
        
    def set_rgb( self, rgb_value):
        red = (rgb_value >> 16) & 0xFF
        green = (rgb_value >> 8) & 0xFF
        blue = rgb_value & 0xFF
        self.set_all_LED_color( red, green, blue )
            

if __name__ == '__main__':
    try:
        xrp_strip = XrpLedStrip(num_leds=10)
        
        xrp_strip.set_brightness(1)
        xrp_strip.set_color('red')
        time.sleep(2)
        xrp_strip.set_color('green')
        time.sleep(2)
        xrp_strip.set_color('blue')
        time.sleep(2)
        xrp_strip.set_rgb( 0x9D00FF)
        time.sleep(2)
        xrp_strip.walk_rainbow(num_colors=40)

        xrp_strip.turn_off()
        
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
