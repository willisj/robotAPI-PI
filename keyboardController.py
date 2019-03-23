import RPi.GPIO as GPIO
import time
import random
import Queue
import threading
import os
from getch import getKey


class KeyboardMonitor:

    def __init__(self):
        # Create the key queue
        self.keyQueue = Queue.Queue();

        # Set the state to running
        self.running = True

        # Start the background thread
        thread = threading.Thread(target=self.monitorFunction, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()    

    # Function called in it's own thread
    def monitorFunction(self):
        try:
            while(self.running):
                c = getKey()
                self.keyQueue.put(c)
        except KeyboardInterrupt:
            pass

    # Get the next key from the queue 
    # Client function
    def getNext(self):
        if self.keyQueue.empty():
            return None
        else:
            return self.keyQueue.get()

    # Stop the background thread
    # Client function
    def stop(self):
        self.running = False

if __name__ == '__main__':		# Program start from here
    kbm = KeyboardMonitor()
    while 1:
        key = kbm.getNext()
        if key: 
            print("Key",ord(key))

            if ord(key) == ord('q'):
                kbm.stop()
                os.system("reset")
                print ("Exiting")
                break;

        time.sleep(0.1)
