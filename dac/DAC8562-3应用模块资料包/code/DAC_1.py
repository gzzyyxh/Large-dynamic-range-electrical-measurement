from machine import SPI, Pin
import ubinascii
import utime
import math

MISO = Pin(0, Pin.IN)
SYNC = CSn = Pin(1, Pin.OUT)
SCLK = Pin(2, Pin.OUT)
DIN = MOSI = Pin(3, Pin.OUT)
CLR = Pin(8, Pin.OUT)
LDAC = Pin(9, Pin.OUT)

def DAC8562_WRITE(cmd, data):
    SYNC.value(1)
    utime.sleep_us(1)
    SYNC.value(0)
    SCLK.value(0)
    for i in range(0, 8):
        if (cmd & 0x80) == 0x80:
            DIN.value(1)
        else:
            DIN.value(0)
        utime.sleep_us(1)
        SCLK.value(1)
        utime.sleep_us(1)
        cmd = cmd << 1
        SCLK.value(0)
        utime.sleep_us(1)

    for i in range(0, 16):
        if (data & 0x8000) == 0x8000:
            DIN.value(1)
        else:
            DIN.value(0)
        utime.sleep_us(1)
        SCLK.value(1)
        utime.sleep_us(1)
        data = data << 1
        SCLK.value(0)
        utime.sleep_us(1)
    SYNC.value(1)
    LDAC.value(0)
    utime.sleep_us(1)
    LDAC.value(1)

def Voltage2DIN(vout, vref = 2.5, gain = 2):
    # print(vout / (vref * gain) * pow(2, 16))
    # print(int(vout / (vref * gain) * pow(2, 16)))
    DIN = int((vout/4.17 + 2.5) / (vref * gain) * pow(2, 16))
    return DIN

def main():
    CLR.value(0)
    LDAC.value(1)
    DAC8562_WRITE(0X28, 0X0001)   # Reset_All_Regs    101-000-0000000000000001
    DAC8562_WRITE(0X20, 0X0003)   # POWERUP_DAC_A_B   100-000-0000000000000011
    DAC8562_WRITE(0X38, 0X0001)   # ENABLE_INTERNAL   111-000-0000000000000001

    while True:
        # v = input("input v:")
        # utime.sleep_us(1)
        DAC8562_WRITE(0x18, Voltage2DIN(float(5)))
        # DAC8562_WRITE(0x18, 0x0)
        # utime.sleep_ms(1)
        DAC8562_WRITE(0x18, Voltage2DIN(float(-5)))
        # utime.sleep_ms(1)

main()