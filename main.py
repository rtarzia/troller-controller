import RPi.GPIO as GPIO
import time
import threading

dc       = 40
exiting  = False

def pwm_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    pwm = GPIO.PWM(12, 100)
    return pwm

def pwm_loop(pwm, dc_change_event):
    current_dc = 0

    pwm.start(current_dc)

    while current_dc < dc:
        current_dc += 1
        pwm.ChangeDutyCycle(current_dc)
        time.sleep(0.05)

    while True:
        dc_change_event.wait()

        if exiting: break

        if dc > current_dc:
            while current_dc < dc:
                current_dc += 1
                pwm.ChangeDutyCycle(current_dc)
                time.sleep(0.03)
        elif dc < current_dc:
            while current_dc > dc:
                current_dc -= 1
                pwm.ChangeDutyCycle(current_dc)
                time.sleep(0.03)
        
        dc_change_event.clear()

    while current_dc > 0:
        current_dc -= 1
        pwm.ChangeDutyCycle(current_dc)
        time.sleep(0.02)

def pwm_cleanup():
    pwm.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    dc_change_event = threading.Event()
    dc_change_event.set()

    pwm = pwm_setup()

    pwm_thread = threading.Thread(target=pwm_loop, args=(pwm, dc_change_event))
    pwm_thread.start()
    
    try:
        print('starting..')
        while True:
            new_dc = int(input('input duty cycle: '))
            if new_dc >= 0 and new_dc <= 100:
                dc = new_dc
                dc_change_event.set()
            else:
                print('bad input')
    except KeyboardInterrupt:
        dc_change_event.set()
        exiting = True
        print('\nexiting..')

    pwm_thread.join()
    pwm_cleanup()


    