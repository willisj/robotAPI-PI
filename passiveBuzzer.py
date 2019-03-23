# 
#		Passive buzzer 			   Pi 
#			VCC ----------------- 3.3V
#			GND ------------------ GND
#			SIG ---------------- Pin 11

import RPi.GPIO as GPIO
import time

class PassiveBuzzerController:

    def __init__(self, buzzerPin=11):
        self.pitch = 0
        self.mode = -1
        self.buzzerPin = buzzerPin
        GPIO.setmode(GPIO.BOARD)		                # Numbers GPIOs by physical location
        GPIO.setup(buzzerPin, GPIO.OUT)	                        # Set pins' mode is output
        self.buzz = GPIO.PWM(buzzerPin, 500)	                # 440 is initial frequency.


    def getIntervalMod(self, interval):
        return int(int(time.time() * 1000.0) / int(interval * 1000.0))

    def setModeContinuous(self, pitch, duration):
        self.mode = 0
        self.buzz.ChangeFrequency(pitch)	
        self.contStop = time.time() + duration

    def setModeSiren(self):
        self.mode = 1
        self.pitch = 0

    def setModeTweet(self, startPitch, duration):
        self.mode = 2
        self.pitch = startPitch
        self.tweetStop = time.time() + duration
        self.lastMod = self.getIntervalMod(0.01)

    def tick(self):
        if self.mode == 0 and self.contStop <= time.time():
            self.stop()
        elif self.mode == 1:
            if(self.pitch == 0 and (int(time.time()*6) % 2) == 0 ):
                self.buzz.ChangeFrequency(500)	
                self.pitch = 1
            elif self.pitch == 1 and (int(time.time()*6) % 2) == 1 :
                self.buzz.ChangeFrequency(300)	
                self.pitch = 0
        if self.mode == 2:

            if self.tweetStop >= time.time():
                curMod = self.getIntervalMod(0.01)
                if not self.lastMod == curMod:
                    self.lastMod =  curMod
                    self.pitch = self.pitch + 10
                    self.buzz.ChangeFrequency(self.pitch)	
            else:
                self.stop()

    def start(self):
        self.buzz.start(50)

    def stop(self):
        self.mode = -1
	self.buzz.stop()					# Stop the buzzer

    def getMode(self):
        return self.mode

    def destroy(self):
	self.buzz.stop()					# Stop the buzzer
	GPIO.output(self.buzzerPin, 1)		# Set Buzzer pin to High
	GPIO.cleanup()				# Release resource

# debug program
if __name__ == '__main__':	
    bCont = PassiveBuzzerController()
    try:
        bCont.start()
        bCont.setModeTweet(400, 1.0)
        while 1:
            bCont.tick()
            time.sleep(0.01)
    except KeyboardInterrupt:
        bCont.destroy()
