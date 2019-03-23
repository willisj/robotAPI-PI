import RPi.GPIO as GPIO
import time


# Hardware PWM is available on pins 12, 13, 18, 19 
# There are only 2 channels split between the 4 pins
class ServoWrapper:
    
    # Prepare the values for this servo (constraints)
    def __init__(self, pin, minDC = 2.5, maxDC = 12.5):
        # Set the state to 'STOPPED'
        self.stopCalled = True

        # The pin number for this servo
        self.pin = pin

        # Set constraints (DC = Duty Cycle)
        self.minDC = minDC
        self.maxDC = maxDC
        self.midDC = minDC + (( maxDC - minDC) / 2.0)

        # Default Duty Cycle 
        self.targetDC = self.midDC

    # Convert a percentage value to a Duty Cycle value
    def percentToDC(self, percent):
        return (( self.maxDC - self.minDC) / 100.0) * percent

    # Correct the current DC value against the constraints
    def correctDC(self):
        if self.targetDC > self.maxDC:
            self.targetDC =  self.maxDC
        elif self.targetDC < self.minDC:
            self.targetDC =  self.minDC

    # Start up the PWM signal to the servo
    def start(self):
        if self.stopCalled:
            # Set the state to 'NOT STOPPED'
            self.stopCalled = False

            # PWM prep
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.pin, 50)

            # Check constraints
            self.correctDC()

            # Start it up
            self.pwm.start(self.midDC)
            self.pwm.ChangeDutyCycle(self.targetDC)

    # Stop the servo control
    def stop(self):
        # Check the state first
        if not self.stopCalled:
            # update state
            self.stopCalled = True

            # stop the servo PWM signal
            self.pwm.stop();
            GPIO.cleanup()

    # Move the servo to a specific angle given by percentage
    def move(self, percent):
        # Check the state first
        if not self.stopCalled:
            # Update the TARGET duty cycle 
            self.targetDC = self.percentToDC(percent)

            # Check the constraints
            self.correctDC()

            # Update the DC
            self.pwm.ChangeDutyCycle(self.targetDC)

    # Move the servo to a angle relative to it's current position IE +5% 
    def offset(self, percent):
        # Check the state first
        if not self.stopCalled:
            # Update the TARGET duty cycle 
            self.targetDC = self.targetDC + self.percentToDC(percent)

            # Check the constraints
            self.correctDC()

            # Update the DC
            self.pwm.ChangeDutyCycle(self.targetDC)


