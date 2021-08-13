
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# import numpy as np

# root = tkinter.Tk()
# root.wm_title("Embedding in Tk")
# fig = Figure(figsize=(5, 4), dpi=100)
# Time_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', 
# '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']
# Data_list = ['1.873009', '1.93103', '1.933327', '1.941648', '1.93635', '1.927262', '1.935136', '1.937728', '1.933091', '1.936307', '1.932589', '1.935298', '1.935997', '1.939202', '1.934767', '1.937861', '1.933368', '1.936345', '1.932973', '1.934836', '1.93026', '1.933134', '1.933836', '1.936932', '1.932578', '1.935933', '1.93148', '1.93428', '1.930065', '1.933903', '1.928287', '1.936987', '1.931875', '1.934948', '1.930366', '1.934149', '1.929594', '1.932884', '1.928335', '1.931376', '1.931714', '1.909502', '1.926084', '1.933008', '1.928752', '1.932964', '1.927324', '1.929957', '1.925642', '1.929542', '1.929086', '1.931861', '1.927261', '1.930687', '1.926079', '1.928916', '1.938484', '1.941944', '1.9377', '1.940984', '1.941394', '1.94493', '1.940487', '1.944001', '1.939618', '1.947219', '1.942939', '1.941625', '1.937747', '1.940661', '1.941663', 
# '1.945085', '1.94', '1.94315', '1.939268', '1.942205', '1.938105', '1.941401', '1.937023', '1.939594', '1.935402', '1.94387', '1.939392', '1.942069', '1.938404', '1.94131', '1.9368', '1.940021', '1.935977', '1.938993', '1.94021', '1.942745', '1.93924', '1.942151', '1.938403', '1.940288', '1.936532', '1.9391', '1.939509', '1.942004']
# fig.add_subplot(111).plot(Time_list, Data_list)
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()
# canvas.get_tk_widget().place(x = 550, y = 50)
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().place(x = 550, y = 50)
# tkinter.mainloop()

import tkinter as tk

# # make a window
root = tk.Tk()

# def make_new_window():
#     # when this function is called...

#     # make a second window
#     window2 = tk.Toplevel(root)

#     # add some text to the second window (note the use of
#     # root2 as the first argument)
#     label = tk.Label(window2, text="This label is added to the new window")
#     label.pack()

# # make a new button on the first window
# button = tk.Button(root, text="Click here for a new window", command=make_new_window)
# button.pack()

rootp = tkinter.Toplevel(root)
rootp.wm_title("Embedding in Tk")
figp = Figure(figsize=(5, 4), dpi=100)
Time_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Data_list = ['1.873009', '1.93103', '1.933327', '1.941648', '1.93635', '1.927262', '1.935136', '1.937728', '1.933091', '1.936307']
figp.add_subplot(111).plot(Time_list, Data_list)
canvasp = FigureCanvasTkAgg(fig, master=rootp)
canvasp.draw()
canvasp.get_tk_widget().place(x = 550, y = 50)
toolbarp = NavigationToolbar2Tk(canvas, rootp)
toolbarp.update()
canvasp.get_tk_widget().place(x = 550, y = 50)

root.mainloop()