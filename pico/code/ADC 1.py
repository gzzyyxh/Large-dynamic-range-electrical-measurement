from machine import SPI, Pin, Timer, UART
import ubinascii
import utime
import _thread
import sys

REG = {
    'COMMS': 0x00,
    'STATUS': 0x00,
    'ADCMODE': 0x01,
    'IFMODE': 0x02,
    'REGCHECK': 0x03,
    'DATA': 0x04,
    'GPIOCON': 0x06,
    'ID': 0x07,

    'CH0': 0x10,
    'CH1': 0x11,
    'CH2': 0x12,
    'CH3': 0x13,

    'SETUPCON0': 0x20,
    'SETUPCON1': 0x21,
    'SETUPCON2': 0x22,
    'SETUPCON3': 0x23,

    'FILTCON0': 0x28,
    'FILTCON1': 0x29,
    'FILTCON2': 0x2A,
    'FILTCON3': 0x2B,

    'OFFSET0': 0x30,
    'OFFSET1': 0x31,
    'OFFSET2': 0x32,
    'OFFSET3': 0x33,

    'GAIN0': 0x38,
    'GAIN1': 0x39,
    'GAIN2': 0x3A,
    'GAIN3': 0x3B
}

reglist = {
    'COMMS': 'Communication register',
    'STATUS': 'status register',
    'ADCMODE': 'ADCmode register',
    'IFMODE': 'Interface mode register',
    'REGCHECK': 'reg-check register',
    'DATA': 'data register',
    'GPIOCON': 'gpio configuration register',
    'ID': 'id register',

    'CH0': 'channel0 register',
    'CH1': 'channel1 register',
    'CH2': 'channel2 register',
    'CH3': 'channel3 register',

    'SETUPCON0': 'setup0 configuration register',
    'SETUPCON1': 'setup1 configuration register',
    'SETUPCON2': 'setup2 configuration register',
    'SETUPCON3': 'setup3 configuration register',

    'FILTCON0': 'filter0 configuration register',
    'FILTCON1': 'filter1 configuration register',
    'FILTCON2': 'filter2 configuration register',
    'FILTCON3': 'filter3 configuration register',

    'OFFSET0': 'offset0 register',
    'OFFSET1': 'offset1 register',
    'OFFSET2': 'offset2 register',
    'OFFSET3': 'offset3 register',

    'GAIN0': 'gain0 register',
    'GAIN1': 'gain1 register',
    'GAIN2': 'gain2 register',
    'GAIN3': 'gain3 register'
}

OP = {'w': 0x00, 'r': 0x40}

MISO = Pin(0, Pin.IN, Pin.PULL_DOWN)
CSn = Pin(1, Pin.OUT)
SCLK = Pin(2, Pin.OUT)
MOSI = Pin(3, Pin.OUT)


