from machine import Pin, PWM
import utime



def main():
    servo_180=PWM(Pin(18))
    servo_180.freq(50)
    
    
    while True:
        angulo=float(input('Ingrese su angulo'))
        if angulo>=0 and angulo<=180:
            duty=int(500000 + (angulo / 180) * 2000000)
            servo_180.duty_ns(duty)
if __name__=='__main__':
    main()