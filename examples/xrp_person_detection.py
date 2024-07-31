from XRPLib.defaults import *
import time

from xrp_config import read_config
from Qwiic.qwiic_person_sensor import QwiicPersonSensor

def find_user(users, face):
    for user in users:
        if face['id'] == user['id']:
            return user
    return None


if __name__ == '__main__':
    config = read_config(section='person_sensor')
    users = config.get('users',list())

    person_sensor = QwiicPersonSensor()

    if not person_sensor.is_connected():
        print( 'Could not connect to Person Sensor!' )
    else:
        print( 'Scanning for known people...' )
        person_sensor.set_id_detection_mode(True)
        while True:
            try:
                faces = person_sensor.read()
                for face in faces:
                    print( 'Face: %s' % face )
                    if face['id_confidence'] > 50:
                        user = find_user(users, face)
                        if user:
                            print( 'Welcome Back %s!' % user['name'] )
                        else:
                            print( 'User %d Is Not Configured' % face['id'] )
                    else:
                        print( 'Unknown User' )
                        print( 'Press User Button To Store User')
                        button_pressed = False
                        attempts = 0
                        while not button_pressed:
                            if board.is_button_pressed():
                                button_pressed = True
                                break
                            else: 
                                time.sleep(0.1)
                                attempts += 1
                                if attempts == 50:
                                    break
                        if button_pressed:
                            id = 1
                            print( 'Storing User For ID: %d' % id )
                            person_sensor.calibrate(id)
                            print( 'Calibration Done!' )
                        else:
                            print( 'User Not Stored')
                time.sleep(1)
            except (KeyboardInterrupt, SystemExit) as exErr:
                print("\nDone")
                sys.exit(0)        
