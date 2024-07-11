from PyQt6 import QtWidgets, QtGui
import data.windows.windows_production
import data.windows.windows_dishes
from data.ui.nomenklatura import Ui_WindowNomenklatura
from data.active_session import Session
from data.signals import Signals
from data.server_requests import ServerRequests
from data.add_logs import add_log
import sys


class WindowNomenklatura(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowNomenklatura()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.server_requests = ServerRequests()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.btn_dishe.clicked.connect(self.show_windowDishe)
        self.ui.btn_back.clicked.connect(self.show_windowProduction)
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.crit_failed_signal.connect(self.show_crit_error_message)


    # Закрываем выбор раздела, открываем окно выбора секции
    def show_windowProduction(self):
        self.close()
        global windowProduction
        windowProduction = data.windows.windows_production.WindowProduction()
        windowProduction.show()

    # Закрываем выбор раздела, открываем окно с таблицей блюд
    def show_windowDishe(self):
        self.close()
        global windowDishe
        windowDishe = data.windows.windows_dishes.WindowDishes()
        windowDishe.show()


    def show_success_message(self, message):
        pass


    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def show_crit_error_message(self, message):
        QtWidgets.QMessageBox.information(self, "Критическая ошибка", message)
        sys.exit()


    def closeEvent(self, event):
        if event.spontaneous():
            logs_result = add_log(f"Пользователь {self.session.get_username()} вышел из системы.")
            if "Лог записан" in logs_result['result']:
                self.signals.success_signal.emit(logs_result['result'])
                self.close()
            elif 'Критическая ошибка' in logs_result['result']:
                self.signals.crit_failed_signal.emit(logs_result['result'])
            else:
                self.signals.failed_signal.emit(logs_result['result'])
        event.accept()
