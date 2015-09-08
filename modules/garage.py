try:
    import RPi.GPIO as GPIO
except:
    print 'Notice: Not Connect To A Pi.'
import time


class Garage:
    __pinList = None
    __inputPin = None

    def __init__(self, pinList, inputPin):
        self.__pinList = pinList
        self.__inputPin = inputPin

        try:
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Warning: Could Not Init Garage.'

    # Toggle Door
    def toggleDoor(self):
        try:
            for pin in self.__pinList:
                GPIO.output(pin, GPIO.LOW)

            time.sleep(.2)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Warning: Failed To Toggle Door.'

    # Cleanup PI
    def cleanupRelay(self):
        try:
            for pin in self.__pinList:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.HIGH)
        except:
            print 'Warning: Failed To Clean Up.'

    # Door status
    # True: open
    # False: closed
    # None: In Motion
    # error: No GPIO
    def doorStatus(self):
        try:
            GPIO.setup(self.__inputPin, GPIO.IN)
            counter = 0
            lastState = GPIO.input(self.__inputPin)
            while True:
                time.sleep(.0002)
                state = GPIO.input(self.__inputPin)
                if state == lastState:
                    counter = counter + 1
                    if counter >= 200:
                        if state == 1:
                            return True
                        else:
                            return False
                else:
                    return None
        except:
            return 'error'
