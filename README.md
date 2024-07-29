# Qwiic_XRP

This repository contains QWIIC device drivers ported for use with XRP.

The following devices are currently supported:

* [SparkFun Qwiic OLED Display](https://www.sparkfun.com/products/24606)
* [SparkFun Qwiic LED Stick](https://www.sparkfun.com/products/18354)
* [Person Sensor by Useful Sensors](https://www.sparkfun.com/products/21231)
* [SparkFun Optical Tracking Odometry Sensor](https://www.sparkfun.com/products/24904)

## Installation

The XRP Code Editor does not support copying a directory (folder) hierarchy from your computer to the XRP, so these instructions will guide you through manually creating the necessary folders on the XRP and then uploading the files to the appropriate folder on your XRP. Note that the folder hierarchy aligns with the default hierarchy from SparkFun device drivers and we want to minimize the code reorganization when porting the drivers for use with XRP.

### Qwiic General Installation

In order to use any of the supported drivers, you must first install the general Qwiic I2C device driver that has been ported to the XRP platform. In order to keep the top level **`/lib`** folder uncluttered, all Qwiic device support will be installed in a subfolder called **`Qwiic`**.

1. Connect to the target XRP robot using the [XRP Code Editor](https://xrpcode.wpi.edu/).
2. Copy the file **`__future__.py`** from the **`GitHub/XRP_Qwiic`** repo to the **`/lib`** folder by selecting **File** from the top menu, select **Upload To XRP**, and navigate to the file **`__future__.py`**. Select the **`/lib`** as the destination folder.
3. Right click on the **`/lib`** folder, select **New Folder**, and create a folder named **`Qwiic`**.
4. Navigate to the new **`Qwiic`** folder, right click on that folder and create a subfolder called **`qwiic_i2c`** and **`qwiic_oled_base`** under the Qwiic folder.
5. From **`GitHub/XRP_Qwiic/Qwiic/qwiic_i2c`**, upload all files to the folder **`/lib/Qwiic/qwiic_i2c`**.

### OLED Display Driver Installation

1. From **`GitHub/XRP_Qwiic/Qwiic/`**, upload **`qwiic_oled_display.py`** file to the folder **`/lib/Qwiic`**.
2. Right click on the **`/lib/Qwiic`** folder and create a subfolder called **`qwiic_oled_base`** under the Qwiic folder.
3. Navigate to the new **`qwiic_oled_base`** folder, right click on that folder and create a subfolder **`fonts`**.
4. From **`GitHub/XRP_Qwiic/Qwiic/qwiic_oled_base`**, upload all files to the folder **`/lib/Qwiic/qwiic_oled_base`**.
5. From **`GitHub/XRP_Qwiic/Qwiic/qwiic_oled_base/fonts`**, upload all files to the folder **`/lib/Qwiic/qwiic_oled_base/fonts`**.

### LED Stick Driver Installation

1. From **`GitHub/XRP_Qwiic/Qwiic/`**, upload **`qwiic_led_stick.py`** file to the folder **`/lib/Qwiic`**.

### Person Sensor Driver Installation

1. From **`GitHub/XRP_Qwiic/Qwiic/`**, upload **`qwiic_person_sensor.py`** file to the folder **`/lib/Qwiic`**.

## Examples

Sample code using each of the supported Qwiic devices is available in the **`examples`** folder in the **`GitHub/XRP_Qwiic`** repo. Simply upload any of the example files to the base directory on your XRP to test out the device and driver.

### OLED Display Example

The **`xrp_display.py`** example contains a class definition that encapsulates the base device driver and provides a multiline display buffer for the SparkFun OLED display device. Instantiate the XrpDisplay class in your program to have your XRP display status information at runtime.

### LED Strip Example

The **`xrp_led_strip.py`** example contains a class definition that encapsulates the base device driver and provides support for the SparkFun LED strip with 10 pixels. Intantiate the XrpLedStick class in your program to allow your XRP to display status via the LED strip.

### Person Sensor Example

The **`xrp_person_sensor.py`** example contains a class definition that encapsulates the base device driver and provides support for the UsefulSensor's Person Sensor device. Intantiate the XrpPersonSensor class in your program to allow your XRP to detect a human face and control behavior based on facial recognition.




