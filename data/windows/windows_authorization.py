from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from data.ui.authorization import Ui_WindowAuthorization
from data.signals import Signals
from data.active_session import Session
import data.windows.windows_sections
import datetime
import requests
import subprocess
import sys

class WindowAuthorization(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowAuthorization()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.session = Session.get_instance()
        self.ui.label_login_password.setFocus()
        self.ui.btn_login.clicked.connect(self.login)
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.label_logo_721 = QtWidgets.QLabel(parent=self.ui.centralwidget)
        self.label_logo_721.setGeometry(QtCore.QRect(0, 0, 731, 721))
        self.label_logo_721.setText("")
        self.label_logo_721.setPixmap(QtGui.QPixmap("data/images/logo_721.png"))
        self.label_logo_721.setScaledContents(False)
        self.label_logo_721.setObjectName("label_logo_721")
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setGeometry(140, 200, 1000, 50)
        self.progress_bar.hide()

    def check_update(self):
        version = self.ui.label_version_number.text()
        response = requests.post('http://localhost:5000/check_version', json={"version": version})
        if response.status_code == 200:
            data = response.json()
            result = data['result']
            actual_version = data['actual_version']
            if "Необходимо обновить приложение до версии" in result:
                self.dialog_need_update(actual_version)

    def dialog_need_update(self, actual_version):
        self.setEnabled(False)
        self.dialogBox_need_update = QMessageBox()
        self.dialogBox_need_update.setText(f"Требуется обновление клиента программы до версии {actual_version}. Выполнить обновление сейчас?")
        self.dialogBox_need_update.setWindowIcon(QtGui.QIcon("data/images/icon.png"))
        self.dialogBox_need_update.setWindowTitle('Вышла новая версия программы')
        self.dialogBox_need_update.setIcon(QMessageBox.Icon.Critical)
        self.dialogBox_need_update.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.dialogBox_need_update.buttonClicked.connect(self.upload_file_update)
        self.dialogBox_need_update.exec()


    def upload_file_update(self, button):
        if button.text() == "OK":
            self.progress_bar.show()
            url = 'http://localhost:5000/update'  # URL на сервере для загрузки обновления
            file_name = 'Malina64_Setup.exe'
            try:
                with open(file_name, 'rb') as file:
                    files = {'file': (file_name, file, 'application/octet-stream')}
                    response = requests.post(url, files=files)
                    if response.status_code == 200:
                        print('\nФайл обновлений успешно загружен на сервер.')
                        self.start_update(file_name)
                    else:
                        self.signals.failed_signal.emit('Ошибка при загрузке файла на сервер.')
            except Exception as e:
                self.signals.failed_signal.emit(f'Ошибка при считывании файла: {str(e)}')
                self.progress_bar.hide()
        else:
            sys.exit()

    def start_update(self, file_name):
        try:
            subprocess.Popen([file_name])
            sys.exit()
        except Exception as e:
            self.signals.failed_signal.emit(f'Произошла ошибка при запуске файла: {str(e)}')

    def login(self):
        username = self.ui.line_login.text()
        password = self.ui.line_password.text()
        response = requests.post('http://localhost:5000/login', json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            result = data['result']
            role = data['role']
            if "Авторизация успешна" in result:
                logs_result = self.add_log(f"Пользователь {username} выполнил вход в систему.")
                if "Лог записан" in logs_result:
                    self.session.set_username_role_date(username, role, datetime.datetime.now().strftime('%Y.%m.%d'))
                    self.signals.success_signal.emit(result)
                else:
                    self.signals.failed_signal.emit(logs_result)
            else:
                self.signals.failed_signal.emit(result)
        else:
            self.signals.failed_signal.emit('Ошибка при выполнении запроса на сервере.')

    def add_log(self, log):
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        response = requests.post('http://localhost:5000/add_log', json={"date": str(date), "time": str(time), "log": log})
        if response.status_code == 200:
            data = response.json()
            return data['result']
        else:
            return 'Ошибка при записи лога на сервере.'

    def get_users_role(self):
        response = requests.get('http://localhost:5000/get_users_role')
        if response.status_code == 200:
            data = response.json()
            return data['result']
        else:
            return 'Ошибка при получении ролей пользователей с сервера.'

    def count_row_in_DB_user_role(self):
        response = requests.get('http://localhost:5000/count_row_in_DB_user_role')
        if response.status_code == 200:
            data = response.json()
            return data['result']
        else:
            return 'Ошибка при получении количества строк в таблице пользователей с сервера.'


    def show_success_message(self, message):
        if "Авторизация успешна" in message:
            self.show_windowSection()


    def show_error_message(self, message):
        if "Введите логин" in message or "Введите пароль" in message:
            self.ui.label_login_password.setText(message)
            self.ui.label_login_password.setStyleSheet('color: rgba(228, 107, 134, 1)')
        else:
            # Отображаем сообщение об ошибке
            QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def show_windowSection(self):
        # Отображаем главное окно приложения
        self.close()
        global windowSection
        windowSection = data.windows.windows_sections.WindowSections()
        windowSection.show()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.ui.btn_login.click()  # Имитируем нажатие кнопки btn_login