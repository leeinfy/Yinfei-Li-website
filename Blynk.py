import RPi.GPIO as GPIO
import blynklib
import random
from gpiozero import LED
import time

BLYNK_AUTH = 'B8ltEMSYdnD9pn0rWOC_vC4oXMNBDecF'

# initialize blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

motorAin1 = 17
motorAin2 = 27
motorAen = 22
led = LED(4)
speed = 0

motorState = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorAin1,GPIO.OUT)
GPIO.setup(motorAin2,GPIO.OUT)
GPIO.setup(motorAen,GPIO.OUT)
p = GPIO.PWM(motorAen, 1000)
p.start(0)


# register handler for virtual pin V0 write event
@blynk.handle_event('write V0') # on and off switch
def write_virtual_pin_handler(pin, value):
    switch = (format(value[0]))
    if switch == "0":
        GPIO.output(motorAin1, 0)
        GPIO.output(motorAin2, 0)
        led.value = 0
    elif switch == "1":
        GPIO.output(motorAin1, 1)
        GPIO.output(motorAin2, 0)
        led.value = 1
        
# register handler for virtual pin V2 write event       
@blynk.handle_event('write V2') # motor speed
def write_virtual_pin_handler(pin, value):
    sliderValue = int(format(value[0]))
    global speed
    speed = sliderValue
    p.ChangeDutyCycle(speed)

# register handler for virtual pin V1 write event
@blynk.handle_event('write V1') #change direction of motor
def write_virtual_pin_handler(pin, value):
    motorReverse = (format(value[0]))
    if  motorReverse == "1":
        GPIO.output(motorAin1, 0)
        GPIO.output(motorAin2, 1)
        led.value = 1
    elif motorReverse == "0":
        GPIO.output(motorAin1, 1)
        GPIO.output(motorAin2, 0)
        led.value = 1

@blynk.handle_event('read V3')
def read_virtual_pin_handler(pin):
    blynk.virtual_write(pin, speed)

while True:
    blynk.run()
