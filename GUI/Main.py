import base64
import os
import sys
from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from GUI.Configuration import Configuration
from GUI.root_ui import Ui_MainWindow
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time, datetime
import win32timezone


def connect_event(main_ui):
    """
    连接信号注册监听
    """
    main_ui.start_day.dateChanged.connect(on_date_changed)  # 开始时间改变监听
    main_ui.interval.valueChanged.connect(on_interval_changed)  # 周期时间改变监听
    main_ui.random_time_start.timeChanged.connect(on_random_start_time_changed)  # 随机时刻起点改变监听
    main_ui.random_time_end.timeChanged.connect(on_random_end_time_changed)  # 随机时刻终点改变监听
    main_ui.folder.textChanged.connect(on_folder_changed)  # 文件路径改变监听
    main_ui.set_folder.clicked.connect(partial(on_folder_selected, main_ui))  # 选择文件夹按钮监听
    main_ui.run.clicked.connect(on_run)  # 执行按钮监听


def on_date_changed(date):
    """
    日期控件变化回调
    :param date: QDate
    :return: None
    """
    start_date = time.mktime((date.year(), date.month(), date.day(), 0, 0, 0, 0, 0, 0))
    configuration.set_start_day(start_date)
    print(start_date)


def on_interval_changed(value):
    """
    周期日期变化回调
    :param value:变化值
    :return: None
    """
    configuration.set_increment_day(value)
    print(time.localtime(Configuration.STANDARD_TIME))


def on_random_start_time_changed(time_value):
    """
    start控件 时间选择器变化回调
    :param time_value:QTime
    :return: None
    """
    standard = time.localtime(Configuration.STANDARD_TIME)
    start_random_time = time.mktime((standard.tm_year, standard.tm_mon, standard.tm_mday, time_value.hour(),
                                     time_value.minute(), time_value.second(), 0, 0, 0))
    configuration.set_time_random_start(start_random_time)
    print(start_random_time)


def on_random_end_time_changed(time_value):
    """
    end控件 时间选择器变化回调
    :param time_value:QTime
    :return: None
    """
    standard = time.localtime(Configuration.STANDARD_TIME)
    end_random_time = time.mktime((standard.tm_year, standard.tm_mon, standard.tm_mday, time_value.hour(),
                                   time_value.minute(), time_value.second(), 0, 0, 0))
    configuration.set_time_random_end(end_random_time)
    print(end_random_time)


def on_folder_selected(main_ui):
    """
    文件选择按钮点击
    :param main_ui: 主UI
    :return: None
    """
    root = QFileDialog.getExistingDirectory()
    # 设置文件路径编辑框，触发回调
    main_ui.folder.setText(root)


def on_folder_changed(value):
    """
    文件夹路径变化回调
    :param value: 文件夹路径
    :return:
    """
    configuration.set_root(value)
    print(value)


def on_run():
    """
    点击按钮，开始执行
    :return:
    """
    msg = is_valid_param()
    if len(msg) == 0:
        configuration.calculation_time_random_delta()
        has_failed = start_walk()
        if not has_failed:
            QMessageBox(QMessageBox.Warning, '恭喜', "全部完成").exec()
        pass
    else:
        QMessageBox(QMessageBox.Information, '异常', msg).exec()
        pass


def is_valid_param():
    """
    检测参数是否合法
    :return: 异常：异常信息 否则：空字符
    """
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
    """
    开始遍历文件夹，并且开始执行修改操作
    :return:
    """
    count = 0
    has_filed = False
    all_files = None
    for root, dirs, files in os.walk(configuration.root):
        all_files = files
        break

    for file_name in all_files:
        path_abs = os.path.join(configuration.root, file_name)
        file_name = path_abs
        # 获取开始时间的时间戳
        start_time = configuration.get_start_day()
        # 获取周期性的增加时间戳 如果1天，就是1天的秒数
        add_time = configuration.get_increment_day_mktime() * count
        # 获取当天的随机时刻
        rand_time = configuration.get_random_delta()
        # 计算出当天的时间戳秒
        result = int(start_time) + int(add_time) + int(rand_time)
        print(time.localtime(result))
        # 转换时间戳秒为时间对象
        result_time = time.localtime(result)
        # 执行修改
        code = modify_file_all_time(file_name, result_time)
        print(code)
        if code == 1:
            has_filed = True
        count = count + 1
    return has_filed


def modify_file_all_time(file_path, create_time):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param file_path: 文件路径名
    :param create_time: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    print(file_path, create_time)
    try:
        fh = CreateFile(file_path, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)

        final_create_time = Time(time.mktime(create_time))
        final_access_time = Time(time.mktime(create_time))
        final_modify_time = Time(time.mktime(create_time))
        SetFileTime(fh, final_create_time, final_access_time, final_modify_time)
        CloseHandle(fh)
        return 0
    except Exception as e:
        print(e)
        return 1


def init_data(root_ui):
    root_ui.start_day.setDate(QDate.currentDate())
    root_ui.interval.setValue(1)
    root_ui.random_time_start.setTime(QTime(17, 0, 0))
    root_ui.random_time_end.setTime(QTime(17, 0, 0))


configuration = Configuration()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
    ui.start_day.setCalendarPopup(True)
    connect_event(ui)
    init_data(ui)
    MainWindow.show()
    sys.exit(app.exec_())
