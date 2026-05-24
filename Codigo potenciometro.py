from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(18))
servo.freq(50)

while True:

    # izquierda
    servo.duty_u16(1000)
    sleep(1)

    # centro
    servo.duty_u16(5000)
    sleep(1)

    # derecha
    servo.duty_u16(9000)
    sleep(1)