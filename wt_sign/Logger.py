from PyQt5.QtCore import pyqtSignal, QObject


class Logger(QObject):
    breakSignal = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

    def log(self, msg):
        self.breakSignal.emit(msg)
        pass
