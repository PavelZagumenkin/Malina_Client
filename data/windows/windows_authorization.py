from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from data.ui.authorization import Ui_WindowAuthorization
from data.signals import Signals
from data.active_session import Session
from data.add_logs import add_log
from data.server_requests import ServerRequests
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
        self.server_requests = ServerRequests()
        self.ui.label_login_password.setFocus()
        self.ui.btn_login.clicked.connect(self.login)
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.crit_failed_signal.connect(self.show_crit_error_message)
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
        data_server = self.server_requests.post('check_version', {"version": version})
        if 'Критическая ошибка' in data_server['result']:
            self.signals.crit_failed_signal.emit(data_server['result'])
        else:
            result = data_server['result']
            actual_version = data_server['actual_version']
            if "Необходимо обновить приложение до версии" in result:
                self.dialog_need_update(actual_version)


    def dialog_need_update(self, actual_version):
        self.setEnabled(False)
        self.dialogBox_need_update = QMessageBox()
        self.dialogBox_need_update.setText(f"Требуется обновление клиента программы до версии {actual_version}. "
                                           f"Выполнить обновление сейчас?")
        self.dialogBox_need_update.setWindowIcon(QtGui.QIcon("data/images/icon.png"))
        self.dialogBox_need_update.setWindowTitle('Вышла новая версия программы')
        self.dialogBox_need_update.setIcon(QMessageBox.Icon.Critical)
        self.dialogBox_need_update.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.dialogBox_need_update.buttonClicked.connect(self.upload_file_update)
        self.dialogBox_need_update.exec()

    def upload_file_update(self, button):
        if button.text() == "OK":
            self.progress_bar.show()
            url = 'http://localhost:5000/get_update'  # URL для получения обновления
            file_name = 'Malina64_Setup.exe'
            try:
                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                chunk_size = 5242880
                downloaded_size = 0
                with open(file_name, 'wb') as file:
                    for data_size in response.iter_content(chunk_size=chunk_size):
                        file.write(data_size)
                        downloaded_size += len(data_size)
                        progress = int((downloaded_size / total_size) * 100)
                        self.progress_bar.setValue(progress)
                if total_size > 0 and downloaded_size == total_size:
                    print('\nФайл обновлений успешно скачан.')
                else:
                    self.signals.failed_signal.emit(
                        f'\nОшибка при скачивании файла. Загружено {downloaded_size / 1024:.2f} КБ из {total_size / 1024:.2f} КБ')
                self.progress_bar.hide()
                self.start_update(file_name)
            except Exception as e:
                self.signals.failed_signal.emit(f'Ошибка при скачивании файла: {str(e)}')
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
        # Отправляем POST-запрос на сервер для входа
        data_server = self.server_requests.post('login', {"username": username, "password": password})
        if 'Критическая ошибка' in data_server['result']:
            self.signals.crit_failed_signal.emit(data_server['result'])
        # Получаем результат и роль из ответа
        result = data_server.get('result')
        role = data_server.get('role')
        # Обрабатываем ответ
        if "Авторизация успешна" in result:
            logs_result = add_log(f"Пользователь {username} выполнил вход в систему.")
            if "Лог записан" in logs_result['result']:
                self.session.set_username_role_date(username, role, datetime.datetime.now().strftime('%Y.%m.%d'))
                self.show_windowSection()
            elif 'Критическая ошибка' in logs_result['result']:
                self.signals.crit_failed_signal.emit(logs_result['result'])
            else:
                self.signals.failed_signal.emit(logs_result['result'])
        else:
            if len(username) == 0:
                self.signals.failed_signal.emit("Введите логин")
            elif len(password) == 0:
                self.signals.failed_signal.emit("Введите пароль")
            else:
                self.signals.failed_signal.emit(result)

    def get_users_role(self):
        data_server = self.server_requests.post('get_users_role')
        return data_server['result']

    def count_row_in_DB_user_role(self):
        data_server = self.server_requests.post('count_row_in_DB_user_role')
        return data_server['result']

    def show_success_message(self, message):
        pass

    def show_crit_error_message(self, message):
        QtWidgets.QMessageBox.information(self, "Критическая ошибка", message)
        sys.exit()

    def show_error_message(self, message):
        if "Введите логин" in message or "Введите пароль" in message:
            self.ui.label_login_password.setText(message)
            self.ui.label_login_password.setStyleSheet('color: rgba(228, 107, 134, 1)')
        elif "Неверный логин или пароль" in message:
            self.ui.label_login_password.setText(message)
            self.ui.label_login_password.setStyleSheet('color: rgba(228, 107, 134, 1)')


    def show_windowSection(self):
        # Отображаем главное окно приложения
        self.close()
        global windowSection
        windowSection = data.windows.windows_sections.WindowSections()
        windowSection.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.ui.btn_login.click()  # Имитируем нажатие кнопки btn_login
