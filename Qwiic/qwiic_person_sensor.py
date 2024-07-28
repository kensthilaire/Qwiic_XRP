
# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import Qwiic.qwiic_i2c as qwiic_i2c
import ustruct as struct
import time

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = 'Qwiic Person Sensor'

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x62]

# We will be reading raw bytes over I2C, and we'll need to decode them into
# data structures. These strings define the format used for the decoding, and
# are derived from the layouts defined in the developer guide.
PERSON_SENSOR_I2C_HEADER_FORMAT = 'BBH'
PERSON_SENSOR_I2C_HEADER_BYTE_COUNT = struct.calcsize(
    PERSON_SENSOR_I2C_HEADER_FORMAT)

PERSON_SENSOR_FACE_FORMAT = 'BBBBBBbB'
PERSON_SENSOR_FACE_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_FACE_FORMAT)

PERSON_SENSOR_FACE_MAX = 4
PERSON_SENSOR_RESULT_FORMAT = PERSON_SENSOR_I2C_HEADER_FORMAT + \
    'B' + PERSON_SENSOR_FACE_FORMAT * PERSON_SENSOR_FACE_MAX + 'H'
PERSON_SENSOR_RESULT_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_RESULT_FORMAT)

PERSON_SENSOR_REG_MODE          = 0x01
PERSON_SENSOR_REG_ENABLE_ID     = 0x02
PERSON_SENSOR_REG_SINGLE_SHOT   = 0x03
PERSON_SENSOR_REG_CALIBRATE_ID  = 0x04
PERSON_SENSOR_REG_PERSIST_IDS   = 0x05
PERSON_SENSOR_REG_ERASE_IDS     = 0x06
PERSON_SENSOR_REG_DEBUG_MODE    = 0x07

PERSON_SENSOR_MODE_STANDBY      = 0x00
PERSON_SENSOR_MODE_CONTINUOUS   = 0x01

# How many different faces the sensor can recognize.
PERSON_SENSOR_MAX_IDS_COUNT = 8

class QwiicPersonSensor(object):
    '''
    Class for the UseFul Person Sensor
    '''
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    def __init__(self, address=None, i2c_driver=None):
        '''
        Constructor

        :param address: The I2C address to use for the device
            If not provided, the default address is used
        :type address: int, optional
        :param i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        :type i2c_driver: I2CDriver, optional
        '''

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print('Unable to load I2C driver for this platform.')
                return
        else:
            self._i2c = i2c_driver

    def is_connected(self):
        '''
        Determines if this device is connected

        :return: `True` if connected, otherwise `False`
        :rtype: bool
        '''
        # Check if connected by seeing if an ACK is received
        if(self._i2c.isDeviceConnected(self.address) == False):
            return False

    def read(self):

        read_data = self._i2c.read_block(self.address, 0, PERSON_SENSOR_RESULT_BYTE_COUNT)

        offset = 0
        (pad1, pad2, payload_bytes) = struct.unpack_from(
            PERSON_SENSOR_I2C_HEADER_FORMAT, read_data, offset)
        offset = offset + PERSON_SENSOR_I2C_HEADER_BYTE_COUNT

        (num_faces) = struct.unpack_from('B', read_data, offset)
        num_faces = int(num_faces[0])
        offset = offset + 1

        faces = []
        for i in range(num_faces):
            (box_confidence, box_left, box_top, box_right, box_bottom, id_confidence, id,
            is_facing) = struct.unpack_from(PERSON_SENSOR_FACE_FORMAT, read_data, offset)
            offset = offset + PERSON_SENSOR_FACE_BYTE_COUNT
            face = {
                'box_confidence': box_confidence,
                'box_left': box_left,
                'box_top': box_top,
                'box_right': box_right,
                'box_bottom': box_bottom,
                'id_confidence': id_confidence,
                'id': id,
                'is_facing': is_facing,
            }
            faces.append(face)
        checksum = struct.unpack_from('H', read_data, offset)
        return faces

    def set_mode(self, mode):
        self._i2c.write_byte(self.address, PERSON_SENSOR_REG_MODE, int(mode))
        
    def set_debug_mode(self, mode):
        self._i2c.write_byte(self.address, PERSON_SENSOR_REG_DEBUG_MODE, int(mode))
        
    def set_id_detection_mode(self, enable_flag=True):
        self._i2c.write_byte(self.address, PERSON_SENSOR_REG_ENABLE_ID, int(enable_flag))

    def trigger_single_shot(self):
        self._i2c.write_byte(self.address, PERSON_SENSOR_REG_SINGLE_SHOT, 0)
        
    def persist_ids(self, enable_flag=True):
        self._i2c.write_byte(self.address, PERSON_SENSOR_REG_PERSIST_IDS, int(enable_flag))

    def erase_ids(self):
        self._i2c.write_byte(self.address, PERSON_SENSOR_REG_ERASE_IDS, 0)
        
    def calibrate(self, id_slot):
        if id_slot < PERSON_SENSOR_MAX_IDS_COUNT:
            self._i2c.write_byte(self.address, PERSON_SENSOR_REG_CALIBRATE_ID, id_slot)
        else:
            print( 'Invalid calibration slot: %d, must be less than %d' % (id_slot,PERSON_SENSOR_MAX_IDS_COUNT) )

if __name__ == '__main__':

    person_sensor = QwiicPersonSensor()

    if not person_sensor.is_connected():
        print( 'Could not connect to Person Sensor!' )
    else:
        person_sensor.set_id_detection_mode(True)
        while True:
            try:
                faces = person_sensor.read()
                for face in faces:
                    print('Faces: %s' % face )
                    if face['id_confidence'] > 50:
                        print( 'Welcome Back %d!' % face['id'] )
                    else:
                        print( 'Who Are You?' )
                        person_sensor.calibrate(1)
                        print( 'Calibration Done!' )
                time.sleep(1)
            except (KeyboardInterrupt, SystemExit) as exErr:
                print('\nDone')
                sys.exit(0)        
