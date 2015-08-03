# import RPi.GPIO as GPIO


class Garage:
    def __init__(self):
        pinList = [4]
        # GPIO.setmode(GPIO.BCM)
        # cleanupRelay


    # TOGGLE FUNCTION
    def toggleDoor(self):
        GPIO.output(4, GPIO.LOW)
        time.sleep(.2)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        self.cleanupRelay()


    # Cleanup PI
    def cleanupRelay(self):
        for i in self.pinList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)
