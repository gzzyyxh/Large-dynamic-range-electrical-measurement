# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Github\Large-dynamic-range-electrical-measurement\pico\code\10.26\ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1993, 990)
        MainWindow.setMouseTracking(False)
        MainWindow.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Output = QtWidgets.QLabel(self.centralwidget)
        self.Output.setGeometry(QtCore.QRect(60, 230, 104, 15))
        self.Output.setTextFormat(QtCore.Qt.AutoText)
        self.Output.setScaledContents(False)
        self.Output.setObjectName("Output")
        self.pushButton_START = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_START.setEnabled(True)
        self.pushButton_START.setGeometry(QtCore.QRect(500, 40, 91, 41))
        self.pushButton_START.setObjectName("pushButton_START")
        self.textEdit_Configuration = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Configuration.setGeometry(QtCore.QRect(20, 100, 181, 81))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.textEdit_Configuration.setFont(font)
        self.textEdit_Configuration.setObjectName("textEdit_Configuration")
        self.comboBox_device = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_device.setGeometry(QtCore.QRect(20, 40, 181, 21))
        self.comboBox_device.setObjectName("comboBox_device")
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(240, 40, 93, 28))
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_disconnect.setGeometry(QtCore.QRect(370, 40, 93, 28))
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(30, 270, 32, 15))
        self.label_20.setObjectName("label_20")
        self.comboBox_rate = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_rate.setGeometry(QtCore.QRect(80, 270, 71, 21))
        self.comboBox_rate.setObjectName("comboBox_rate")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(170, 270, 24, 15))
        self.label_21.setObjectName("label_21")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(20, 410, 48, 15))
        self.label_24.setObjectName("label_24")
        self.textEdit_points = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_points.setEnabled(False)
        self.textEdit_points.setGeometry(QtCore.QRect(80, 400, 71, 31))
        self.textEdit_points.setObjectName("textEdit_points")
        self.pushButton_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Stop.setEnabled(True)
        self.pushButton_Stop.setGeometry(QtCore.QRect(610, 40, 91, 41))
        self.pushButton_Stop.setObjectName("pushButton_Stop")
        self.textEdit_File = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_File.setGeometry(QtCore.QRect(940, 40, 491, 31))
        self.textEdit_File.setObjectName("textEdit_File")
        self.pushButton_File = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_File.setGeometry(QtCore.QRect(1440, 40, 41, 28))
        self.pushButton_File.setObjectName("pushButton_File")
        self.pushButton_Clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Clear.setEnabled(True)
        self.pushButton_Clear.setGeometry(QtCore.QRect(830, 40, 91, 41))
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.pushButton_Continue = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Continue.setEnabled(True)
        self.pushButton_Continue.setGeometry(QtCore.QRect(720, 40, 91, 41))
        self.pushButton_Continue.setObjectName("pushButton_Continue")
        self.label_h = QtWidgets.QLabel(self.centralwidget)
        self.label_h.setGeometry(QtCore.QRect(170, 320, 8, 15))
        self.label_h.setObjectName("label_h")
        self.textEdit_h = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_h.setGeometry(QtCore.QRect(80, 310, 71, 31))
        self.textEdit_h.setObjectName("textEdit_h")
        self.textEdit_min = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_min.setGeometry(QtCore.QRect(80, 350, 71, 31))
        self.textEdit_min.setObjectName("textEdit_min")
        self.pushButton_Save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Save.setEnabled(True)
        self.pushButton_Save.setGeometry(QtCore.QRect(80, 500, 71, 31))
        self.pushButton_Save.setObjectName("pushButton_Save")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 340, 32, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 360, 24, 15))
        self.label_2.setObjectName("label_2")
        self.label_res = QtWidgets.QLabel(self.centralwidget)
        self.label_res.setGeometry(QtCore.QRect(240, 910, 1031, 20))
        self.label_res.setObjectName("label_res")
        self.textEdit_out_1_A = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_out_1_A.setGeometry(QtCore.QRect(80, 450, 71, 31))
        self.textEdit_out_1_A.setObjectName("textEdit_out_1_A")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(10, 460, 56, 15))
        self.label_25.setObjectName("label_25")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 8, 15))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1993, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Output.setText(_translate("MainWindow", "Configuration"))
        self.pushButton_START.setText(_translate("MainWindow", "Start"))
        self.pushButton_connect.setText(_translate("MainWindow", "Connect"))
        self.pushButton_disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.label_20.setText(_translate("MainWindow", "rate"))
        self.label_21.setText(_translate("MainWindow", "SPS"))
        self.label_24.setText(_translate("MainWindow", "points"))
        self.pushButton_Stop.setText(_translate("MainWindow", "Stop"))
        self.pushButton_File.setText(_translate("MainWindow", "..."))
        self.pushButton_Clear.setText(_translate("MainWindow", "Clear"))
        self.pushButton_Continue.setText(_translate("MainWindow", "Continue"))
        self.label_h.setText(_translate("MainWindow", "h"))
        self.pushButton_Save.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "time"))
        self.label_2.setText(_translate("MainWindow", "min"))
        self.label_res.setText(_translate("MainWindow", "已测量0次 当前用时0s 总用时0s 平均用时0s"))
        self.label_25.setText(_translate("MainWindow", "out_1_A"))
        self.label_3.setText(_translate("MainWindow", "v"))
