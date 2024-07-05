from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from data.ui.authorization import Ui_WindowAuthorization
from data.requests.db_requests import Database
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
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        self.ui.label_login_password.setFocus()  # Фокус по умолчанию на тексте
        self.ui.btn_login.clicked.connect(self.login)
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)
        # Устанавливаем иконку
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        # Добавляем картинку
        self.label_logo_721 = QtWidgets.QLabel(parent=self.ui.centralwidget)
        self.label_logo_721.setGeometry(QtCore.QRect(0, 0, 731, 721))
        self.label_logo_721.setText("")
        self.label_logo_721.setPixmap(QtGui.QPixmap("data/images/logo_721.png"))
        self.label_logo_721.setScaledContents(False)
        self.label_logo_721.setObjectName("label_logo_721")
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setGeometry(140, 200, 1000, 50)  # Устанавливаем положение и размеры прогресс-бара
        self.progress_bar.hide()


    def check_update(self):
        version = self.ui.label_version_number.text()
        update_result, actual_version = self.database.check_version(version)
        if "Необходимо обновить приложение до версии" in update_result:
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
            # URL, откуда нужно скачать исполняемый файл
            url = 'http://88.147.144.216:55667/Malina64_Update/Malina64_Setup.exe'
            # Имя, под которым сохранить файл
            file_name = 'Malina64_Setup.exe'
            # Создаем сессию для управления соединением
            session = requests.Session()
            response = session.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))  # Общий размер файла
            chunk_size = 5242880  # Размер куска данных
            downloaded_size = 0
            with open(file_name, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    downloaded_size += len(data)
                    progress = int((downloaded_size / total_size) * 100)
                    self.progress_bar.setValue(progress)
            # Проверяем, что файл успешно скачан
            if total_size > 0 and downloaded_size == total_size:
                print('\nФайл обновлений успешно скачан.')
            else:
                self.signals.failed_signal.emit(f'\nОшибка при скачивании файла. Загружено {downloaded_size / 1024:.2f} КБ из {total_size / 1024:.2f} КБ')
            self.progress_bar.hide()
            self.start_update(file_name)
        else:
            sys.exit()


    def start_update(self, file_name):
        # Запуск исполняемого файла
        try:
            subprocess.Popen([file_name])
            sys.exit()
        except Exception as e:
            self.signals.failed_signal.emit(f'Произошла ошибка при запуске файла: {e}')


    def login(self):
        # Получаем данные из полей ввода
        username = self.ui.line_login.text()
        password = self.ui.line_password.text()
        # Выполняем авторизацию в базе данных и отправляем соответствующий сигнал
        login_result = self.database.login(username, password)
        if isinstance(login_result, tuple) and len(login_result) == 2:
            result, role = login_result
            if "Авторизация успешна" in result:
                logs_result = self.database.add_log(datetime.datetime.now().date(), datetime.datetime.now().time(),
                                      f"Пользователь {username} выполнил вход в систему.")
                if "Лог записан" in logs_result:
                    self.session.set_username_role_date(username, role, datetime.datetime.now().strftime('%Y.%m.%d'))  # сохраняем пользователя, роль пользователя, текущую дату в объекте UserSession
                    self.signals.success_signal.emit(result)
                elif 'Ошибка работы' in logs_result:
                    self.signals.error_DB_signal.emit(logs_result)
                else:
                    self.signals.failed_signal.emit(logs_result)
            else:
                if len(username) == 0:
                    self.signals.failed_signal.emit("Введите логин")
                elif len(password) == 0:
                    self.signals.failed_signal.emit("Введите пароль")
                else:
                    if 'Ошибка работы' in result:
                        self.signals.error_DB_signal.emit(result)
                    else:
                        self.signals.failed_signal.emit(result)
        else:
            self.signals.error_DB_signal.emit('Ошибка Базы данных')


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