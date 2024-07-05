from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QInputDialog, QMessageBox
from data.ui.mini_table_window import Ui_mini_table_window
from data.requests.db_requests import Database
from data.signals import Signals
import data.windows.windows_nomenklatura
from data.active_session import Session
import datetime

class WindowDishes(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mini_table_window()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        self.ui.btn_back.clicked.connect(self.show_windowNomenklatura)
        self.ui.label_windowName.setText('Список блюд')
        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_error_message)
        # Устанавливаем иконку
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        # Оформление
        self.font = QtGui.QFont()
        self.font.setFamily("Trebuchet MS")
        self.font.setBold(False)
        self.font.setWeight(50)
        self.font.setPointSize(14)
        # Распологаем кнопку "Назад"
        self.ui.btn_back.setGeometry(QtCore.QRect(910, 620, 346, 51))
        self.create_table()
        self.create_form_add_konditerskay()


    def create_table(self):
        self.ui.tableWidget.setMaximumWidth(887)
        self.ui.tableWidget.setMinimumWidth(887)
        self.ui.tableWidget.setMinimumHeight(590)
        self.ui.tableWidget.setMaximumHeight(590)
        self.ui.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.tableWidget.setRowCount(self.get_count_rows())
        self.ui.tableWidget.setColumnCount(10)
        self.columnName = ['АРТИКУЛ', 'НАИМЕНОВАНИЕ', 'КАТЕГОРИЯ БЛЮДА', 'ВЫКЛАДКА', 'КВАНТ', 'ЗАМЕС', 'СРОК ПО', 'ЦЕХ ПРОИЗВОДСТВА', 'ТЕХПРОЦЕСС', '', '']
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columnName)
        self.font_table = QtGui.QFont()
        self.font_table.setFamily("Trebuchet MS")
        self.font_table.setBold(False)
        self.font_table.setWeight(13)
        self.font_table.setPointSize(9)
        self.ui.tableWidget.horizontalHeader().setFont(self.font_table)
        self.ui.tableWidget.verticalHeader().setFont(self.font_table)
        self.ui.tableWidget.setColumnWidth(0, 60)
        self.ui.tableWidget.setColumnWidth(1, 100)
        self.ui.tableWidget.setColumnWidth(2, 60)
        self.ui.tableWidget.setColumnWidth(3, 60)
        self.ui.tableWidget.setColumnWidth(4, 60)
        self.ui.tableWidget.setColumnWidth(5, 60)
        self.ui.tableWidget.setColumnWidth(6, 60)
        self.ui.tableWidget.setColumnWidth(7, 100)
        self.ui.tableWidget.setColumnWidth(8, 60)
        self.ui.tableWidget.setColumnWidth(9, 60)
        self.add_data_in_table()


    def create_form_add_konditerskay(self):
        # Создаем поле для названия кондитерской
        self.labelName_dishe = QtWidgets.QLabel(self.ui.centralwidget)
        self.labelName_dishe.setGeometry(QtCore.QRect(897, 80, 372, 20))
        self.labelName_dishe.setFont(self.font)
        self.labelName_dishe.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.labelName_dishe.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelName_dishe.setObjectName("label_add_konditerskay_text")
        self.labelName_dishe.setText("Добавление блюда")
        self.labelName_dishe.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelName_type_dishe = QtWidgets.QLabel(self.ui.centralwidget)
        self.labelName_type_dishe.setGeometry(QtCore.QRect(897, 190, 372, 20))
        self.labelName_type_dishe.setFont(self.font)
        self.labelName_type_dishe.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.labelName_type_dishe.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelName_type_dishe.setObjectName("labelName_type_dishe")
        self.labelName_type_dishe.setText("Тип блюда")
        self.labelName_type_dishe.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.line_name_konditeskay = QtWidgets.QLineEdit(self.ui.centralwidget)
        self.line_name_konditeskay.setGeometry(QtCore.QRect(910, 120, 346, 51))
        self.font = QtGui.QFont()
        self.font.setFamily("Trebuchet MS")
        self.font.setBold(False)
        self.font.setWeight(50)
        self.font.setPointSize(14)
        self.line_name_konditeskay.setFont(self.font)
        self.line_name_konditeskay.setTabletTracking(False)
        self.line_name_konditeskay.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.line_name_konditeskay.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.line_name_konditeskay.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.line_name_konditeskay.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.line_name_konditeskay.setMaxLength(24)
        self.line_name_konditeskay.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.line_name_konditeskay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.line_name_konditeskay.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.LogicalMoveStyle)
        self.line_name_konditeskay.setClearButtonEnabled(False)
        self.line_name_konditeskay.setObjectName("line_name_konditerskay")
        self.line_name_konditeskay.setPlaceholderText("Название кондитерской")
        # Создаем поле для выбора типа кондитерской
        self.line_type = QtWidgets.QComboBox(self.ui.centralwidget)
        self.line_type.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.line_type.setGeometry(QtCore.QRect(910, 225, 346, 51))
        self.line_type.setObjectName("line_type_konditerskoi")
        self.line_type.setStyleSheet(open('data/css/QComboBox.qss').read())
        self.line_type.setFont(self.font)
        self.listType = ['Дисконт', 'Магазин']
        self.line_type.addItems(self.listType)
        self.line_type.setCurrentIndex(1)
        self.line_type.currentIndexChanged.connect(self.on_line_type_changed)
        # Создаем чек-боксы пунктов
        self.checkbox_bakery = QtWidgets.QCheckBox(self.ui.centralwidget)
        self.checkbox_bakery.setGeometry(QtCore.QRect(910, 280, 173, 51))
        self.checkbox_bakery.setText('Печка')
        self.checkbox_bakery.setFont(self.font)
        self.checkbox_ice_sklad = QtWidgets.QCheckBox(self.ui.centralwidget)
        self.checkbox_ice_sklad.setGeometry(QtCore.QRect(1083, 280, 173, 51))
        self.checkbox_ice_sklad.setText('Мороз. склад')
        self.checkbox_ice_sklad.setFont(self.font)
        self.checkbox_vhod_group = QtWidgets.QCheckBox(self.ui.centralwidget)
        self.checkbox_vhod_group.setGeometry(QtCore.QRect(910, 331, 173, 51))
        self.checkbox_vhod_group.setText('Вх. группа')
        self.checkbox_vhod_group.setFont(self.font)
        self.checkbox_tualet = QtWidgets.QCheckBox(self.ui.centralwidget)
        self.checkbox_tualet.setGeometry(QtCore.QRect(1083, 331, 173, 51))
        self.checkbox_tualet.setText('Туалет')
        self.checkbox_tualet.setFont(self.font)
        self.checkbox_tables = QtWidgets.QCheckBox(self.ui.centralwidget)
        self.checkbox_tables.setGeometry(QtCore.QRect(910, 382, 173, 51))
        self.checkbox_tables.setText('Столики')
        self.checkbox_tables.setFont(self.font)
        self.checkbox_bakery_store = QtWidgets.QCheckBox(self.ui.centralwidget)
        self.checkbox_bakery_store.setGeometry(QtCore.QRect(1083, 382, 173, 51))
        self.checkbox_bakery_store.setText('Продает выпечку')
        self.checkbox_bakery_store.setFont(self.font)
        # Создаем кнопку регистрации новой кондитерской
        self.btn_reg = QtWidgets.QPushButton(self.ui.centralwidget)
        self.btn_reg.setGeometry(QtCore.QRect(910, 433, 346, 51))
        font_button = QtGui.QFont()
        font_button.setFamily("Trebuchet MS")
        font_button.setPointSize(16)
        font_button.setBold(False)
        font_button.setWeight(50)
        self.btn_reg.setFont(font_button)
        self.btn_reg.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.btn_reg.setStyleSheet(open('data/css/QPushButton.qss').read())
        self.btn_reg.setObjectName("btn_reg_konditerskay")
        self.btn_reg.setCheckable(False)
        self.btn_reg.setText('РЕГИСТРАЦИЯ')
        self.btn_reg.clicked.connect(self.register_konditerskay)


    def on_line_type_changed(self):
        if self.line_type.currentText() == "Дисконт":
            self.checkbox_bakery.setCheckable(False)
            self.checkbox_ice_sklad.setCheckable(False)
            self.checkbox_vhod_group.setCheckable(False)
            self.checkbox_tualet.setCheckable(False)
            self.checkbox_tables.setCheckable(False)
            self.checkbox_bakery_store.setCheckable(False)
            self.checkbox_bakery.setEnabled(False)
            self.checkbox_ice_sklad.setEnabled(False)
            self.checkbox_vhod_group.setEnabled(False)
            self.checkbox_tualet.setEnabled(False)
            self.checkbox_tables.setEnabled(False)
            self.checkbox_bakery_store.setEnabled(False)
        elif self.line_type.currentText() == "Магазин":
            self.checkbox_bakery.setCheckable(True)
            self.checkbox_ice_sklad.setCheckable(True)
            self.checkbox_vhod_group.setCheckable(True)
            self.checkbox_tualet.setCheckable(True)
            self.checkbox_tables.setCheckable(True)
            self.checkbox_bakery_store.setCheckable(True)
            self.checkbox_bakery.setEnabled(True)
            self.checkbox_ice_sklad.setEnabled(True)
            self.checkbox_vhod_group.setEnabled(True)
            self.checkbox_tualet.setEnabled(True)
            self.checkbox_tables.setEnabled(True)
            self.checkbox_bakery_store.setEnabled(True)


    def add_data_in_table(self):
        result = self.database.get_dishe_in_DB("Блюдо")
        if len(result) >= 1:
            if isinstance(result, list):
                for row in range(len(result)):
                    font = QtGui.QFont()
                    font.setFamily("Trebuchet MS")
                    font.setBold(False)
                    font.setWeight(50)
                    font.setPointSize(10)


                    self.button_save_changes = QtWidgets.QPushButton()
                    self.button_delete_dishes = QtWidgets.QPushButton()

                    self.line_combo_yes_no_bakery = QtWidgets.QComboBox()
                    self.line_combo_yes_no_ice_sklad = QtWidgets.QComboBox()
                    self.line_combo_yes_no_vhod_group = QtWidgets.QComboBox()
                    self.line_combo_yes_no_tualet = QtWidgets.QComboBox()
                    self.line_combo_yes_no_tables = QtWidgets.QComboBox()
                    self.line_combo_yes_no_enable = QtWidgets.QComboBox()
                    self.line_combo_bakery_store = QtWidgets.QComboBox()
                    self.line_combo_yes_no_bakery.setObjectName("line_yes_no")
                    self.line_combo_yes_no_ice_sklad.setObjectName("line_yes_no")
                    self.line_combo_yes_no_vhod_group.setObjectName("line_yes_no")
                    self.line_combo_yes_no_tualet.setObjectName("line_yes_no")
                    self.line_combo_yes_no_tables.setObjectName("line_yes_no")
                    self.line_combo_yes_no_enable.setObjectName("line_yes_no")
                    self.line_combo_bakery_store.setObjectName("line_yes_no")
                    self.line_combo_yes_no_bakery.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_combo_yes_no_ice_sklad.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_combo_yes_no_vhod_group.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_combo_yes_no_tualet.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_combo_yes_no_tables.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_combo_yes_no_enable.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_combo_bakery_store.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_combo_yes_no_bakery.setFont(font)
                    self.line_combo_yes_no_ice_sklad.setFont(font)
                    self.line_combo_yes_no_vhod_group.setFont(font)
                    self.line_combo_yes_no_tualet.setFont(font)
                    self.line_combo_yes_no_tables.setFont(font)
                    self.line_combo_yes_no_enable.setFont(font)
                    self.line_combo_bakery_store.setFont(font)
                    self.line_combo_yes_no_bakery.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_combo_yes_no_ice_sklad.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_combo_yes_no_vhod_group.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_combo_yes_no_tualet.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_combo_yes_no_tables.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_combo_yes_no_enable.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_combo_bakery_store.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_combo_yes_no_bakery.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.line_combo_yes_no_ice_sklad.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.line_combo_yes_no_vhod_group.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.line_combo_yes_no_tualet.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.line_combo_yes_no_tables.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.line_combo_yes_no_enable.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.line_combo_bakery_store.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.list_combo_yes_no = ['Нет', 'Да']
                    self.line_combo_yes_no_bakery.addItems(self.list_combo_yes_no)
                    self.line_combo_yes_no_ice_sklad.addItems(self.list_combo_yes_no)
                    self.line_combo_yes_no_vhod_group.addItems(self.list_combo_yes_no)
                    self.line_combo_yes_no_tualet.addItems(self.list_combo_yes_no)
                    self.line_combo_yes_no_tables.addItems(self.list_combo_yes_no)
                    self.line_combo_yes_no_enable.addItems(self.list_combo_yes_no)
                    self.line_combo_bakery_store.addItems(self.list_combo_yes_no)
                    self.line_combo_yes_no_bakery.wheelEvent = lambda event: None
                    self.line_combo_yes_no_ice_sklad.wheelEvent = lambda event: None
                    self.line_combo_yes_no_vhod_group.wheelEvent = lambda event: None
                    self.line_combo_yes_no_tualet.wheelEvent = lambda event: None
                    self.line_combo_yes_no_tables.wheelEvent = lambda event: None
                    self.line_combo_yes_no_enable.wheelEvent = lambda event: None
                    self.line_combo_bakery_store.wheelEvent = lambda event: None
                    self.line_type_table = QtWidgets.QComboBox()
                    self.line_type_table.setObjectName("line_type")
                    self.line_type_table.setStyleSheet(open('data/css/QComboBox.qss').read())
                    self.line_type_table.setFont(font)
                    self.line_type_table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_type_table.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.listType_table = ['Дисконт', 'Магазин']
                    self.line_type_table.addItems(self.listType_table)
                    self.line_type_table.wheelEvent = lambda event: None
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(result[row][1]))
                    self.ui.tableWidget.setCellWidget(row, 1, self.line_type_table)
                    self.ui.tableWidget.cellWidget(row, 1).setCurrentIndex(result[row][2])
                    self.ui.tableWidget.setCellWidget(row, 2, self.line_combo_yes_no_bakery)
                    self.ui.tableWidget.cellWidget(row, 2).setCurrentIndex(result[row][3])
                    self.ui.tableWidget.setCellWidget(row, 3, self.line_combo_bakery_store)
                    self.ui.tableWidget.cellWidget(row, 3).setCurrentIndex(result[row][9])
                    self.ui.tableWidget.setCellWidget(row, 4, self.line_combo_yes_no_ice_sklad)
                    self.ui.tableWidget.cellWidget(row, 4).setCurrentIndex(result[row][4])
                    self.ui.tableWidget.setCellWidget(row, 5, self.line_combo_yes_no_vhod_group)
                    self.ui.tableWidget.cellWidget(row, 5).setCurrentIndex(result[row][5])
                    self.ui.tableWidget.setCellWidget(row, 6, self.line_combo_yes_no_tualet)
                    self.ui.tableWidget.cellWidget(row, 6).setCurrentIndex(result[row][6])
                    self.ui.tableWidget.setCellWidget(row, 7, self.line_combo_yes_no_tables)
                    self.ui.tableWidget.cellWidget(row, 7).setCurrentIndex(result[row][7])
                    self.ui.tableWidget.setCellWidget(row, 8, self.line_combo_yes_no_enable)
                    self.ui.tableWidget.cellWidget(row, 8).setCurrentIndex(result[row][8])
                    self.ui.tableWidget.setCellWidget(row, 9, self.button_save_changes)
                    self.ui.tableWidget.cellWidget(row, 9).setText('Сохранить')
                    self.ui.tableWidget.cellWidget(row, 9).setStyleSheet(open('data/css/QPushButton.qss').read())
                    self.ui.tableWidget.cellWidget(row, 9).clicked.connect(self.update_konditerskay)
            else:
                self.signals.error_DB_signal.emit(result)
        else:
            self.signals.failed_signal.emit('Кондитерские не найдены!')


    def get_count_rows(self):
        count_rows = self.database.count_row_in_DB_dishes("Блюдо")
        if isinstance(count_rows, int):
            return count_rows
        else:
            self.signals.failed_signal.emit(count_rows)
            return 0


    def register_konditerskay(self):
        bakery = 0
        ice_sklad = 0
        vhod_group = 0
        tualet = 0
        tables = 0
        bakery_store = 0
        # Получаем данные из полей ввода
        konditerskay_name = self.line_name_konditeskay.text()
        if self.line_type.currentText() == "Магазин":
            konditerskay_type = 1
            if self.checkbox_bakery.isChecked():
                bakery = 1
            if self.checkbox_ice_sklad.isChecked():
                ice_sklad = 1
            if self.checkbox_vhod_group.isChecked():
                vhod_group = 1
            if self.checkbox_tualet.isChecked():
                tualet = 1
            if self.checkbox_tables.isChecked():
                tables = 1
            if self.checkbox_bakery_store.isChecked():
                bakery_store = 1
        else:
            konditerskay_type = 0

        if len(konditerskay_name) == 0:
            self.signals.failed_signal.emit("Введите название кондитерской")
        else:
            # Выполняем регистрацию в базе данных и отправляем соответствующий сигнал
            result = self.database.register_konditerskay(konditerskay_name, konditerskay_type, bakery, ice_sklad, vhod_group, tualet, tables, bakery_store)
            if "успешно зарегистрирована" in result:
                self.signals.success_signal.emit(result)
            else:
                if 'Ошибка работы' in result:
                    self.signals.error_DB_signal.emit(result)
                else:
                    self.signals.failed_signal.emit(result)


    def show_windowNomenklatura(self):
        # Отображаем главное окно приложения
        self.close()
        global windowNomenklatura
        windowNomenklatura = data.windows.windows_nomenklatura.WindowNomenklatura()
        windowNomenklatura.show()


    def update_konditerskay(self):
        buttonClicked = self.sender()
        index = self.ui.tableWidget.indexAt(buttonClicked.pos())
        konditerskay_name = self.ui.tableWidget.item(index.row(), 0).text()
        konditerskay_type = self.ui.tableWidget.cellWidget(index.row(), 1).currentIndex()
        konditerskay_bakery = self.ui.tableWidget.cellWidget(index.row(), 2).currentIndex()
        konditerskay_bakery_store = self.ui.tableWidget.cellWidget(index.row(), 3).currentIndex()
        konditerskay_ice_sklad = self.ui.tableWidget.cellWidget(index.row(), 4).currentIndex()
        konditerskay_vhod_group = self.ui.tableWidget.cellWidget(index.row(), 5).currentIndex()
        konditerskay_tualet = self.ui.tableWidget.cellWidget(index.row(), 6).currentIndex()
        konditerskay_tables = self.ui.tableWidget.cellWidget(index.row(), 7).currentIndex()
        konditerskay_enable = self.ui.tableWidget.cellWidget(index.row(), 8).currentIndex()
        result = self.database.update_konditerskay_data(konditerskay_name, konditerskay_type, konditerskay_bakery, konditerskay_ice_sklad, konditerskay_vhod_group, konditerskay_tualet, konditerskay_tables, konditerskay_enable, konditerskay_bakery_store)
        if "успешно изменены" in result:
            self.signals.success_signal.emit(result)
        else:
            if 'Ошибка работы' in result:
                self.signals.error_DB_signal.emit(result)
            else:
                self.signals.failed_signal.emit(result)
            return

    def show_success_message(self, message):
        if "успешно" in message:
            # Отображаем сообщение об успешной операции
            QtWidgets.QMessageBox.information(self, "Успешно", message)
            self.create_table()
        else:
            pass


    def show_error_message(self, message):
        # Отображаем сообщение об ошибке в БД
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