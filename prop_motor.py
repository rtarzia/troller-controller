import RPi.GPIO as GPIO
import time

PROP_PIN = 12

class Prop:

    def __init__(self, dc_change_event):
        self.duty_cycle       = 0
        self.exiting          = False
        self.dc_change_event  = dc_change_event

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PROP_PIN, GPIO.OUT)
        
        self.pwm = GPIO.PWM(PROP_PIN, 100)
        self.pwm.start(self.duty_cycle)

    def loop(self):
        current_dc = 0

        while True:
            self.dc_change_event.wait()

            if self.exiting: break

            while current_dc != self.duty_cycle:
                current_dc = current_dc + 1 if current_dc < self.duty_cycle else current_dc - 1
                self.pwm.ChangeDutyCycle(current_dc)
                time.sleep(0.005)

            self.dc_change_event.clear()

        while self.duty_cycle > 0:
            self.duty_cycle -= 1
            self.pwm.ChangeDutyCycle(self.duty_cycle)
            time.sleep(0.01)

        self.pwm.stop()

