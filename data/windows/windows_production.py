from PyQt6 import QtWidgets, QtGui
import data.windows.windows_sections
from data.ui.production import Ui_WindowProduction
from data.windows.windows_nomenklatura import WindowNomenklatura
from data.windows.windows_view_tp import WindowTpView
from data.requests.db_requests import Database
import datetime
from data.active_session import Session
from data.signals import Signals


class WindowProduction(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowProduction()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.btn_tp.clicked.connect(self.show_windowViewTP)
        self.ui.btn_nomenklatura.clicked.connect(self.show_windowViewNomenklatura)
        self.ui.btn_back.clicked.connect(self.show_windowSection)
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)


    def show_windowViewTP(self):
        self.close()
        global windowViewTP
        windowViewTP = data.windows.windows_view_tp.WindowTpView()
        windowViewTP.show()


    def show_windowViewNomenklatura(self):
        self.close()
        global windowViewNomenklatura
        windowViewNomenklatura = data.windows.windows_nomenklatura.WindowNomenklatura()
        windowViewNomenklatura.show()


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


    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def closeEvent(self, event):
        if event.spontaneous():
            username = self.session.get_username()  # Получение имени пользователя из экземпляра класса Session
            logs_result = self.database.add_log(datetime.datetime.now().date(), datetime.datetime.now().time(),
                                            f"Пользователь {username} вышел из системы.")
            if "Лог записан" in logs_result:
                self.signals.success_signal.emit(logs_result)
            elif 'Ошибка работы' in logs_result:
                self.signals.error_DB_signal.emit(logs_result)
            else:
                self.signals.failed_signal.emit(logs_result)
        event.accept()
