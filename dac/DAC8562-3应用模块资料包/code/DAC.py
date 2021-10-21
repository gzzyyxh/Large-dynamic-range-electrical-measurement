from machine import SPI, Pin
import utime

PERIOD_US = 1000
VOLTAGE = 5

OUTA = 0x18
OUTB = 0x19
Reset_All_Regs = 0x280001
POWERUP_DAC_A_B = 0x200003
ENABLE_INTERNAL = 0x380001

Square = {"VH": 0, "VL": 0, "TD": 0, "TR": 0, "TF": 0, "PW": 0, "PER": 0}

MISO = Pin(0, Pin.IN)
SYNC = CSn = Pin(1, Pin.OUT)
SCLK = Pin(2, Pin.OUT, Pin.PULL_UP)
DIN = MOSI = Pin(3, Pin.OUT, Pin.PULL_UP)
CLR = Pin(8, Pin.OUT)
LDAC = Pin(9, Pin.OUT)

spi = SPI(0, baudrate = 20000000, polarity = 0, phase = 1, bits = 8, firstbit = SPI.MSB, sck = Pin(2), mosi = Pin(3), miso = Pin(0))


def get_buf(command, data):
    DIN = (command << 16) | data
    buf = bytearray()
    for i in range(0, 3):
        din = DIN & 0xff0000
        din = din >> 16
        # print(hex(din))
        buf.append(din)
        DIN = DIN << 8
    return buf

def DAC_writebuf(buf):
    # SYNC.value(1)
    SYNC.value(0)
    spi.write(buf)
    SYNC.value(1)
    # LDAC.value(0)
    # LDAC.value(1)


def DAC_write(command, data):
    SYNC.value(1)
    # utime.sleep_us(1)    # delay 1 us
    SYNC.value(0)
    SCLK.value(0)

    DIN = (command << 16) | data
    buf = bytearray()
    for i in range(0, 3):
        din = DIN & 0xff0000
        din = din >> 16
        # print(hex(din))
        buf.append(din)
        DIN = DIN << 8
    spi.write(buf)
    # utime.sleep_us(1)
    SYNC.value(1)
    LDAC.value(0)
    # utime.sleep_us(1)
    LDAC.value(1)

def Voltage2DIN(vout, vref = 2.5, gain = 2):
    # print(vout / (vref * gain) * pow(2, 16))
    # print(int(vout / (vref * gain) * pow(2, 16)))
    DIN = int((vout/4.17 + 2.5) / (vref * gain) * pow(2, 16))
    return DIN

def DAC_SetVoltage():
    global PERIOD_US, OUTA, OUTB, VOLTAGE, Reset_All_Regs, POWERUP_DAC_A_B, ENABLE_INTERNAL
    CLR.value(0)
    LDAC.value(1)
    DAC_write(Reset_All_Regs >> 16, Reset_All_Regs & 0xffff)   # Reset_All_Regs    101-000-0000000000000001
    DAC_write(POWERUP_DAC_A_B >> 16, POWERUP_DAC_A_B & 0xffff)   # POWERUP_DAC_A_B   100-000-0000000000000011
    DAC_write(ENABLE_INTERNAL >> 16, ENABLE_INTERNAL & 0xffff)   # ENABLE_INTERNAL   111-000-0000000000000001

    buf_1 = get_buf(OUTA, Voltage2DIN(float(VOLTAGE)))
    buf_2 = get_buf(OUTA, Voltage2DIN(float(VOLTAGE * -1)))

    while True:
        # start = utime.ticks_us()
        DAC_writebuf(buf_1)
        # utime.sleep_us(int(PERIOD_US / 2) - 20 - (utime.ticks_us() - start))  # 20us
        # start = utime.ticks_us()
        # DAC_writebuf(buf_2)
        # utime.sleep_us(int(PERIOD_US / 2) - 20 - (utime.ticks_us() - start))  # 20us

DAC_SetVoltage()