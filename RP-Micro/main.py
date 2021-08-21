from machine import UART, Pin
import utime

import machine

led = Pin(25, Pin.OUT)
count = 0;

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
aux = Pin(2, Pin.IN)
m0 = Pin(3, Pin.OUT)
m1 = Pin(4, Pin.OUT)

def read_temperature():
    reading = sensor_temp.read_u16() * conversion_factor 
    return 27 - (reading - 0.706)/0.001721

def send_temperature_by_lorawan():
    global count
    temperature_celsius = read_temperature()

    # wait until aux is HIGH
    while aux.value() == 0:
        utime.sleep(0.3)

    utime.sleep(0.002)
    # print("Sent temperature: {0:05}T{1:.2f}".format(count, temperature_celsius).encode('ascii'))
    uart0.write("{0:05}T{1:.2f}".format(count, temperature_celsius).encode('ascii'))
    

    count += 1

while True:
    led.value(True)
    send_temperature_by_lorawan()
    led.value(False)
    utime.sleep(3)
