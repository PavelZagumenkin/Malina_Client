from PyQt6.QtCore import QObject, pyqtSignal

class Signals(QObject):
    success_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)
    crit_failed_signal = pyqtSignal(str)