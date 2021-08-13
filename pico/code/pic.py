import matplotlib.pyplot as plt
from pylab import *
from functools import cmp_to_key
import os
while True:
    path = input("path:")

    f = open(path, 'r')
    Time_list = []
    Data_list = []


    def my_cmp(x, y):
        temp = x - y
        if temp > 0:
            return 1
        elif temp == 0:
            return 0
        else:
            return -1

    def float_range(start, stop, step):
        ''' 支持 float 的步进函数

        输入 Input:
            start (float)  : 计数从 start 开始。默认是从 0 开始。
            end   (float)  : 计数到 stop 结束，但不包括 stop。
            step (float)  : 步长，默认为 1，如为浮点数，参照 steps 小数位数。

        输出 Output:
            浮点数列表

        例子 Example:
            >>> print(float_range(3.612, 5.78, 0.22))
            [3.612, 3.832, 4.052, 4.272, 4.492, 4.712, 4.932, 5.152, 5.372]
    '''
        start_digit = len(str(start))-1-str(start).index(".") # 取开始参数小数位数
        stop_digit = len(str(stop))-1-str(stop).index(".")    # 取结束参数小数位数
        step_digit = len(str(step))-1-str(step).index(".")    # 取步进参数小数位数
        digit = max(start_digit, stop_digit, step_digit)      # 取小数位最大值
        return [(start*10**digit+i*step*10**digit)/10**digit for i in range(int((stop-start)//step))]

    for line in f.readlines():
        line_split = line.split('\t')
        Time_list.append(line_split[0].strip('\n'))
        Data_list.append(float(line_split[1].strip('\n')))
        Data_list_p = Data_list
        # Data_list_p.sort(key = cmp_to_key(my_cmp))

    print(Data_list)
    plt.plot(Time_list, Data_list, marker='o', mec='r', mfc='w',label=u'测量结果')

    x_labels = range(0, 1000, 100)
    x = [x for x in Time_list if Time_list.index(x) % 100 == 0]
    print("x: ", x)
    print("x_labels: ", x_labels)

    y_labels = [y for y in Data_list_p if Data_list_p.index(y) % 100 == 0]
    for y in y_labels:
        print(Data_list_p.index(y))
    y = float_range(Data_list_p[0], Data_list_p[99], (Data_list_p[99] - Data_list_p[0]) / 10)
    print("y: ", y)
    print("y_labels: ", y_labels)

    plt.xticks(x, x_labels,color='blue', rotation=0)
    # plt.xticks(y, y_labels,color='blue', rotation=0)

    plt.margins(0)
    plt.xlabel(u"time(ms)")
    plt.ylabel("voltage(v)")
    plt.title("measurement result")
    plt.show()

    f.close()
    Time_list.clear()
    Data_list.clear()