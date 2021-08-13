# print(((0x4a5109e9 / 2 * 0x400000 / 0x555555) + (0x800000 - 0x800000)) / pow(2, 31) * 2.5 / 0.75 * 4.3)
# print(1/3)
# print(1.34e-4)

# a = ['wefefw','fwegr']
# print(''.join(a))
import utime

start = utime.ticks_ms()
print(int('0x10', 16))
print(utime.ticks_ms() - start)

while True:
    start = utime.ticks_ms()
    print(utime.ticks_ms() - start)



Time_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Data_list = ['1.873009', '1.93103', '1.933327', '1.941648', '1.93635', '1.927262', '1.935136', '1.937728', '1', '0.5']
plt.plot(Time_list, Data_list, marker='o', mec='r', mfc='w',label=u'测量结果')
plt.xticks(Time_list, Time_list, rotation=45)
plt.margins(0)
plt.xlabel(u"time(ms)")
plt.ylabel("voltage(v)")
plt.title("measurement result")
plt.show()