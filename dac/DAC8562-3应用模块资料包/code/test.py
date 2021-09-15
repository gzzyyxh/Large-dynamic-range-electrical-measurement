def Voltage2DIN(vout, vref = 2.5, gain = 2):
    DIN = int((vout/4.17 + vref) / (vref * gain) * pow(2, 16))
    print("hex: ", hex(DIN))
    return DIN

while True:
    v = input("input v: ")
    print(Voltage2DIN((float(v))))
# import utime

# while True:
#     start = utime.ticks_us()

#     # utime.sleep_us(1)

#     print(utime.ticks_us() - start)
