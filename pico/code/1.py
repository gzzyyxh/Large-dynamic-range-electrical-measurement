
# 树莓派 Pico RGB Blink
# rgb-blink.py
 
# RED LED - Pico GPIO 10 - Pin 14
# GREEN LED - Pico GPIO 11 - Pin 15
# BLUE LED - Pico GPIO 14 - Pin 19
 
# DroneBot Workshop 2021
# https://dronebotworkshop.com
 
 
import machine
import utime
 
led = machine.Pin(25, machine.Pin.OUT)
 
while True:
    
    led.value(1) 
    utime.sleep(0.05)

    led.value(0)
    utime.sleep(0.05)