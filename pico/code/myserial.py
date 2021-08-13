import serial
import serial.tools.list_ports
import threading
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askdirectory
import time
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import inspect
import ctypes
import numpy as np



def _async_raise(tid, exctype):
  """raises the exception, performs cleanup if needed"""
  tid = ctypes.c_long(tid)
  if not inspect.isclass(exctype):
    exctype = type(exctype)
  res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
  if res == 0:
    raise ValueError("invalid thread id")
  elif res != 1:
    # """if it returns a number greater than one, you're in trouble,
    # and you should call it again with exc=NULL to revert the effect"""
    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
    raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
  _async_raise(thread.ident, SystemExit)

'''
    1、扫描串口列表
    2、打开串口
    3、向串口写数据
    4、从串口读数据
    5、关闭串口

    init 初始化串口
        --> 创建线程：
            1. 如果串口未打开，则用于实时扫描串口，检测是否有新设备插入
                有新设备插入：添加到设备列表，并刷新UI的设备列表提供选择
                没有新设备：继续扫描
            2. 如果串口已打开，则用于监测串口是否有接收到数据
                如果有则读取数据，并发送给UI
                如果没有则继续扫描
        参数：主窗口，端口列表，接收窗口
        返回：线程实例(用于关闭窗口前，先关闭线程)

    open 打开串口
        --> 参数：端口号，波特率，超时时间
            返回：串口实例（打开成功）/ None(打开失败)

    close 关闭串口
        --> 参数：串口实例
            返回：0（关闭成功）/ -1（关闭失败）

    write 写数据
    read 读数据

'''

SERIAL_IS_OPEN = False      # 默认串口关闭
port_name_list = []         # 端口名称列表
port_com_list = []          # 端口号列表
line_list = []
Time_list = []
Data_list = []
MySerial = None             # 打开的串口
Counter = 0
Measure_Start = False
Measure_End = False
File = None
_Figure = None
PATH = None
Get_str = []
threadLock = threading.Lock()

def 扫描串口():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) > 0:
        # print(port_list)
        return port_list
    else:
        return None

def 打开串口(port, bps, timex, text, button_0, button_1):
    try:
        # 打开串口
        ser = serial.Serial(port, bps, timeout=timex)

        if ser.is_open:
            global SERIAL_IS_OPEN
            SERIAL_IS_OPEN = True
            # print("--- 串口打开 ---")
            text.configure(state='normal')
            text.insert(tk.END, "\n-------打开串口：" + str(port) + "---------\n")
            text.configure(state='disable')
            text.see(tk.END)
            button_0['state'] = tk.DISABLED
            button_1['state'] = tk.NORMAL
            return ser

    except Exception as e:
        # print("--- 打开异常 ---: ", e)
        messagebox.showinfo("拒绝访问", str(e))
        return None

def 发送数据(ser, text, code="utf-8"):
    try:
        result = ser.write(text.encode(code))
        if result == len(text):
            # print("--- 发送成功 ---：", text)
            return result
        else:
            # print("--- 发送错误 ---：", "data len:", len(text), "send len:", result)
            messagebox.showinfo("错误","发送错误")
            return None
    except Exception as e:
        # print("--- 发送异常 ---：", e)
        messagebox.showinfo("发送异常", str(e))

def 读取数据(ser, code="utf-8"):
    if ser.in_waiting:
        str = ser.read(ser.in_waiting).decode(code)
        # print("--- 读到数据 ---：", str)
        return str
    else:
        return None


def 关闭串口(ser, text, button_0, button_1):
    if ser.is_open:
        try:
            global SERIAL_IS_OPEN
            SERIAL_IS_OPEN = False
            ser.close()
            # print("--- 串口关闭 ---")
            text.configure(state='normal')
            text.insert(tk.END, "\n-------关闭串口---------------\n")
            text.configure(state='disable')
            text.see(tk.END)
            button_0['state'] = tk.NORMAL
            button_1['state'] = tk.DISABLED
            return 0
        except Exception as e:
            # print("--- 关闭异常 ---：", e)
            messagebox.showinfo("关闭异常", str(e))
            return -1
    else:
        # print("--- 错误 ---：串口未打开！")
        messagebox.showinfo("错误", "串口未打开")
        return -1

