from machine import ADC, Pin, PWM
from time import sleep

# ====================================
# POTENCIOMETRO
# ====================================

pot = ADC(26)

# ====================================
# LEDS
# ====================================

led1 = Pin(15, Pin.OUT)
led2 = Pin(16, Pin.OUT)
led3 = Pin(17, Pin.OUT)

# ====================================
# BOTON
# ====================================

boton = Pin(14, Pin.IN, Pin.PULL_UP)

# ====================================
# SERVOS
# ====================================

servo1 = PWM(Pin(18))
servo2 = PWM(Pin(19))
servo3 = PWM(Pin(20))

servo1.freq(50)
servo2.freq(50)
servo3.freq(50)

# ====================================
# DISPLAY 7 SEGMENTOS
# 5161BS - ANODO COMUN
# ====================================

a = Pin(0, Pin.OUT)
b = Pin(1, Pin.OUT)
c = Pin(2, Pin.OUT)
d = Pin(3, Pin.OUT)
e = Pin(4, Pin.OUT)
f = Pin(5, Pin.OUT)
g = Pin(6, Pin.OUT)

segmentos = [a, b, c, d, e, f, g]

# ====================================
# NUMEROS DISPLAY
# ANODO COMUN
# 0 = encender
# 1 = apagar
# ====================================

numeros = {

    0: [0,0,0,0,0,0,1],
    1: [1,0,0,1,1,1,1],
    2: [0,0,1,0,0,1,0],
    3: [0,0,0,0,1,1,0],
    4: [1,0,0,1,1,0,0],
    5: [0,1,0,0,1,0,0],
    6: [0,1,0,0,0,0,0],
    7: [0,0,0,1,1,1,1],
    8: [0,0,0,0,0,0,0],
    9: [0,0,0,0,1,0,0]
}

# ====================================
# FUNCION DISPLAY
# ====================================

def mostrar_numero(numero):

    patron = numeros[numero]

    for i in range(7):
        segmentos[i].value(patron[i])

# ====================================
# FUNCION SERVO
# ====================================

def mover_servo(servo, angulo):

    duty = int(1000 + (angulo / 180) * 8000)
    servo.duty_u16(duty)

# ====================================
# INICIAR SERVOS EN 0°
# ====================================

mover_servo(servo1, 0)
mover_servo(servo2, 0)
mover_servo(servo3, 0)

sleep(1)

# ====================================
# STOCK PRODUCTOS
# ====================================

stock1 = 9
stock2 = 9
stock3 = 9

# ====================================
# PRODUCTO ACTUAL
# ====================================

producto_actual = 1

# ====================================
# LOOP PRINCIPAL
# ====================================

while True:

    valor = pot.read_u16()

    # apagar LEDs
    led1.off()
    led2.off()
    led3.off()

    # ====================================
    # SELECCION PRODUCTO
    # ====================================

    if valor < 22000:

        led1.on()
        producto_actual = 1

        mostrar_numero(stock1)

    elif valor < 44000:

        led2.on()
        producto_actual = 2

        mostrar_numero(stock2)

    else:

        led3.on()
        producto_actual = 3

        mostrar_numero(stock3)

    # ====================================
    # BOTON PRESIONADO
    # ====================================

    if boton.value() == 0:

        # ================================
        # PRODUCTO 1
        # ================================

        if producto_actual == 1 and stock1 > 0:

            stock1 -= 1

            mover_servo(servo1, 90)
            sleep(1)

            mover_servo(servo1, 0)
            sleep(1)

        # ================================
        # PRODUCTO 2
        # ================================

        elif producto_actual == 2 and stock2 > 0:

            stock2 -= 1

            mover_servo(servo2, 90)
            sleep(1)

            mover_servo(servo2, 0)
            sleep(1)

        # ================================
        # PRODUCTO 3
        # ================================

        elif producto_actual == 3 and stock3 > 0:

            stock3 -= 1

            mover_servo(servo3, 90)
            sleep(1)

            mover_servo(servo3, 0)
            sleep(1)

        sleep(0.5)

    sleep(0.1)