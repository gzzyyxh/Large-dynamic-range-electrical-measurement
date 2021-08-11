import os
import tkinter as tk

# filedialog是tkinter模块下的一个子模块，并不是他的函数和性质。
# 不能直接去调用filedialog模块下的函数；需要引入子模块filedialog，再去使用它的函数。
# 这个问题提示我们再使用python的过程中，需要注意子模块和函数的性质。
# 同时这也是类中的相关知识，子模块就是子类，函数是父类中的函数。
from tkinter import filedialog
# import tkinter.filedialog

fpath = ""
dirpath = ""

#1 新建窗口
root = tk.Tk()

#2 给窗口起名字
root.title("文件浏览器")

#3 设定窗口大小
root.geometry("1024x768")

# 锁定大小
root.resizable(False, True)

#4 frame 整体框架设计
#顶部Frame,上下排列，横向填充
frame_Top = tk.Frame(root)
frame_Top.pack(
    side=tk.TOP,
    fill=tk.X,
)
# 中部Frame，上下排列，向下扩展，双向填充
frame_Middle = tk.Frame(root)
frame_Middle.pack(
    side=tk.TOP,
    expand=tk.YES,
    fill=tk.BOTH,
)
# 底部Frame
frame_End = tk.Frame(root)
frame_End.pack(
    side=tk.TOP,
    expand=tk.NO,
    fill=tk.BOTH,
)

# 底部左边Frame，扩展
frame_End_left = tk.Frame(frame_End)
frame_End_left.pack(
    side=tk.LEFT,
    expand=tk.YES,
    fill=tk.BOTH,
)

# 底部右边Frame，不扩展
frame_End_right = tk.Frame(frame_End)
frame_End_right.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
)

#5 自定义函数


#显示文件信息
def get_file_information(event):
    fname.set("")
    ftype.set("")
    fsize.set("")
    fpath.set("")
    try:
        value = lb_files.get(lb_files.curselection())
        # 文件名称
        fname.set(os.path.basename(value))
        # 文件类型
        ftype.set(os.path.splitext(value)[1])
        # 计算文件大小
        s = os.stat(value).st_size
        if s > 1000000000:
            s /= 1000000000
            fsize.set("{:.2f} GB".format(s))
        elif s > 1000000:
            s /= 1000000
            fsize.set("{:.2f} MB".format(s))
        elif s > 1000:
            s /= 1000
            fsize.set("{:.2f} KB".format(s))
        # 文件路径
        fpath.set(value)
    except tk.TclError:
        pass


# 打开文件夹
def get_dirs_information(event):
    fname.set("")
    ftype.set("")
    fsize.set("")
    fpath.set("")
    try:
        value = lb_dirs.get(lb_dirs.curselection())
        # 文件夹名称
        fname.set(os.path.basename(value))
        # 文件夹是否为空
        if not os.listdir(value):
            ftype.set("文件夹为空")
        else:
            ftype.set("文件夹有东西")
        # 文件路径
        fpath.set(value)
    except tk.TclError:
        pass


# 分别处理文件和文件夹
def file_dir_divider(dirpath):
    lb_files.delete(0, tk.END)  # 清空
    lb_dirs.delete(0, tk.END)
    try:
        for fp in os.listdir(dirpath):
            filepath = dirpath + "/" + fp
            if os.path.isfile(filepath):
                lb_files.insert(tk.END, filepath)
            else:
                lb_dirs.insert(tk.END, filepath)
    except FileNotFoundError:  # 如果文件夹为空，则跳过
        pass


# 定义文件夹对话框函数
def openfile():
    global dirpath
    dirpath = e_path.get()
    if dirpath == "":
        dirpath = filedialog.askdirectory()
    else:
        dirpath = filedialog.askdirectory(initialdir=dirpath)
    e_path.delete(0, tk.END)
    e_path.insert(0, dirpath)
    file_dir_divider(dirpath)


# 添加Label
l_path = tk.Label(
    frame_Top,
    text="请选择路径：",
    font=("Arial", 15),
)
l_path.pack(
    side=tk.LEFT,
    padx=10,
    pady=10,
)

# 添加Entry，当前工作路径
e_path = tk.Entry(frame_Top, )
e_path.pack(
    side=tk.LEFT,
    expand=tk.YES,
    fill=tk.X,
    pady=10,
)

