import time
import os
from servo import ServoWrapper

from keyboardController import KeyboardMonitor
from passiveBuzzer import PassiveBuzzerController

#12
#13
#18
#19

class RoaverModel:

    # Setup the deps
    def __init__(self):
        # Buzzer Controller
        self.buzzerCtrl = PassiveBuzzerController()

        # Keyboard Input monitor
        # This messes with the terminal
        # you might have to give 'reset' in bash
        self.kbm = KeyboardMonitor()

        # Servo Controllers
        self.pitch = ServoWrapper(12)
        self.yaw = ServoWrapper(13)

        # Local state of the camera controls
        self.cameraState = False

        # Exit flag
        self.running = True

    # Clean up deps
    def cleanup(self):
        self.running = False
        self.kbm.stop()
        self.pitch.stop()
        self.yaw.stop()
        os.system("reset")

    def run(self):

        # Main input loop
        while self.running:

            # Get the key 
            key = self.kbm.getNext()
            if key:     # NULL CHECK

                ## #####################
                ## EXIT KEY
                if ord(key) == ord('q'):
                    self.cleanup()
                    break;

                ## #####################
                ## BUZZER RELATED 
                elif ord(key) == ord('h'):  # Low Horn
                    self.buzzerCtrl.setModeContinuous(400, 0.4)
                    self.buzzerCtrl.start()

                elif ord(key) == ord('j'):  # High Horn
                    self.buzzerCtrl.setModeContinuous(900, 0.4)
                    self.buzzerCtrl.start()

                elif ord(key) == ord('k'):  # Siren
                    self.buzzerCtrl.setModeSiren()
                    self.buzzerCtrl.start()

                elif ord(key) == ord('l'):  # Siren
                    self.buzzerCtrl.setModeTweet(300,0.75)
                    self.buzzerCtrl.start()

                elif ord(key) == ord('n'):  # Stop sound
                    self.buzzerCtrl.stop()

                ## #####################
                ## CAMERA CONTROL

                elif ord(key) == ord('c'):  # Toggle Camera
                    if self.cameraState: 
                        self.cameraState = False
                        # This is broken, can't re-start
                        #self.pitch.stop()
                        #self.yaw.stop()
                    else :
                        self.cameraState = True
                        self.pitch.start()
                        self.yaw.start()

                elif ord(key) == ord('w'):  # UP/FW
                    self.pitch.offset(5.0)
                elif ord(key) == ord('s'):  # UP/FW
                    self.pitch.offset(-5.0)
                elif ord(key) == ord('a'):  # UP/FW
                    self.yaw.offset(5)
                elif ord(key) == ord('d'):  # UP/FW
                    self.yaw.offset(-5)

            # Frequency of the control loop
            time.sleep(0.01)

            # Allow the buzzer to update if needed
            self.buzzerCtrl.tick()

        print ("Exiting")


# start it up
r = RoaverModel()
r.run()
