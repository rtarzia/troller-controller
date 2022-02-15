import RPi.GPIO as GPIO
import time

SERVO_PIN   = 11

class Servo:

    def __init__(self, dc_change_event):
        self.duty_cycle       = 7.0
        self.exiting          = False
        self.dc_change_event  = dc_change_event

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        
        self.pwm = GPIO.PWM(SERVO_PIN, 50)
        self.pwm.start(self.duty_cycle)

    def change_duty_cycle(self, delta):
        new_duty_cycle = delta + self.duty_cycle
        if new_duty_cycle >= 2.0 and new_duty_cycle <= 12.0:
            self.duty_cycle = new_duty_cycle

        print('new dc: ' + str(new_duty_cycle))
        print('duty cycle: ' + str(self.duty_cycle))

    def loop(self):
        while True:
            self.dc_change_event.wait()

            if self.exiting: break

            self.pwm.ChangeDutyCycle(self.duty_cycle)

            self.dc_change_event.clear()
        
        self.pwm.ChangeDutyCycle(7.0)
        time.sleep(2)
        self.pwm.stop()

