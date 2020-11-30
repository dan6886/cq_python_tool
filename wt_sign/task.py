import os
import subprocess
import sys
from threading import Thread

from PyQt5.QtCore import pyqtSignal


class Task(Thread):

    def __init__(self, name):  # 可以通过初始化来传递参数
        super(Task, self).__init__()
        self.cmd = ""
        self.callback = None
        self.name = name

    def set_callback(self, callback):
        self.callback = callback

    def set_cmd(self, cmd):
        self.cmd = cmd

        pass

    def run(self):  # 必须有的函数
        self.callback(type="status", name=self.name, value=True)
        self.callback(type="msg", name=self.name, value=self.cmd)
        print(f"{self.name}开始执行：" + self.cmd)
        # p = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        # # for line in iter(p.stdout.readline, b''):
        # #     print(str(line))
        # p.stdout.close()
        # p.wait()
        # code = p.returncode
        # p.kill()
        r = os.system(command=self.cmd)
        print(r)
        self.callback(type="result", name=self.name, value=r)
        self.callback(type="status", name=self.name, value=False)
