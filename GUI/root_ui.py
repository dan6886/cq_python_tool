# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'root_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 234)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 0, 371, 181))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.start_day = QtWidgets.QDateEdit(self.formLayoutWidget)
        self.start_day.setObjectName("start_day")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.start_day)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.interval = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.interval.setObjectName("interval")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.interval)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.random_time_start = QtWidgets.QTimeEdit(self.formLayoutWidget)
        self.random_time_start.setObjectName("random_time_start")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.random_time_start)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setEnabled(True)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.random_time_end = QtWidgets.QTimeEdit(self.formLayoutWidget)
        self.random_time_end.setObjectName("random_time_end")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.random_time_end)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.folder = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.folder.setObjectName("folder")
        self.horizontalLayout.addWidget(self.folder)
        self.set_folder = QtWidgets.QPushButton(self.formLayoutWidget)
        self.set_folder.setObjectName("set_folder")
        self.horizontalLayout.addWidget(self.set_folder)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)
        self.run = QtWidgets.QPushButton(self.formLayoutWidget)
        self.run.setObjectName("run")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.run)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "tool"))
        self.label.setText(_translate("MainWindow", "起始日期"))
        self.label_4.setText(_translate("MainWindow", "周期天数"))
        self.label_2.setText(_translate("MainWindow", "当天随机时间起点"))
        self.random_time_start.setDisplayFormat(_translate("MainWindow", "HH:mm:ss"))
        self.label_3.setText(_translate("MainWindow", "当天随机时间终点"))
        self.random_time_end.setDisplayFormat(_translate("MainWindow", "HH:mm:ss"))
        self.set_folder.setText(_translate("MainWindow", "选择文件夹"))
        self.run.setText(_translate("MainWindow", "运行"))
