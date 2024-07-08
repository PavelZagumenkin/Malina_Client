from PyQt6 import QtWidgets, QtGui
import data.windows.windows_sections
import data.windows.windows_autoorders
import data.windows.windows_konditerskie
from data.ui.logistics import Ui_WindowLogistics
from data.active_session import Session
from data.signals import Signals
from data.server_requests import ServerRequests
from data.add_logs import add_log
import sys


class WindowLogistics(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowLogistics()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.server_requests = ServerRequests()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.btn_autoorders.clicked.connect(self.show_windowAutoorders)
        self.ui.btn_konditerskie.clicked.connect(self.show_windowKonditerskie)
        self.ui.btn_back.clicked.connect(self.show_windowSection)
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.crit_failed_signal.connect(self.show_crit_error_message)


    def show_windowAutoorders(self):
        self.close()
        global windowAutoorders
        windowAutoorders = data.windows.windows_autoorders.WindowAutoorders()
        windowAutoorders.show()


    def show_windowKonditerskie(self):
        self.close()
        global windowKonditerskie
        windowKonditerskie = data.windows.windows_konditerskie.WindowKonditerskie()
        windowKonditerskie.show()


    # Закрываем выбор раздела, открываем окно выбора секции
    def show_windowSection(self):
        self.close()
        global windowSection
        windowSection = data.windows.windows_sections.WindowSections()
        windowSection.show()


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
