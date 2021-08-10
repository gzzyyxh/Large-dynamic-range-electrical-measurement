import machine
import utime

out = machine.Pin(14, machine.Pin.OUT)
while True:
    
    out.value(1) 
    utime.sleep(0.05)

    out.value(0)
    utime.sleep(0.05)