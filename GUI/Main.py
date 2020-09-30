import base64
import os
import sys
from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from GUI.Configuration import Configuration
from GUI.untitled import Ui_MainWindow
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time, datetime
import win32timezone



def connect_event(main_ui):
    main_ui.start_day.dateChanged.connect(onDateChanged)  # 点击按钮，执行btnFn方法
    main_ui.interval.valueChanged.connect(onIntervalChanged)  # 点击按钮，执行btnFn方法
    main_ui.random_time_start.timeChanged.connect(on_random_start_time_changed)  # 点击按钮，执行btnFn方法
    main_ui.random_time_end.timeChanged.connect(on_random_end_time_changed)  # 点击按钮，执行btnFn方法
    main_ui.folder.textChanged.connect(on_folder_change)  # 点击按钮，执行btnFn方法
    main_ui.set_folder.clicked.connect(partial(on_folder_selected, main_ui))  # 点击按钮，执行btnFn方法
    main_ui.run.clicked.connect(on_run)  # 点击按钮，执行btnFn方法
    pass


def onDateChanged(date):
    # 输出改变的日期
    start_date = time.mktime((date.year(), date.month(), date.day(), 0, 0, 0, 0, 0, 0))
    configuration.set_start_day(start_date)
    print(start_date)


def onIntervalChanged(value):
    # 输出改变的日期
    configuration.set_increment_day(value)
    print(time.localtime(Configuration.STANDARD_TIME))


def on_random_start_time_changed(time_value):
    # 输出改变的日期
    standard = time.localtime(Configuration.STANDARD_TIME)
    start_random_time = time.mktime((standard.tm_year, standard.tm_mon, standard.tm_mday, time_value.hour(),
                                     time_value.minute(), time_value.second(), 0, 0, 0))
    configuration.set_time_random_start(start_random_time)
    print(start_random_time)


def on_random_end_time_changed(time_value):
    # 输出改变的日期
    standard = time.localtime(Configuration.STANDARD_TIME)
    end_random_time = time.mktime((standard.tm_year, standard.tm_mon, standard.tm_mday, time_value.hour(),
                                   time_value.minute(), time_value.second(), 0, 0, 0))
    configuration.set_time_random_end(end_random_time)
    print(end_random_time)


def on_folder_selected(main_ui):
    root = QFileDialog.getExistingDirectory()
    main_ui.folder.setText(root)


def on_folder_change(value):
    configuration.set_root(value)
    print(value)


def on_run():
    msg = is_valid_param()
    if len(msg) == 0:
        configuration.calculation_time_random_delta()
        has_failed = start_walk()
        if not has_failed:
            QMessageBox(QMessageBox.Question, '恭喜', "全部完成").exec()
        pass
    else:
        QMessageBox(QMessageBox.Question, '异常', msg).exec()
        pass


def is_valid_param():
    delta = configuration.get_time_random_end() - configuration.get_time_random_start()
    root = configuration.get_root()
    isdir = os.path.isdir(root)
    if delta < 0:
        return "随机时刻结束值不能小于起始值"
    elif not isdir:
        return "文件夹路径异常"
    else:
        return ""


def start_walk():
    count = 0
    has_filed = False
    all_files = None
    for root, dirs, files in os.walk(configuration.root):
        all_files = files
        break

    for file_name in all_files:
        path_abs = os.path.join(configuration.root, file_name)

        file_name = path_abs
        start_time = configuration.get_start_day()
        add_time = configuration.get_increment_day_mktime() * count
        rand_time = configuration.get_random_delta()
        result = int(start_time) + int(add_time) + int(rand_time)
        print(time.localtime(result))
        result_time = time.localtime(result)
        code = modify_file_all_time(file_name, result_time)
        print(code)
        if code == 1:
            has_filed = True
        count = count + 1
    return has_filed


def modify_file_all_time(filePath, createTime):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    print(filePath, createTime)
    try:
        format = "%Y-%m-%d %H:%M:%S"  # 时间格式
        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)

        createTimes = Time(time.mktime(createTime))
        accessTimes = Time(time.mktime(createTime))
        modifyTimes = Time(time.mktime(createTime))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except Exception as e:
        print(e)
        return 1


configuration = Configuration()


def init_data(ui):
    ui.start_day.setDate(QDate.currentDate())
    ui.interval.setValue(1)
    ui.random_time_start.setTime(QTime(17, 0, 0))
    ui.random_time_end.setTime(QTime(17, 0, 0))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    connect_event(ui)
    init_data(ui)

    MainWindow.show()
    sys.exit(app.exec_())
