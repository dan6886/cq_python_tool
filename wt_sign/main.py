import os
import sys
import threading
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir, pyqtSignal
from PyQt5.QtWidgets import QFileSystemModel, QApplication
from PyQt5.uic.properties import QtGui

from wt_sign.Logger import Logger
from wt_sign.task import Task
from wt_sign.ui2 import Ui_MainWindow

PLATFORMS = ["S311_ICA", "S111_MCA"]
US = ["user", "debug"]

logger = Logger()


def initUI():
    UI.mode = QFileSystemModel()
    UI.mode.setRootPath('.')
    UI.input.setModel(UI.mode)
    UI.input.setAnimated(False)
    UI.input.setIndentation(20)
    UI.input.setSortingEnabled(True)
    UI.input.setWindowTitle("Dir View")
    UI.sign.clicked.connect(do_sign)

    UI.output_mode = QFileSystemModel()
    UI.output_mode.setRootPath(QDir.currentPath())
    UI.output_mode.setNameFilters(['*.apk'])
    UI.output_mode.setNameFilterDisables(False)
    UI.output.setModel(UI.output_mode)
    # 这里要先设置mode然后再切换index
    UI.output.setRootIndex(UI.output_mode.index(QDir.currentPath()))
    UI.output.setAnimated(False)
    UI.output.setIndentation(20)
    UI.output.setSortingEnabled(True)
    UI.output.setWindowTitle("Dir View")
    UI.install.clicked.connect(do_install)

    UI.platform.addItem("平台", "hint")
    for p in PLATFORMS:
        UI.platform.addItem(p, p)
    for u in US:
        UI.us.addItem(u, u)
    logger.breakSignal.connect(log_to_UI)


def do_sign():
    if not pre_check():
        return

    src = get_input_abspath()
    filename = os.path.split(src)[-1]
    if os.path.splitext(filename)[1] != ".apk" and os.path.splitext(filename)[1] != ".APK":
        log_to_UI("请选择正确apk文件!!!")
        return

    dest = get_output_abspath(filename)
    p = UI.platform.currentText()
    u = UI.us.currentText()
    cmd = "sign_key_client_win.exe -p {p} -v {u} -f {input_file} -o {output_file}".format(p=p, u=u, input_file=src,
                                                                                          output_file=dest)
    command(cmd=cmd, tag="sign")


def pre_check():
    platform = UI.platform.currentText()
    if platform not in PLATFORMS:
        log_to_UI("请选择一个合法的平台!!!")
        return False
    if isRunnig():
        log_to_UI("当前正在执行任务，请稍后...")
        return False

    return True


def isRunnig():
    return RUNNIG


def get_install_apk_path():
    current = UI.output.currentIndex()
    path = UI.output.model().filePath(current)
    print(path)
    return path


def do_install():
    if isRunnig():
        log_to_UI("当前正在执行任务，请稍后...")
        return
    if UI.output.currentIndex().data() == None:
        log_to_UI("请选择右侧一个apk安装")
        return
    path = get_install_apk_path()
    cmd = "adb install -r {output_file}".format(output_file=path)
    command(cmd=cmd, tag="install")


OUT_PATH = ""
PLATFORM = ""
us = "user"


def get_input_abspath():
    current = UI.input.currentIndex()
    path = UI.input.model().filePath(current)
    print(path)
    return path


def get_output_abspath(input_name):
    platform = UI.platform.currentText()
    u = UI.us.currentText()
    return build_out_file_name(input_name, platform, u)


def build_out_file_name(input_name, *args):
    names = input_name.split('.')
    return names[0] + "-" + "-".join(args) + "-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "." + names[
        -1]


def run_command(input_path, output_path):
    pass


def command(cmd, tag):
    task = Task(tag)
    task.set_callback(callback)
    task.set_cmd(cmd=cmd)
    task.start()


RUNNIG = False


def callback(**kwargs):
    t = kwargs['type']
    if t == "status":
        global RUNNIG
        RUNNIG = kwargs['value']
        logger.log(kwargs['name'] + "执行" + ("开始" if RUNNIG else "结束"))
        print(RUNNIG)
    elif t == "msg":
        logger.log(kwargs['value'])
    elif t == "result":
        if kwargs['name'] == "install":
            if kwargs['value'] == 1:
                logger.log("操作失败，请确保安装的apk和对应的rom签名一致，版本高低，必要时可以用终端验证")
            elif kwargs['value'] == 0:
                logger.log("安装完成!!!")
        elif kwargs['name'] == "sign":
            if kwargs['value'] == 1:
                logger.log("签名失败...")
            elif kwargs['value'] == 0:
                logger.log("签名完成!!!")


def log_to_UI(msg):
    refresh(msg)


def refresh(msg):
    print(threading.currentThread().name + ":" + msg)
    msg = threading.currentThread().name + ":" + msg
    UI.log.insertPlainText(msg)
    UI.log.insertPlainText("\n")
    cursor = UI.log.textCursor()
    UI.log.moveCursor(cursor.End)
    QApplication.processEvents()
    UI.log.repaint()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    UI = Ui_MainWindow()
    UI.setupUi(MainWindow)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
    MainWindow.show()
    initUI()
    sys.exit(app.exec_())
