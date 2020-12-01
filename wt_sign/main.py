import os
import sys
import threading
import time

import win32clipboard
import win32con

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QFileSystemModel, QApplication, QHeaderView

from wt_sign.Logger import Logger
from wt_sign.task import Task
from wt_sign.ui2 import Ui_MainWindow

PLATFORMS = ["C211EV", "C211EVL", "F202", "F202U", "HY_M3N", "MTK2712", "NS2.0R_D", "OpenOS", "S111_MCA", "S202",
             "S202DA", "S202M", "S202_ICA", "S203", "S203EV", "S302_ICA", "S311CR", "S311R", "S311Z", "S311_ICA",
             "S311_MCA", "S820A", "Speech_SDK", "SX1.5", "TOS", "WT1.5R", "WT1.5R_MONTH", "WT1.5R_Q", "WT1.5R_S203EV",
             "WT2.0R", "WT2.0R_H", "WT2.0R_Q", "WT3.0R", "WT3.0R_VM", "WT30P_MV", "WTOSFramework", "WT_OpenOSSDK",
             "X70", "ALL", "A12", "A18", "A39", "A77", "A86", "Audi_Cluster35", "Audi_SOP", "C490", "S111", "S111_ICA",
             "S201", "S201_DMAP", "S302", "S311", "S311Y"]
US = ["user", "debug"]

logger = Logger()


def initUI():
    UI.mode = QFileSystemModel()
    UI.mode.setRootPath('.')
    UI.mode.setNameFilters(['*.apk'])
    UI.mode.setNameFilterDisables(False)

    UI.input.setModel(UI.mode)
    UI.input.setAnimated(False)
    UI.input.setIndentation(20)
    UI.input.setSortingEnabled(True)
    UI.input.setWindowTitle("Dir View")
    UI.input.hideColumn(1)
    UI.input.hideColumn(2)
    UI.input.header().setSectionResizeMode(QHeaderView.ResizeToContents)
    UI.sign.clicked.connect(do_sign)

    UI.output_mode = QFileSystemModel()
    UI.output_mode.setRootPath(QDir.currentPath())
    UI.output_mode.setNameFilters(['*.apk'])
    UI.output_mode.setNameFilterDisables(False)
    UI.output_mode.setNameFilterDisables(False)
    UI.output.setModel(UI.output_mode)
    UI.output.hideColumn(1)
    UI.output.hideColumn(2)

    # 这里要先设置mode然后再切换index
    UI.output.setRootIndex(UI.output_mode.index(QDir.currentPath()))
    UI.output.setAnimated(False)
    UI.output.setIndentation(20)
    UI.output.setSortingEnabled(True)
    UI.output.setWindowTitle("Dir View")
    UI.output.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    UI.input.setContextMenuPolicy(Qt.CustomContextMenu)
    UI.input.customContextMenuRequested['QPoint'].connect(lambda: show_context_menu(UI.input))
    UI.output.setContextMenuPolicy(Qt.CustomContextMenu)
    UI.output.customContextMenuRequested['QPoint'].connect(lambda: show_context_menu(UI.output))

    UI.install.clicked.connect(do_install)

    UI.platform.addItem("平台", "hint")
    for p in PLATFORMS:
        UI.platform.addItem(p, p)
    for u in US:
        UI.us.addItem(u, u)
    logger.breakSignal.connect(log_to_UI)


def show_context_menu(treeview):
    target = get_selected(treeview=treeview)
    if not is_Apk_path(target):
        return
    menubar = QtWidgets.QMenuBar(UI.input)
    menubar.setGeometry(QtCore.QRect(0, 0, 1148, 22))
    menubar.setObjectName("menubar")
    rightMenu = QtWidgets.QMenu(menubar)

    # copy_action = QtWidgets.QAction(UI.input)
    # copy_action.setObjectName("copy")
    # copy_action.setText(QtCore.QCoreApplication.translate("MainWindow", "复制"))
    # rightMenu.addAction(copy_action)

    delete_action = QtWidgets.QAction(UI.input)
    delete_action.setObjectName("delete")
    delete_action.setText(QtCore.QCoreApplication.translate("MainWindow", "删除"))
    rightMenu.addAction(delete_action)
    # copy_action.triggered.connect(lambda: copy_selected(target))
    delete_action.triggered.connect(lambda: delete_selected(target))
    rightMenu.exec_(QtGui.QCursor.pos())
    pass


def is_Apk_path(path):
    filename = os.path.split(path)[-1]
    if os.path.splitext(filename)[1] != ".apk" and os.path.splitext(filename)[1] != ".APK":
        return False
    return True


def get_item():
    return get_input_abspath()


def delete_selected(target):
    if not is_Apk_path(target):
        return
    log_to_UI("删除:" + target)
    os.unlink(target)
    pass


def copy_selected(target):
    print(target)
    win32clipboard.OpenClipboard()
    print(win32clipboard.GetClipboardData())
    win32clipboard.CloseClipboard()


def do_sign():
    if not pre_check():
        return

    src = get_input_abspath()
    filename = os.path.split(src)[-1]
    if os.path.splitext(filename)[1] != ".apk" and os.path.splitext(filename)[1] != ".APK":
        log_to_UI("请在左侧选择正确apk文件!!!")
        return

    dest = get_output_abspath(filename)
    print(dest)
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


def get_selected(treeview):
    current = treeview.currentIndex()
    path = treeview.model().filePath(current)
    print(path)
    return path


def get_input_abspath():
    current = UI.input.currentIndex()
    path = UI.input.model().filePath(current)
    print(path)
    return path


def get_output_abspath(input_name):
    platform = UI.platform.currentText()
    u = UI.us.currentText()
    child_dir = UI.child_dirs.text().strip()
    print(os.path.exists(child_dir))
    if not os.path.exists(child_dir) and len(child_dir) != 0:
        print("不存在")
        os.makedirs(child_dir)
    else:
        print("存在")
    return os.path.join(child_dir, build_out_file_name(input_name, platform, u))


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
            if kwargs['value'] == 0:
                logger.log("安装完成!!!")
            else:
                logger.log("操作失败，请确保安装的apk和对应的rom签名一致，版本高低，必要时可以用终端验证")
        elif kwargs['name'] == "sign":
            if kwargs['value'] == 0:
                logger.log("签名完成!!!")
            else:
                logger.log("签名失败,请检查网络环境是否处于内网状态...")


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


PATH = "C:\Windows\System32\sign_key_client_win.exe"


def set_up_tool():
    print(os.path.exists(PATH))  # True/False
    if not os.path.exists(PATH):
        copy_tool()


def copy_tool():
    try:
        data = None
        with open("tool.py", 'rb') as f:
            data = f.read()
        with open(PATH, 'wb') as f2:
            f2.write(data)
    except:
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    UI = Ui_MainWindow()
    UI.setupUi(MainWindow)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
    MainWindow.show()
    initUI()
    set_up_tool()
    sys.exit(app.exec_())
