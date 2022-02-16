import RPi.GPIO as GPIO
import time
import threading
import bluetooth
from servo_motor import Servo
from prop_motor import Prop

if __name__ == '__main__':
    target_name = 'ESP32test'
    target_address = None

    nearby_devices = bluetooth.discover_devices()

    for baddr in nearby_devices:
        if target_name in bluetooth.lookup_name(baddr):
            print('connecting to: ' + bluetooth.lookup_name(baddr) + ' at: ' + baddr)
            target_address = baddr
            break

    BTsocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    BTsocket.connect((target_address, 1))
    BTsocket.send(b'ack')

    # setup servo
    servo_event = threading.Event()
    servo = Servo(servo_event)
    servo_thread = threading.Thread(target=Servo.loop, args=(servo,))
    servo_thread.start()
    servo_event.set()

    # setup prop
    prop_event = threading.Event()
    prop = Prop(prop_event)
    prop_thread = threading.Thread(target=Prop.loop, args=(prop,))
    prop_thread.start()
    prop_event.set()

    # main loop
    print('starting..')
    while True:
        recval = BTsocket.recv(128).decode()
        print(recval)

        if 'e' in recval:
            servo.exiting = prop.exiting = exiting = True
            servo_event.set()
            prop_event.set()
            print('\nexiting..')
            break

        elif recval[0] == 'p':
            try:
                prop.duty_cycle = int(recval[1:])
            except:
                print('exception: bad int for prop dc')

            prop_event.set()

        elif recval[0] == 's':
            duty_cycle_delta = -0.25 if recval[1] == 'l' else 0.25
            print('duty cycle delta: ' + str(duty_cycle_delta))
            servo.change_duty_cycle(duty_cycle_delta)
            servo_event.set()        

    # cleanup
    servo_thread.join()
    prop_thread.join()
    GPIO.cleanup()
    BTsocket.close()    