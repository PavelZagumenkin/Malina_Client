from PyQt6 import QtWidgets, QtGui
import data.windows.windows_logistics
import data.windows.windows_bakery
from data.ui.autoorders import Ui_WindowAutoOrders
from data.active_session import Session
from data.signals import Signals


class WindowAutoorders(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowAutoOrders()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.btn_bakery.clicked.connect(self.show_windowBakery)
        self.ui.btn_back.clicked.connect(self.show_windowLogistik)
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)


    def show_windowBakery(self):
        self.close()
        global windowBakery
        windowBakery = data.windows.windows_bakery.WindowBakery()
        windowBakery.show()


    # Закрываем выбор раздела, открываем окно выбора раздела логистики
    def show_windowLogistik(self):
        self.close()
        global windowLogistik
        windowLogistik = data.windows.windows_logistics.WindowLogistics()
        windowLogistik.show()


    def show_success_message(self, message):
        pass


    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def closeEvent(self, event):
        if event.spontaneous():
            self.logs.add_log(f"Пользователь {self.session.get_username()} вышел из системы.")
        event.accept()
