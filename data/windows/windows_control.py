from PyQt6 import QtWidgets, QtGui
from data.ui.control import Ui_WindowControl
import data.windows.windows_sections
import data.windows.windows_usersControl
import data.windows.windows_logsView
from data.signals import Signals
from data.server_requests import ServerRequests
from data.add_logs import add_log
from data.active_session import Session
import sys

class WindowControl(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowControl()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.server_requests = ServerRequests()
        self.session = Session.get_instance()
        self.ui.btn_back.clicked.connect(self.show_windowSection)
        self.ui.btn_control_users.clicked.connect(self.show_windowUserControl)
        self.ui.btn_logs_editing.clicked.connect(self.show_windowLogsView)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.crit_failed_signal.connect(self.show_crit_error_message)


    def show_windowSection(self):
        self.close()
        global windowSection
        windowSection = data.windows.windows_sections.WindowSections()
        windowSection.show()


    def show_windowUserControl(self):
        self.close()
        global windowUserControl
        windowUserControl = data.windows.windows_usersControl.WindowUsersControl()
        windowUserControl.show()


    def show_windowLogsView(self):
        self.close()
        global windowLogsView
        windowLogsView = data.windows.windows_logsView.WindowLogsView()
        windowLogsView.show()


    def show_success_message(self, message):
        pass


    def show_error_message(self, message):
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def show_crit_error_message(self, message):
        QtWidgets.QMessageBox.information(self, "Ошибка", message)
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
