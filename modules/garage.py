try:
    import RPi.GPIO as GPIO
except:
    print 'Notice: Not Connect To A Pi.'
import time


class Garage:
    def __init__(self):
        try:
            pinList = [4]
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Notice: Not Connect To A Pi.'

    # TOGGLE FUNCTION
    def toggleDoor(self):
        try:
            for pin in self.pinList:
                GPIO.output(pin, GPIO.LOW)

            time.sleep(.2)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Notice: Not Connect To A Pi.'

    # Cleanup PI
    def cleanupRelay(self):
        try:
            for pin in self.pinList:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.HIGH)
        except:
            print 'Notice: Not Connect To A Pi.'
