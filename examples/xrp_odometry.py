#
#-----------------------------------------------------------------------------
# xrp_odometry.py
#

import Qwiic.qwiic_otos as qwiic_otos
import sys
import time

class XrpOdometry(qwiic_otos.QwiicOTOS):
    def __init__(self, units='inches'):
        super().__init__()
        
        # Check if it's connected
        if self.is_connected() == False:
            print("The device isn't connected to the system. Please check your connection", \
                file=sys.stderr)
            return
    
        # Initialize the device
        self.begin()
    
        # Set the default units for the sensor
        units = units.lower()
        if units == 'inches':
            self.setLinearUnit(self.kLinearUnitInches)
        elif units == 'meters':
            self.setLinearUnit(self.kLinearUnitMeters)
        else:
            print( 'Unsupported units parameter: %s' % units )

        print("Ensure the OTOS is flat and stationary during calibration!")
        for i in range(5, 0, -1):
            print("Calibrating in %d seconds..." % i)
            time.sleep(1)
    
        # Calibrate the IMU, which removes the accelerometer and gyroscope offsets
        print("Calibrating IMU...")
        self.calibrateImu()
    
        # Reset the tracking algorithm - this resets the position to the origin,
        # but can also be used to recover from some rare tracking errors
        self.resetTracking()
        
        
    def print_position(self):
        # Get the latest position, which includes the x and y coordinates, plus
        # the heading angle
        myPosition = self.getPosition()

        # Print measurement
        print()
        print("Position:")
        print("X (Inches): {}".format(myPosition.x))
        print("Y (Inches): {}".format(myPosition.y))
        print("Heading (Degrees): {}".format(myPosition.h))

if __name__ == '__main__':
    try:
        xrp_odometry = XrpOdometry()
        
        while True:
            xrp_odometry.print_position()
            
            time.sleep(0.5)
        
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding XRP Odometry Example")
        sys.exit(0)