spi = SPI(0, baudrate = 10000000, polarity = 1, phase=1, bits=8, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

def Reset():    #复位
    i = 64
    buf = bytearray()
    buf.append(0x00)
    MOSI.value(1)
    CSn.value(0)
    while i > 0:
        spi.write(buf)
        i = i - 1
        utime.sleep_us(10)
    CSn.value(1)
    MOSI.value(0)
    utime.sleep_us(500)
    print("Reset.")

def Access(op, reg, value = 0x00, bytes = 3):
    if reg in ['STATUS', 'REGCHECK', 'DATA', 'ID'] and op == 'w':
        print("Error, read only!")
        return 1
    if reg == 'COMMS' and op == 'r':
        print("Error, write only!")
        return 1

    buf = bytearray()
    buf.append(OP[op] + REG[reg])
    CSn.value(0)
    spi.write(buf)

    if op == 'r':
        v = hex(int.from_bytes(spi.read(bytes), 'big'))
        CSn.value(1)
        return v

    if op == 'w':
        buf = bytearray()
        while value > 0:
            buf.append(value)
            value = value >> 8
        spi.write(buf)
        CSn.value(1)

def VIN_24(data, gain, offset, vref = 2.5):
    return ((int(data) / 2 * 0x400000 / int(gain)) + (int(offset) - 0x800000)) / pow(2, 23) * vref / 0.75 * 4.3

def VIN_32(data, gain, offset, vref = 2.5):
    return ((int(data) / 2 * 0x400000 / int(gain)) + (int(offset) - 0x800000)) / pow(2, 31) * vref / 0.75 * 4.3

def calu(self):
    global RX_MEASURE, Time_list, Data_list, i, Counter
    i = i + 1
    print(i)
    if len(Time_list) == 500:
        tm.deinit()
        for line in Time_list:
            utime.sleep(0.002)
            uart1.write((str(Time_list.index(line)) + '\t' + str(Data_list[Time_list.index(line)]) + '\n').encode("gbk"))
        Time_list.clear()
        Data_list.clear()
        i = 0
    data = Access('r', 'DATA', bytes = 4)
    Time_list.append(utime.ticks_ms())
    Data_list.append(offset0 + '\t' + gain0 + '\t' + data)

RX_MEASURE = False
Time_list = []
Data_list = []
i = 0
Counter = 0
tm = Timer(-1)
def measure(freq):
    global RX_MEASURE, Time_list, Data_list, i, Counter
    Counter = Counter + 1
    if RX_MEASURE == True:
        tm.init(freq = freq, mode = Timer.PERIODIC, callback = calu)
        utime.sleep(5)

# if __name__ == "__main__":
freq = 100
uart1 = UART(1, baudrate = 115200, bits=8, parity = None, stop = 1, tx = Pin(8), rx = Pin(9))
# measure_thread = _thread.start_new_thread(measure, (freq, ))

# while True:
    # print("Master.rx_measure = ", RX_MEASURE)
    # utime.sleep(1)
    # while uart1.any() > 0:
    #     data = uart1.readline()

        # if data == b'*':
RX_MEASURE = True
# print(data)

Reset()

print("start.")
print("ID: ", Access('r','ID', bytes = 2))


Access('w', 'SETUPCON0', value = 0x2003)
print("SETUPCON0: ", Access('r', 'SETUPCON0', bytes = 2))

offset0 = Access('r', "OFFSET0", bytes = 3)
print("OFFSET0: ", offset0)

Access('w', 'GAIN0', value = 0x555555)
gain0 = Access('r', 'GAIN0', bytes = 3)
print("GAIN0: ", gain0)

# Access('w', 'IFMODE', value = 0x0000)
# Access('r', 'IFMODE', bytes = 2)

# data = Access('r', 'DATA', bytes = 3)
# vin_24 = VIN_24(data, gain0, offset0)
# print("VIN_24: ", vin_24)

Access('w', 'ADCMODE', value = 0x00a0)
print("ADCMODE: ", Access('r', 'ADCMODE', bytes = 2))

Access('w', 'IFMODE', value = 0x0200)
print("IFMODE: ", Access('r', 'IFMODE', bytes = 2))

# Access('w', 'FILTCON0', value = 0x0e05)    # 100SPS
Access('w', 'FILTCON0', value = 0x0705)    # 10000SPS
print("FILTCON0: ", Access('r', 'FILTCON0', bytes = 2))

# while True:
#     start = utime.ticks_ms()
#     data = Access('r', 'DATA', bytes = 4)
#     print(data)
#     vin_32 = VIN_32(data, gain0, offset0)
#     print("VIN_32: ", vin_32)
#     print(utime.ticks_ms() - start)
# print(offset0 + gain0 + data)


# measure(100)

Access('w', 'IFMODE', value = 0x0201)
print("IFMODE: ", Access('r', 'IFMODE', bytes = 2))

CSn.value(0)

buf_1 = bytearray()
buf_2 = bytearray()
buf_3 = bytearray()
buf_1.append(0x02)
print(buf_1)
spi.write(buf_1)
buf_2.append(0x00)
spi.write(buf_2)
buf_3.append(0x80)
spi.write(buf_3)

print(MISO.value())

for i in range(0, 100):
    v = hex(int.from_bytes(spi.read(4), 'big'))
    print("v: ", VIN_32(v, gain0, offset0))
    Time_list.append(utime.ticks_ms())
    Data_list.append(offset0 + '\t' + gain0 + '\t' + v)

buf_4 = bytearray()
buf_4.append(0x44)
spi.write(buf_4)

CSn.value(1)

print(Time_list)
print(Data_list)

print("over.")
