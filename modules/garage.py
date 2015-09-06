try:
    import RPi.GPIO as GPIO
except:
    print 'Notice: Not Connect To A Pi.'
import time


class Garage:
    __pinList = [4]

    def __init__(self, pinList):
        try:
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Warning: Could Not Init Garage.'

        self.__pinList = pinList

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
            GPIO.setup(22, GPIO.IN)
            counter = 0
            lastState = GPIO.input(22)
            while True:
                time.sleep(.0002)
                state = GPIO.input(22)
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
