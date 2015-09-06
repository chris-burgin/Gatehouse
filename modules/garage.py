try:
    import RPi.GPIO as GPIO
except:
    print 'Notice: Not Connect To A Pi.'
import time


class Garage:
    pinList = [4]

    def __init__(self):
        try:
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Warning: Could Not Init Garage.'

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
            print 'Warning: Failed To Toggle Door.'

    # Cleanup PI
    def cleanupRelay(self):
        try:
            for pin in self.pinList:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.HIGH)
        except:
            print 'Warning: Failed To Clean Up.'

    # Door status
    # True: open
    # False: closed
    # None: Timeout/Error
    def doorStatus(self):
        try:
            GPIO.setup(22, GPIO.IN)
            counter = 0
            lastState = GPIO.input(22)
            while counter <= 100:
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
            return None
