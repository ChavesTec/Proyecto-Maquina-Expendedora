from machine import ADC, Pin, PWM
import socket
import network
from time import sleep, ticks_ms

# ====================================
# WIFI
# ====================================

SSID     = "Iphone 20 de Daniel"
PASSWORD = "Dansol1702"
PORT     = 1717

# ====================================
# POTENCIOMETRO
# ====================================

pot = ADC(26)

# ====================================
# LEDS NORMALES
# ====================================

led1 = Pin(15, Pin.OUT)
led2 = Pin(16, Pin.OUT)
led3 = Pin(17, Pin.OUT)

# ====================================
# LEDS AGOTADO(rojo)
# ====================================

led_agotado1 = Pin(21, Pin.OUT)
led_agotado2 = Pin(22, Pin.OUT)
led_agotado3 = Pin(27, Pin.OUT)

# ====================================
# BOTON
# ====================================

boton = Pin(14, Pin.IN, Pin.PULL_UP)

# ====================================
# LED MANTENIMIENTO
# ====================================

led_mantenimiento = Pin(28, Pin.OUT)

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
# INICIAR SERVOS
# ====================================

mover_servo(servo1, 0)
mover_servo(servo2, 0)
mover_servo(servo3, 0)

sleep(1)

# ====================================
# stock
# ====================================

stock = [9, 9, 9]

# ====================================
# WIFI
# ====================================

def conectar_wifi():

    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    wlan.connect(SSID, PASSWORD)

    print("Conectando a WiFi", end="")

    for _ in range(20):

        if wlan.isconnected():
            break

        print(".", end="")

        sleep(0.5)

    if wlan.isconnected():

        ip = wlan.ifconfig()[0]

        print("\nConectado! IP:", ip)

        return ip

    print("\nError de conexion")

    return None

# ====================================
# SERVIDOR TCP
# ====================================

def iniciar_servidor(ip):

    s = socket.socket()

    s.bind((ip, PORT))

    s.listen(1)

    s.setblocking(False)

    print(
        "Servidor listo en {}:{}".format(
            ip,
            PORT
        )
    )

    return s

ip = conectar_wifi()

servidor = iniciar_servidor(ip)

conn_actual = None

# ====================================
# ESTADO SERVO
# ====================================

servo_activo        = False
servo_obj           = None
servo_angulo_dest   = 0
servo_tiempo_inicio = 0

DURACION_SERVO = 3000

producto_actual = 1

# ====================================
# MODO MANTENIMIENTO
# ====================================

modo_mantenimiento = False
# ====================================
# LOOP PRINCIPAL
# ====================================

while True:

    ahora = ticks_ms()

    # =====================================
    # SERVIDOR TCP
    # =====================================

    try:

        if conn_actual is None:

            try:

                conn_actual, addr = servidor.accept()

                conn_actual.setblocking(False)

                print(
                    "Cliente conectado:",
                    addr
                )

            except:

                pass

        if conn_actual is not None:

            try:

                data = conn_actual.recv(1024)

                if data:

                    msg = data.decode().strip()

                    # =================================
                    # ENVIAR STOCK
                    # =================================

                    if msg == "STOCK":

                        respuesta = "{},{},{}\n".format(
                            stock[0],
                            stock[1],
                            stock[2]
                        )

                        conn_actual.send(
                            respuesta.encode()
                        )

                    # =================================
                    # MODO MANTENIMIENTO ON
                    # =================================

                    elif msg == "MANTENIMIENTO_ON":

                        modo_mantenimiento = True

                        led_mantenimiento.on()

                        print("Mantenimiento ACTIVADO")

                    # =================================
                    # MODO MANTENIMIENTO OFF
                    # =================================

                    elif msg == "MANTENIMIENTO_OFF":

                        modo_mantenimiento = False

                        led_mantenimiento.off()

                        print("Mantenimiento DESACTIVADO")

            except OSError:

                pass

            except Exception:

                conn_actual.close()

                conn_actual = None

    except Exception:

        pass

    # =====================================
    # MODO MANTENIMIENTO
    # =====================================

    if modo_mantenimiento:

        led1.off()
        led2.off()
        led3.off()

        led_agotado1.off()
        led_agotado2.off()
        led_agotado3.off()

        sleep(0.05)

        continue

    # =====================================
    # SERVO SIN SLEEP
    # =====================================

    if servo_activo:

        if ahora - servo_tiempo_inicio >= DURACION_SERVO:

            if servo_angulo_dest == 90:

                mover_servo(
                    servo_obj,
                    0
                )

                servo_angulo_dest = 0

                servo_tiempo_inicio = ahora

            else:

                servo_activo = False

                servo_obj = None

    # =====================================
    # POTENCIOMETRO
    # =====================================

    valor = pot.read_u16()

    # apagar LEDs normales
    led1.off()
    led2.off()
    led3.off()

    # apagar LEDs agotado
    led_agotado1.off()
    led_agotado2.off()
    led_agotado3.off()

    # =====================================
    # PRODUCTO 1
    # =====================================

    if valor < 22000:

        producto_actual = 1

        if stock[0] > 0:

            led1.on()

        else:

            led_agotado1.on()

        mostrar_numero(stock[0])

    # =====================================
    # PRODUCTO 2
    # =====================================

    elif valor < 44000:

        producto_actual = 2

        if stock[1] > 0:

            led2.on()

        else:

            led_agotado2.on()

        mostrar_numero(stock[1])

    # =====================================
    # PRODUCTO 3
    # =====================================

    else:

        producto_actual = 3

        if stock[2] > 0:

            led3.on()

        else:

            led_agotado3.on()

        mostrar_numero(stock[2])

    # =====================================
    # BOTON FISICO
    # =====================================

    if boton.value() == 0 and not servo_activo:

        idx = producto_actual - 1

        if stock[idx] > 0:

            stock[idx] -= 1

            servos = [
                servo1,
                servo2,
                servo3
            ]

            servo_obj = servos[idx]

            mover_servo(
                servo_obj,
                90
            )

            servo_angulo_dest = 90

            servo_tiempo_inicio = ahora

            servo_activo = True

        sleep(0.3)

    sleep(0.05)