def calu(line_list, vref = 2.5):
    for line in line_list:
        line_split = line.split('\t')
        Time_list.append(int(line_split[0]))
        Data_list.append(((int(line_split[3], 16) / 2 * 0x400000 / int(line_split[2], 16)) + (int(line_split[1], 16) - 0x800000)) / pow(2, 31)
                         * vref / 0.75 * 4.3)

class SERIAL:
    def __init__(self):
        self.ser = None
        self.get_str = ''
        print(self.get_str)
        self.master = None
        self.show_com = None
        self.read_text_win = None
        self.win_read_text = None
        self.serialThread = None
        self.fileThread = None
        self.canvas = None

    def serial_thread(self, master, list_port, text_read):
        global SERIAL_IS_OPEN, port_name_list, port_com_list, Measure_End, File, _Figure, Get_str
        global MySerial
        while True:
            # print(Measure_End)
            # time.sleep(1)
            if SERIAL_IS_OPEN:
                # start = time.time()
                self.get_str = 读取数据(MySerial)
                if self.get_str:
                    print(self.get_str)
                    Get_str.append(self.get_str)
                    # print(Get_str)
                    text_read.configure(state='normal')
                    text_read.insert(tk.END, self.get_str)
                    text_read.configure(state='disable')
                    text_read.see(tk.END)
                    if (File != None or _Figure != None) and self.get_str[-1] == '\n':
                        hole_str = ''.join(Get_str)
                        # print(hole_str)
                        str_split = hole_str.split('\n')
                        # print(str_split)
                        data = [x for x in str_split if x != '']
                        # print(data)
                        threadLock.acquire()
                        for line in data:
                            print(line)
                            line_list.append(line)
                        print(len(line_list))
                        if len(line_list) == 500:
                            calu(line_list)
                            time.sleep(1)
                            Measure_End = True
                        threadLock.release()
                        # print("Counter:", Counter)
                        # print("len: ",len(line_list))
                        Get_str.clear()
                    master.update()
                    # print("serial: ", time.time() - start)
            else:
                port_list = 扫描串口()
                if len(port_name_list) is not len(port_list):   # 只判断列表长度，不可靠。需修改为列表内容判断比较可靠
                    port_name_list.clear()
                    port_com_list.clear()
                    for i in range(0, len(port_list)):
                        port_name_list.append(port_list[i].description)
                        port_com_list.append(port_list[i].device)
                        list_port["values"] = port_name_list
                        if list_port.get() == "":  # 如果当前UI中的端口列表为空，则指定显示第一个
                            list_port.current(0)
                    master.update()

    @classmethod
    def init(cls, master, list_port, text_send, text_recv, canvas):
        cls.master = master
        cls.show_com = list_port
        cls.read_text_win = text_send
        cls.win_read_text = text_recv
        cls.canvas = canvas
        cls.serialThread = threading.Thread(target=cls.serial_thread,
                                            args=(SERIAL, cls.master, cls.show_com, cls.win_read_text))

        cls.serialThread.start()
        return cls.serialThread

    @classmethod
    def open(cls, button_0, button_1, port=None, bps=115200, timex=5):
        global port_name_list, port_com_list, MySerial
        if not port:
            port_name = cls.show_com.get()
            index = port_name_list.index(port_name)
            MySerial = 打开串口(port_com_list[index], bps, timex, cls.win_read_text, button_0, button_1)
            print(MySerial)
            print(type(MySerial))
        else:
            MySerial = 打开串口(port, bps, timex, cls.win_read_text, button_0, button_1)
            print(MySerial)
            print(type(MySerial))

    @staticmethod
    def write(text, coding="gbk"):
        global MySerial, SERIAL_IS_OPEN, Counter
        # Counter = Counter + 1
        if SERIAL_IS_OPEN:
            发送数据(MySerial, text, coding)

    @staticmethod
    def read(coding="gbk"):
        global MySerial, SERIAL_IS_OPEN
        str = None
        if SERIAL_IS_OPEN:
            str = 读取数据(MySerial, coding)
        return str

    @classmethod
    def close(cls, button_0, button_1):
        global MySerial, SERIAL_IS_OPEN
        if SERIAL_IS_OPEN and MySerial:
            关闭串口(MySerial, cls.win_read_text, button_0, button_1)


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk
    root = tk.Tk()
    root.title("测试窗口")
    root.geometry("550x650")

    frame = tkinter.Frame(root)
    frame.place(x=10, y=200)

    list_box = ttk.Combobox(root, width = 22, textvariable=port_name_list, state="readonly")
    list_box.place(x=10, y=10)

    text_box_send = tk.Text(root, width = 60, heigh = 10)
    text_box_send.place(x=10, y=50)

    scroll = tkinter.Scrollbar(frame)
    scroll.pack(side = tkinter.RIGHT, fill  = tkinter.Y)

    text_box_recv = tk.Text(frame, width = 60, heigh = 30, yscrollcommand = scroll.set)
    text_box_recv.pack()
    text_box_recv.configure(state='disabled')

    scroll.config(command = text_box_recv.yview)
    text_box_recv.config(yscrollcommand = scroll.set)

    def open_serial():
        SERIAL.open(button_0 = button0, button_1 = button2)

    def send_date():
        SERIAL.write(str(text_box_send.get(1.0, "end")), coding="gbk")

    def close_serial():
        SERIAL.close(button_0 = button0, button_1 = button2)

    def meas():
        SERIAL.write("*", coding = "gbk")
        # Measure_Start = True
        # text_box_recv.configure(state='normal')
        # text_box_recv.insert(tk.END, "\n-------第" + str(Counter) + "次测量-------------\n")
        # text_box_recv.insert(tk.END, "\n-------开始测量---------------\n")
        # text_box_recv.see(tk.END)
        # text_box_recv.configure(state='disable')

    def recv_clear():
        text_box_recv.configure(state='normal')
        text_box_recv.delete(1.0,tkinter.END)
        text_box_recv.configure(state='disable')


    button0 = tk.Button(root, text="打开串口", command = open_serial)
    button0.place(x=230, y=8)
    button1 = tk.Button(root, text="发送数据", command = send_date)
    button1.place(x=450, y=50)
    button2 = tk.Button(root, text="关闭串口", command = close_serial)
    button2.place(x=330, y=8)
    button3 = tk.Button(root, text="开始测量", command = meas)
    button3.place(x=450, y=150)
    button4 = tk.Button(root, text="清空接收", command = recv_clear)
    button4.place(x=450, y=100)

    fig = Figure(figsize = (5, 4), dpi = 100)
    canvas = FigureCanvasTkAgg(fig, master = root)

    SERIAL.init(root, list_box, text_box_send, text_box_recv, canvas)

    file = IntVar()

    def file_thread(root):
        global Measure_End, PATH, Counter, File, line_list, Time_list, Data_list, _Figure
        while True:
            # print("File: ",File,'\t',"Measure_End: ",'\t',Measure_End)
            # time.sleep(1)
            if File and Measure_End:
                start = time.time()
                Counter = Counter + 1
                name = PATH + '/' + str(Counter) + ".txt"
                print(name)
                file = open(name, 'a+')
                print("hahahahahahahahahahahahaha")
                for line in Time_list:
                    file.write(str(line) + '\t' + str(Data_list[Time_list.index(line)]) + '\n')
                    # line_split = line.split('\t')
                    # Data_list.append(float(line_split[1]))
                file.close()

                mean, std = np.mean(Data_list), np.std(Data_list, ddof = 1)
                for n in Data_list:
                    if n > mean + std *5 or n < mean - std * 5:
                        Data_list.remove(n)

                res = open("res/res.txt", 'a+')
                res.write(str(Counter)
                          + '\t' + str(len(Data_list))
                          + '\t' + str(max(Data_list))
                          + "\t" + str(min(Data_list))
                          + '\t' + str(max(Data_list) - min(Data_list))
                          + "\t" +str(np.mean(Data_list))
                          + "\t\t" + str(np.var(Data_list))
                          + "\t" +str(np.std(Data_list, ddof=1)) + '\n')
                res.close()

                if _Figure == None:
                    line_list.clear()
                    Data_list.clear()
                    print("Counter: ", Counter, "\tFile:",File,"\tMeasure_End", Measure_End)
                Measure_End = False
                print("measure_end", Measure_End)
                print("file: ", time.time() - start)
                messagebox.showinfo("提示", "文件已保存")

    fileThread = None

    def fileSelect():
        global File, fileThread
        File = file.get()
        if File:
            button5['state'] = tk.NORMAL
            if type(fileThread) != threading.Thread or (type(fileThread) == threading.Thread and  not fileThread.is_alive()):
                fileThread = threading.Thread(target=file_thread,args=(root, ))
                fileThread.start()
        else:
            button5['state'] = tk.DISABLED
            if type(fileThread) == threading.Thread and fileThread.is_alive():
                stop_thread(fileThread)

    figure = IntVar()

    def figure_thread(root, canvas):
        global line_list, Time_list, Data_list, Measure_End, _Figure
        while True:
            # print("Figure: ",_Figure,'\t',"Measure_End: ",'\t',Measure_End)
            # time.sleep(1)
            if _Figure and Measure_End:
                print("Figure!.")
                mean, std = np.mean(Data_list), np.std(Data_list, ddof = 1)
                for n in Data_list:
                    if n > mean + std *5 or n < mean - std * 5:
                        Data_list.remove(n)
                # for line in line_list:
                #     line_split = line.split('\t')
                #     Time_list.append(line_split[0])
                #     Data_list.append(line_split[1])
                Measure_End = False
                if File == None:
                    line_list.clear()
                fig = Figure(figsize = (10, 6), dpi = 100)
                print(1)
                # Time_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                # Data_list = [1.873009, 1.93103, 1.933327, 1.941648, 1.93635, 1.927262, 1.935136, 1.937728, 1, 0.5]
                fig.add_subplot(111).plot(Time_list, Data_list, marker='o', mec='r', mfc='w', ms = 1, label=u'测量结果')
                x_labels = range(min(Time_list), max(Time_list), (max(Time_list) - min(Time_list)) // 10 )
                print(x_labels)
                fig._supxlabel = x_labels
                # x_labels = range(0, 100, 10)
                # fig.xticks(10, x_labels,color='blue', rotation=60)
                print(2)
                canvas = FigureCanvasTkAgg(fig, master = root)
                print(3)
                canvas.draw()
                print(4)
                canvas.get_tk_widget().place(x = 550, y = 50)
                print(5)
                toolbar = NavigationToolbar2Tk(canvas, root)
                print(6)
                toolbar.update()
                print(7)
                canvas.get_tk_widget().place(x = 550, y = 50)
                print(8)
                Time_list.clear()
                print(9)
                Data_list.clear()
                print(0)

    figureThread = None
    def figureSelect():
        global _Figure, figureThread
        _Figure = figure.get()
        if _Figure:
            root.geometry("1100x650")
            if type(figureThread) != threading.Thread or (type(figureThread) == threading.Thread and  not figureThread.is_alive()):
                figureThread = threading.Thread(target=figure_thread,args=(root, canvas))
                figureThread.start()
        else:
            root.geometry("550x650")
            if type(figureThread) == threading.Thread and figureThread.is_alive():
                stop_thread(figureThread)

    checkbutton0 = Checkbutton(root, text="自动绘图", variable = figure, onvalue = 1, offvalue = 0, command = figureSelect)
    checkbutton0.place(x=10, y=600)
    checkbutton0 = Checkbutton(root, text="自动保存", variable = file, onvalue = 1, offvalue = 0, command = fileSelect)
    checkbutton0.place(x=100, y=600)

    path = StringVar()

    def selectPath():
        global PATH
        path_ = askdirectory()

        path.set(path_)
        PATH = path_

    entry0 = Entry(root, textvariable = path, state='readonly')
    entry0.place(x=190, y=605)
    button5 = Button(root, text = "...", command = selectPath, state = "disable")
    button5.place(x=350, y=600)

    root.mainloop()