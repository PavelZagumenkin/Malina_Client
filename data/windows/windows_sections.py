from PyQt6 import QtWidgets, QtGui
from data.ui.sections import Ui_WindowSections
from data.active_session import Session
import data.windows.windows_authorization
import data.windows.windows_control
import data.windows.windows_logistics
import data.windows.windows_production
from data.requests.db_requests import Database
from data.signals import Signals
import datetime



class WindowSections(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowSections()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        role = self.session.get_role()  # Получение роли пользователя из экземпляра класса Session
        if role == 'operator':
            self.ui.btn_logistics.setEnabled(True)
        elif role == 'logist':
            self.ui.btn_logistics.setEnabled(True)
        elif role == 'supervisor':
            self.ui.btn_trade.setEnabled(True)
        elif role == 'manager':
            self.ui.btn_office.setEnabled(True)
        elif role == 'superadmin':
            self.ui.btn_logistics.setEnabled(True)
            self.ui.btn_trade.setEnabled(True)
            self.ui.btn_production.setEnabled(True)
            self.ui.btn_office.setEnabled(True)
            self.ui.btn_control.setEnabled(True)
        self.ui.btn_exit.clicked.connect(self.logout)
        self.ui.btn_logistics.clicked.connect(self.show_logistics)
        self.ui.btn_control.clicked.connect(self.show_control)
        self.ui.btn_production.clicked.connect(self.show_production)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)


    # Обработка выхода пользователя
    def logout(self):
        username = self.session.get_username()  # Получение имени пользователя из экземпляра класса Session
        logs_result = self.database.add_log(datetime.datetime.now().date(), datetime.datetime.now().time(),
                                            f"Пользователь {username} вышел из системы.")
        if "Лог записан" in logs_result:
            self.signals.success_signal.emit(logs_result)
        elif 'Ошибка работы' in logs_result:
            self.signals.error_DB_signal.emit(logs_result)
        else:
            self.signals.failed_signal.emit(logs_result)
        self.close()
        global windowLogin
        windowLogin = data.windows.windows_authorization.WindowAuthorization()
        windowLogin.show()
        windowLogin.ui.label_login_password.setFocus()  # Фокус по умолчанию на тексте
        windowLogin.ui.label_login_password.setStyleSheet("color: rgb(0, 0, 0)")
        windowLogin.ui.label_login_password.setText('Введите логин и пароль')
        windowLogin.ui.line_login.clear()
        windowLogin.ui.line_password.clear()


    # Закрываем выбор раздела, открываем выпечку
    def show_logistics(self):
        self.close()
        global WindowLogistics
        WindowLogistics = data.windows.windows_logistics.WindowLogistics()
        WindowLogistics.show()

    # Закрываем выбор раздела, открываем выпечку
    def show_production(self):
        self.close()
        global WindowProduction
        WindowProduction = data.windows.windows_production.WindowProduction()
        WindowProduction.show()


    # Закрываем выбор раздела, открываем выпечку
    def show_control(self):
        self.close()
        global WindowControl
        WindowControl = data.windows.windows_control.WindowControl()
        WindowControl.show()


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
