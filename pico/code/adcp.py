import machine
import utime

from machine import UART
from machine import Pin

uart0 = UART(0, baudrate = 115200, bits=8, parity = None, stop = 1)
uart1 = UART(1, baudrate = 115200, bits=8, parity = None, stop = 1)

while uart1.any() > 0:
    data = uart1.read()
    utime.sleep(1)
    uart1.write(data)

# sensor_temp = machine.ADC(4)
# ad0=machine.ADC(0)
# ad1=machine.ADC(1)
# ad2=machine.ADC(2)

# conversion_factor = 3.3 / (65535)
# while True:
#     reading = sensor_temp.read_u16() * conversion_factor
#     temperature = 27 - (reading - 0.706)/0.001721
#     print(temperature,ad0.read_u16(),ad1.read_u16(),ad2.read_u16())

#     uart.write("/*temp,%3.2f,%4d*/"%(temperature,ad0.read_u16()))
#     utime.sleep(1)