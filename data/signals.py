from PyQt6.QtCore import QObject, pyqtSignal

class Signals(QObject):
    error_DB_signal = pyqtSignal(str)
    success_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)