# 添加按钮，选择工作目录
b_select_path = tk.Button(
    frame_Top,
    text="Select Path",
    command=openfile,
    font=("Arial", 12),
)
b_select_path.pack(
    side=tk.LEFT,
    padx=10,
    pady=10,
)

#6 添加Listbox，显示目录下所有的文件夹
lb_dirs = tk.Listbox(
    frame_Middle,
    font=("Arial", 10),
)

lb_dirs.pack(
    side=tk.LEFT,
    expand=tk.YES,
    fill=tk.BOTH,
    padx=10,
    pady=10,
)

lb_dirs.bind("<<ListboxSelect>>", get_dirs_information)

# 添加滚动条
sb_dirs = tk.Scrollbar(lb_dirs)
sb_dirs.pack(
    side=tk.RIGHT,
    fill=tk.Y,
)

# 设定滚动条对应的滚动方向
sb_dirs.config(command=lb_dirs.yview)

# 绑定Text的Y方向滚动函数
lb_dirs.config(yscrollcommand=sb_dirs.set)

#7 添加Listbox，显示目录下所有文件
lb_files = tk.Listbox(
    frame_Middle,
    font=("Arial", 10),
)

lb_files.pack(
    side=tk.LEFT,
    expand=tk.YES,
    fill=tk.BOTH,
    padx=10,
    pady=10,
)

lb_files.bind("<<ListboxSelect>>", get_file_information)

# 添加滚动条
sb_files = tk.Scrollbar(lb_files)
sb_files.pack(
    side=tk.RIGHT,
    fill=tk.Y,
)

# 设定滚动条对应的滚动方向
sb_files.config(command=lb_files.yview)

# 绑定Text的Y方向滚动函数
lb_files.config(yscrollcommand=sb_files.set)

# 8 添加文件状态显示栏

# 添加Frame，上下排列，向下扩展，双向填充
frame_1 = tk.Frame(frame_End_left)
frame_1.pack(
    side=tk.TOP,
    fill=tk.BOTH,
)

fname = tk.StringVar()
tk.Label(frame_1, text="文件名：").pack(
    side=tk.LEFT,
    padx=10,
    pady=10,
)
l_fname = tk.Label(
    frame_1,
    textvariable=fname,
)
l_fname.pack(
    side=tk.LEFT,
    fill=tk.X,
    padx=10,
    pady=10,
)

# 添加Frame，上下排列，向下扩展，双向填充
frame_2 = tk.Frame(frame_End_left)
frame_2.pack(
    side=tk.TOP,
    fill=tk.BOTH,
)

# 添加label显示类型
ftype = tk.StringVar()
tk.Label(frame_2, text="文件类型：").pack(
    side=tk.LEFT,
    padx=10,
    pady=10,
)
l_ftype = tk.Label(
    frame_2,
    textvariable=ftype,
)
l_ftype.pack(
    side=tk.LEFT,
    fill=tk.X,
    padx=10,
    pady=10,
)

# 添加Frame，上下排列，向下扩展，双向填充
frame_3 = tk.Frame(frame_End_left)
frame_3.pack(
    side=tk.TOP,
    fill=tk.BOTH,
)
# 添加label显示文件大小
fsize = tk.StringVar()
tk.Label(frame_3, text="文件大小：").pack(
    side=tk.LEFT,
    padx=10,
    pady=10,
)
l_fsize = tk.Label(
    frame_3,
    textvariable=fsize,
)
l_fsize.pack(
    side=tk.LEFT,
    fill=tk.X,
    padx=10,
    pady=10,
)

# 添加Frame，上下排列，向下扩展，双向填充
frame_4 = tk.Frame(frame_End_left)
frame_4.pack(
    side=tk.TOP,
    fill=tk.BOTH,
)
# 添加label显示文件路径
fpath = tk.StringVar()
tk.Label(frame_4, text="文件路径：").pack(
    side=tk.LEFT,
    padx=10,
    pady=10,
)
l_fpath = tk.Label(
    frame_4,
    textvariable=fpath,
)
l_fpath.pack(
    side=tk.LEFT,
    fill=tk.X,
    padx=10,
    pady=10,
)

# 主窗口循环
