from datetime import datetime
import os
import pandas as pd
import shutil
from math import ceil

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from data.ui.bakery import Ui_WindowBakery
from data.requests.db_requests import Database
from data.requests.queries import Queries
from data.signals import Signals
from data.active_session import Session

import data.windows.windows_autoorders
import data.windows.windows_prognoz_set
import data.windows.windows_prognoz_view
import data.windows.windows_prognoz_edit
import data.windows.windows_koeff_day_week_set
import data.windows.windows_koeff_day_week_view

# import Windows.WindowsBakeryTablesDayWeekEdit
# import Windows.WindowsBakeryTablesDayWeekView
# import Windows.WindowsBakeryTablesDayWeekRedact
# import Windows.WindowsBakeryNormativEdit
# import Windows.WindowsBakeryNormativRedact


class WindowBakery(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowBakery()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

        # Работа с установкой периода
        if self.session.get_work_date() == None:
            year, month, day = map(int, self.session.get_current_date().split('.'))
        else:
            year, month, day = map(int, self.session.get_work_date().split('-'))
        TodayDate = QtCore.QDate(year, month, day)
        EndDay = TodayDate.addDays(6)
        self.ui.dateEdit_startDay.setDate(TodayDate)
        self.ui.dateEdit_endDay.setDate(EndDay)
        self.periodDay = [self.ui.dateEdit_startDay.date(), self.ui.dateEdit_endDay.date()]
        self.category = 'Выпечка пекарни'

        # Скрываем прогрессбар
        self.ui.progressBar.hide()

        # Подключаем действия к функциям
        self.ui.dateEdit_startDay.userDateChanged['QDate'].connect(self.set_end_day)
        self.ui.btn_exit_bakery.clicked.connect(self.show_window_autoorders)
        self.ui.btn_path_OLAP_prodagi.clicked.connect(self.olap_prodagi_xlsx)
        self.ui.btn_path_dayWeek.clicked.connect(self.olap_dayWeek_xlsx)
        self.ui.btn_set_prognoz.clicked.connect(self.koeff_prognoz_set)
        self.ui.btn_set_dayWeek.clicked.connect(self.koeff_day_week_set)
        self.ui.btn_prosmotr_prognoz.clicked.connect(self.prognoz_tables_view)
        self.ui.btn_edit_prognoz.clicked.connect(self.prognoz_tables_edit)
        self.ui.btn_delete_prognoz.clicked.connect(self.dialog_delete_prognoz)
        self.ui.btn_prosmotr_dayWeek.clicked.connect(self.koeff_day_week_view)
        # self.ui.btn_edit_koeff_DayWeek.clicked.connect(self.dayWeekTablesRedact)
        # self.ui.btn_delete_koeff_DayWeek.clicked.connect(self.dialogDeleteKDayWeek)
        # self.ui.btn_Normativ.clicked.connect(self.normativ)
        # self.ui.btn_editNormativ.clicked.connect(self.normativTablesRedact)
        # self.ui.btn_deleteNormativ.clicked.connect(self.dialogDeleteNormativ)
        # self.ui.btn_download_Normativ.clicked.connect(self.saveFileDialogNormativ)
        # self.ui.btn_download_Layout.clicked.connect(self.saveFileDialogLayout)

        # Проверям наличие готовых автозаказов в БД
        self.check_prognoz()
        self.check_koeff_day_week()
        self.check_normativ()

        self.ui.formLayoutWidget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        checkbox_list = []
        data_konditerskie = self.database.get_konditerskie()
        for point in range(0, len(data_konditerskie)):
            if data_konditerskie[point][2] == 1 & data_konditerskie[point][9] == 1 & data_konditerskie[point][8] == 1:
                checkbox_list.append(data_konditerskie[point][1])
        checkbox_list.sort()
        sorted_checkbox_list = []
        for check in checkbox_list:
            sorted_checkbox_list.append(QtWidgets.QCheckBox(check))
        for checkbox in range(0, len(sorted_checkbox_list), 2):
            checkbox1 = sorted_checkbox_list[checkbox]
            checkbox1.setStyleSheet("font-size: 16px;")
            checkbox1.setChecked(False)
            try:
                checkbox2 = sorted_checkbox_list[checkbox + 1]
                checkbox2.setStyleSheet("font-size: 16px;")
                checkbox2.setChecked(False)
                self.ui.formLayoutWidget.layout().addRow(checkbox1, checkbox2)
            except:
                self.ui.formLayoutWidget.layout().addRow(checkbox1)
        self.install_check_box()

        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)


    # Получаем список кондитерских и устанавливаем чек-боксы
    def install_check_box(self):
        for index in range(0, self.ui.formLayoutWidget.layout().count()):
            self.ui.formLayoutWidget.layout().itemAt(index).widget().setChecked(False)
        if self.check_prognoz() == 1:
            checkbox_list_checked = self.get_spisok_konditerskih_in_DB(Queries.get_spisok_konditerskih_in_prognoz_in_DB)
            sorted_checkbox_list = []
            for index in range(0, self.ui.formLayoutWidget.layout().count()):
                sorted_checkbox_list.append(self.ui.formLayoutWidget.layout().itemAt(index).widget().text())
            for checkbox in checkbox_list_checked:
                if checkbox in sorted_checkbox_list:
                    self.ui.formLayoutWidget.layout().itemAt(sorted_checkbox_list.index(checkbox)).widget().setChecked(True)
        elif self.check_koeff_day_week() == 1:
            checkbox_list_checked = self.get_spisok_konditerskih_in_DB(Queries.get_spisok_konditerskih_in_koeff_day_week_in_DB)
            sorted_checkbox_list = []
            for index in range(0, self.ui.formLayoutWidget.layout().count()):
                sorted_checkbox_list.append(self.ui.formLayoutWidget.layout().itemAt(index).widget().text())
            for checkbox in checkbox_list_checked:
                if checkbox in sorted_checkbox_list:
                    self.ui.formLayoutWidget.layout().itemAt(sorted_checkbox_list.index(checkbox)).widget().setChecked(True)
        else:
            for index in range(0, self.ui.formLayoutWidget.layout().count()):
                self.ui.formLayoutWidget.layout().itemAt(index).widget().setChecked(True)


    # Функция обработки изменения стартовой даты периода
    def set_end_day(self):
        self.ui.dateEdit_endDay.setDate(self.ui.dateEdit_startDay.date().addDays(6))
        self.periodDay = [self.ui.dateEdit_startDay.date(), self.ui.dateEdit_endDay.date()]
        self.check_prognoz()
        self.check_koeff_day_week()
        self.check_normativ()
        self.install_check_box()


    # Функция нажатия кнопки ..., диалог выбора файла OLAP по продажам Выпечки
    def olap_prodagi_xlsx(self):
        fileName = QFileDialog.getOpenFileName(self, 'Выберите файл OLAP по продажам Выпечки', os.path.expanduser(
                '~') + r'\Desktop', 'Excel файл (*.xlsx)')
        self.ui.lineEdit_OLAP_prodagi.setText(fileName[0])
        self.ui.lineEdit_OLAP_prodagi.setStyleSheet("padding-left: 5px; color: rgb(0, 0, 0)")


    # Проверяем на пустоту поле для OLAP отчета по продажам выпечки
    @staticmethod
    def check_prognoz_OLAP(funct_bakery):
        def wrapper(self):
            if len(self.ui.lineEdit_OLAP_prodagi.text()) == 0 or self.ui.lineEdit_OLAP_prodagi.text() == 'Файл отчета неверный, укажите OLAP по продажам за 7 дней':
                self.ui.lineEdit_OLAP_prodagi.setStyleSheet("padding-left: 5px; color: rgba(228, 107, 134, 1)")
                self.ui.lineEdit_OLAP_prodagi.setText('Не выбран файл отчета!')
                return
            elif self.ui.lineEdit_OLAP_prodagi.text() == 'Не выбран файл отчета!':
                return
            funct_bakery(self)
        return wrapper


    # Функция нажатия кнопки "Установить" для OLAP отчета по продажам выпечки
    @check_prognoz_OLAP
    def koeff_prognoz_set(self):
        path_OLAP_prodagi = self.ui.lineEdit_OLAP_prodagi.text()
        self.prognoz_table_open(path_OLAP_prodagi)


    # Проверка на правильность OLAP отчета по продажам выпечки и запуск таблицы с коэффициентами
    def prognoz_table_open(self, path_OLAP_prodagi):
        wb_OLAP_prodagi = pd.ExcelFile(path_OLAP_prodagi)
        sheet_OLAP_prodagi = wb_OLAP_prodagi.sheet_names
        if sheet_OLAP_prodagi[0] != "OLAP отчет для Выпечки":
            self.ui.lineEdit_OLAP_prodagi.setStyleSheet("padding-left: 5px; color: rgba(228, 107, 134, 1)")
            self.ui.lineEdit_OLAP_prodagi.setText('Файл отчета неверный, укажите OLAP по продажам Выпечки за 7 дней')
        else:
            wb_OLAP_prodagi = pd.read_excel(path_OLAP_prodagi)
            index_of_period = wb_OLAP_prodagi.iloc[:, 0].str.find("Период").idxmax()
            start_date_text = wb_OLAP_prodagi.iloc[index_of_period, 0][10:20]
            end_date_text = wb_OLAP_prodagi.iloc[index_of_period, 0][24:34]
            start_date = datetime.strptime(start_date_text, '%d.%m.%Y')
            end_date = datetime.strptime(end_date_text, '%d.%m.%Y')
            if (end_date - start_date).days + 1 != 7:
                self.ui.lineEdit_OLAP_prodagi.setStyleSheet("padding-left: 5px; color: rgba(228, 107, 134, 1)")
                self.ui.lineEdit_OLAP_prodagi.setText(
                    f'Файл OLAP отчета по продажам должен быть за 7 дней, а вы загрузили за {(end_date - start_date).days + 1} дней!')
                return
            index_of_start_table = wb_OLAP_prodagi.iloc[:, 0].str.find("Код блюда").idxmax() + 1
            wb_OLAP_prodagi = pd.read_excel(path_OLAP_prodagi, header=index_of_start_table)
            wb_OLAP_prodagi = wb_OLAP_prodagi.dropna(axis=1, how='all')
            # Удаление последнего столбца и последней строки
            wb_OLAP_prodagi = wb_OLAP_prodagi.iloc[:-1, :-1]
            point_in_OLAP = wb_OLAP_prodagi.columns.tolist()
            del point_in_OLAP[0:2]
            points_check = self.ui.formLayoutWidget.findChildren(QtWidgets.QCheckBox)
            result_koeff_day_week = self.check_data_in_DB(Queries.get_count_row_koeff_day_week_in_DB)
            if result_koeff_day_week == 0:
                points = []
                for i in range(len(points_check)):
                    if points_check[i].isChecked():
                        if not points_check[i].text() in point_in_OLAP:
                            self.signals.failed_signal.emit(
                                f"В OLAP-отчете отсутствует кондитерская {points_check[i].text()}")
                            return
                        else:
                            points.append(points_check[i].text())
            else:
                points_in_DB = self.get_spisok_konditerskih_in_DB(Queries.get_spisok_konditerskih_in_koeff_day_week_in_DB)
                for i in range(len(points_in_DB)):
                    if not points_in_DB[i] in point_in_OLAP:
                        self.signals.failed_signal.emit(f"В OLAP-отчете отсутствует кондитерская {points_in_DB[i]}")
                        return
                points = points_in_DB
            self.hide()
            global window_prognoz_set
            window_prognoz_set = data.windows.windows_prognoz_set.WindowPrognozTablesSet(wb_OLAP_prodagi, self.periodDay, points)
            window_prognoz_set.showMaximized()


    # Диалог выбора файла OLAP отчета по продажам по дням недели для выпечки
    def olap_dayWeek_xlsx(self):
        fileName = QFileDialog.getOpenFileName(self, 'Выберите файл OLAP по дням недели для Выпечки', os.path.expanduser(
                '~') + r'\Desktop', 'Excel файл (*.xlsx)')
        self.ui.lineEdit_OLAP_dayWeek.setText(fileName[0])
        self.ui.lineEdit_OLAP_dayWeek.setStyleSheet("padding-left: 5px; color: rgb(0, 0, 0)")


    # Проверяем на пустоту поля для OLAP отчета по продажам по дням недели для выпечки
    @staticmethod
    def check_day_week(funct_bakery):
        def wrapper(self):
            if len(self.ui.lineEdit_OLAP_dayWeek.text()) == 0 or self.ui.lineEdit_OLAP_dayWeek.text() == 'Файл отчета неверный, укажите OLAP по продажам по дням недели для Выпечки за 7 дней':
                self.ui.lineEdit_OLAP_dayWeek.setStyleSheet("padding-left: 5px; color: rgba(228, 107, 134, 1)")
                self.ui.lineEdit_OLAP_dayWeek.setText('Не выбран файл отчета!')
                return
            elif self.ui.lineEdit_OLAP_dayWeek.text() == 'Не выбран файл отчета!':
                return
            funct_bakery(self)
        return wrapper


    # Обрабытываем кнопку "Установить" для OLAP отчета по продажам по дням недели для выпечки
    @check_day_week
    def koeff_day_week_set(self):
        path_OLAP_DayWeek = self.ui.lineEdit_OLAP_dayWeek.text()
        self.day_week_table(path_OLAP_DayWeek)


    # Проверка на правильность OLAP отчета по продажам по дням недели для выпечки и запуск таблици с коэффициентами
    def day_week_table(self, path_OLAP_DayWeek):
        wb_OLAP_dayWeek = pd.ExcelFile(path_OLAP_DayWeek)
        sheet_OLAP_dayWeek = wb_OLAP_dayWeek.sheet_names
        if sheet_OLAP_dayWeek[0] != "OLAP по дням недели для Выпечки":
            self.ui.lineEdit_OLAP_dayWeek.setStyleSheet("padding-left: 5px; color: rgba(228, 107, 134, 1)")
            self.ui.lineEdit_OLAP_dayWeek.setText(
                'Файл отчета неверный, укажите OLAP по продажам по дням недели для Выпечки')
        else:
            self.day_week_table_open(path_OLAP_DayWeek)


    def day_week_table_open(self, pathOLAP_DayWeek):
        wb_OLAP_dayWeek = pd.ExcelFile(pathOLAP_DayWeek)
        sheet_OLAP_dayWeek = wb_OLAP_dayWeek.sheet_names
        if sheet_OLAP_dayWeek[0] != "OLAP по дням недели для Выпечки":
            self.ui.lineEdit_OLAP_dayWeek.setStyleSheet("padding-left: 5px; color: rgba(228, 107, 134, 1)")
            self.ui.lineEdit_OLAP_dayWeek.setText("Файл отчета неверный, укажите OLAP по продажам по дням недели для Выпечки")
        wb_OLAP_dayWeek = pd.read_excel(pathOLAP_DayWeek)
        index_of_period = wb_OLAP_dayWeek.iloc[:, 0].str.find("Период").idxmax()
        start_date_text = wb_OLAP_dayWeek.iloc[index_of_period, 0][10:20]
        end_date_text = wb_OLAP_dayWeek.iloc[index_of_period, 0][24:34]
        start_date = datetime.strptime(start_date_text, '%d.%m.%Y')
        end_date = datetime.strptime(end_date_text, '%d.%m.%Y')
        if ((end_date - start_date).days + 1) % 7 != 0:
            self.ui.lineEdit_OLAP_prodagi.setStyleSheet("padding-left: 5px; color: rgba(228, 107, 134, 1)")
            self.ui.lineEdit_OLAP_prodagi.setText(
                    f'Файл OLAP отчета должен быть кратен 7 дней, а вы загрузили за {(end_date - start_date).days + 1} дней!')
            return
        index_of_start_table = wb_OLAP_dayWeek.iloc[:, 0].str.find("День недели").idxmax() + 1
        wb_OLAP_dayWeek = pd.read_excel(pathOLAP_DayWeek, header=index_of_start_table)
        wb_OLAP_dayWeek = wb_OLAP_dayWeek.dropna(axis=1, how='all')
        # Удаление последнего столбца и последней строки
        wb_OLAP_dayWeek = wb_OLAP_dayWeek.iloc[:-1, :-1]
        point_in_OLAP = wb_OLAP_dayWeek.columns.tolist()
        del point_in_OLAP[0:1]
        points_check = self.ui.formLayoutWidget.findChildren(QtWidgets.QCheckBox)
        result_prognoz = self.check_data_in_DB(Queries.get_count_row_prognoz_in_DB())
        if result_prognoz == 0:
            points = []
            for i in range(len(points_check)):
                if points_check[i].isChecked():
                    if not points_check[i].text() in point_in_OLAP:
                        self.signals.failed_signal.emit(f"В OLAP-отчете отсутствует кондитерская {points_check[i].text()}")
                        return
                    else:
                        points.append(points_check[i].text())
        else:
            points_in_DB = self.get_spisok_konditerskih_in_DB(Queries.get_spisok_konditerskih_in_prognoz_in_DB)
            for i in range(len(points_in_DB)):
                if not points_in_DB[i] in point_in_OLAP:
                    self.signals.failed_signal.emit(f"В OLAP-отчете отсутствует кондитерская {points_in_DB[i]}")
                    return
            points = points_in_DB
        self.hide()
        global windows_koeff_day_week_set
        windows_koeff_day_week_set = data.windows.windows_koeff_day_week_set.WindowKoeffDayWeekSet(wb_OLAP_dayWeek, self.periodDay, points)
        windows_koeff_day_week_set.showMaximized()


    def check_prognoz(self):
        result_prognoz = self.check_data_in_DB(Queries.get_count_row_prognoz_in_DB)
        if result_prognoz == 0:
            self.ui.btn_set_prognoz.setEnabled(True)
            self.ui.btn_prosmotr_prognoz.setEnabled(False)
            self.ui.btn_edit_prognoz.setEnabled(False)
            self.ui.btn_delete_prognoz.setEnabled(False)
            self.ui.btn_set_normativ.setEnabled(False)
            self.ui.btn_download_layout.setEnabled(False)
            return 0
        else:
            self.ui.btn_set_prognoz.setEnabled(False)
            self.ui.btn_prosmotr_prognoz.setEnabled(True)
            self.ui.btn_edit_prognoz.setEnabled(True)
            self.ui.btn_delete_prognoz.setEnabled(True)
            return 1


    def check_koeff_day_week(self):
        result_koeff_day_week = self.check_data_in_DB(Queries.get_count_row_koeff_day_week_in_DB)
        if result_koeff_day_week == 0:
            self.ui.btn_set_dayWeek.setEnabled(True)
            self.ui.btn_prosmotr_dayWeek.setEnabled(False)
            self.ui.btn_edit_dayWeek.setEnabled(False)
            self.ui.btn_delete_dayWeek.setEnabled(False)
            self.ui.btn_download_layout.setEnabled(False)
            self.ui.btn_set_normativ.setEnabled(False)
            return 0
        else:
            self.ui.btn_set_dayWeek.setEnabled(False)
            self.ui.btn_prosmotr_dayWeek.setEnabled(True)
            self.ui.btn_edit_dayWeek.setEnabled(True)
            self.ui.btn_delete_dayWeek.setEnabled(True)
            return 1


    def check_normativ(self):
        result_normativ = self.check_data_in_DB(Queries.get_count_row_normativ_in_DB)
        if result_normativ == 0:
            self.ui.btn_edit_normativ.setEnabled(False)
            self.ui.btn_download_normativ.setEnabled(False)
            self.ui.btn_delete_normativ.setEnabled(False)
            return 0
        else:
            self.ui.btn_set_normativ.setEnabled(False)
            self.ui.btn_edit_normativ.setEnabled(True)
            self.ui.btn_download_normativ.setEnabled(True)
            self.ui.btn_delete_normativ.setEnabled(True)
            return 1


    def check_data_in_DB(self, check_function_in_DB):
        start_date = self.periodDay[0].toString('yyyy-MM-dd')
        end_date = self.periodDay[1].toString('yyyy-MM-dd')
        result_check = self.database.check_counts_row_in_DB(start_date, end_date, "Выпечка пекарни", check_function_in_DB)
        if isinstance(result_check, int):
            return result_check
        else:
            return 0


    def get_spisok_konditerskih_in_DB(self, check_function_in_DB):
        start_date = self.periodDay[0].toString('yyyy-MM-dd')
        end_date = self.periodDay[1].toString('yyyy-MM-dd')
        result_spisok = self.database.get_spisok_konditerskih_in_DB(start_date, end_date, "Выпечка пекарни", check_function_in_DB)
        return result_spisok


    # Закрываем окно настроек, открываем выбор раздела
    def show_window_autoorders(self):
        self.close()
        global windowAutoorders
        windowAutoorders = data.windows.windows_autoorders.WindowAutoorders()
        windowAutoorders.show()


    def show_success_message(self, message):
        # if "Авторизация успешна" in message:
        #     self.show_windowSection()
        pass


    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def prognoz_tables_view(self):
        self.hide()
        periodDay = self.periodDay
        category = 'Выпечка пекарни'
        global WindowBakeryTablesView
        WindowBakeryTablesView = data.windows.windows_prognoz_view.WindowPrognozTablesView(periodDay, category)
        WindowBakeryTablesView.showMaximized()

    def prognoz_tables_edit(self):
        # self.normativTablesDelete()
        self.hide()
        periodDay = self.periodDay
        category = 'Выпечка пекарни'
        global WindowBakeryTablesEdit
        WindowBakeryTablesEdit = data.windows.windows_prognoz_edit.WindowPrognozTablesEdit(periodDay, category)
        WindowBakeryTablesEdit.showMaximized()
    #
    # def normativTablesRedact(self):
    #     self.hide()
    #     periodDay = self.periodDay
    #     global WindowNormativTablesRedact
    #     WindowNormativTablesRedact = Windows.WindowsBakeryNormativRedact.WindowBakeryNormativRedact(periodDay)
    #     WindowNormativTablesRedact.showMaximized()
    #
    def dialog_delete_prognoz(self):
        dialogBox = QMessageBox()
        dialogBox.setText("Вы действительно хотите удалить сформированный прогноз и норматив(если сформирован) с изначальными данными?")
        dialogBox.setWindowIcon(QtGui.QIcon("data/images/icon.png"))
        dialogBox.setWindowTitle('Удаление прогноза продаж')
        dialogBox.setIcon(QMessageBox.Icon.Critical)
        dialogBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        dialogBox.buttonClicked.connect(self.dialog_delete_prognoz_button_clicked)
        dialogBox.exec()

    def dialog_delete_prognoz_button_clicked(self, button_clicked):
        if button_clicked.text() == "OK":
            self.prognoz_tables_delete()
            # self.normativTablesDelete()
    #
    # def dialogDeleteKDayWeek(self):
    #     dialogBox = QMessageBox()
    #     dialogBox.setText("Вы действительно хотите удалить сформированные коэффициенты по дням недели и норматив(если сформирован) с изначальными данными?")
    #     dialogBox.setWindowIcon(QtGui.QIcon("image/icon.png"))
    #     dialogBox.setWindowTitle('Удаление прогноза продаж')
    #     dialogBox.setIcon(QMessageBox.Icon.Critical)
    #     dialogBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    #     dialogBox.buttonClicked.connect(self.dialogButtonClickedKDayWeek)
    #     dialogBox.exec()
    #
    # def dialogButtonClickedKDayWeek(self, button_clicked):
    #     if button_clicked.text() == "OK":
    #         self.dayWeekTablesDelete()
    #         self.normativTablesDelete()
    #
    # def dialogDeleteNormativ(self):
    #     dialogBox = QMessageBox()
    #     dialogBox.setText("Вы действительно хотите удалить сформированный норматив с изначальными данными?")
    #     dialogBox.setWindowIcon(QtGui.QIcon("image/icon.png"))
    #     dialogBox.setWindowTitle('Удаление норматива')
    #     dialogBox.setIcon(QMessageBox.Icon.Critical)
    #     dialogBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    #     dialogBox.buttonClicked.connect(self.dialogButtonClickedNormativ)
    #     dialogBox.exec()
    #
    # def dialogButtonClickedNormativ(self, button_clicked):
    #     if button_clicked.text() == "OK":
    #         self.normativTablesDelete()
    #
    # def normativTablesDelete(self):
    #     period = self.periodDay
    #     if self.proverkaNormativa(self.periodDay) == 1:
    #         self.check_db.thr_deleteNormativ(period)
    #         self.proverkaNormativaFunc()
    #         self.proverkaPeriodaPrognozFunc()
    #
    def prognoz_tables_delete(self):
        start_date = self.periodDay[0].toString('yyyy-MM-dd')
        end_date = self.periodDay[1].toString('yyyy-MM-dd')
        result_delete = self.database.delete_prognoz(start_date, end_date, self.category)
        print(result_delete)
        self.check_prognoz()
        self.check_normativ()
    #
    #
    def koeff_day_week_view(self):
        self.hide()
        periodDay = self.periodDay
        category = 'Выпечка пекарни'
        global WindowBakeryTablesDayWeekView
        WindowBakeryTablesDayWeekView = data.windows.windows_koeff_day_week_view.WindowKoeffDayWeekView(periodDay, category)
        WindowBakeryTablesDayWeekView.showMaximized()
    #
    # def dayWeekTablesRedact(self):
    #     self.normativTablesDelete()
    #     self.hide()
    #     periodDay = self.periodDay
    #     global WindowBakeryTablesDayWeekRedact
    #     WindowBakeryTablesDayWeekRedact = Windows.WindowsBakeryTablesDayWeekRedact.WindowBakeryTablesDayWeekRedact(
    #         periodDay)
    #     WindowBakeryTablesDayWeekRedact.showMaximized()
    #
    # def dayWeekTablesDelete(self):
    #     period = self.periodDay
    #     self.check_db.thr_deleteKDayWeek(period)
    #     self.proverkaPeriodaKDayWeekFunc()
    #
    # def saveFileDialogNormativ(self):
    #     fileName, _ = QFileDialog.getSaveFileName(
    #         parent=self,
    #         caption="Сохранение данных",
    #         directory=os.path.expanduser(
    #             '~') + r'\Desktop' + f"\Нормативы для пекарни с {self.periodDay[0].toString('dd.MM.yyyy')} по {self.periodDay[1].toString('dd.MM.yyyy')}.xlsx",
    #         filter="Все файлы (*);")
    #     if fileName:
    #         self.ui.progressBar.show()
    #         self.setEnabled(False)
    #         progress = 0
    #         normativData = self.poiskNormativa(self.periodDay)
    #         headers = json.loads(normativData[0].strip("\'"))
    #         data = json.loads(normativData[1].strip("\'"))
    #         self.ui.progressBar.setValue(progress)
    #         self.ui.progressBar.setMinimum(0)
    #         self.ui.progressBar.setMaximum(len(data.keys()) - 3)
    #         Excel = win32com.client.Dispatch("Excel.Application")
    #         normativExcel = Excel.Workbooks.Add()
    #         sheet = normativExcel.ActiveSheet
    #         sheet.Columns(1).NumberFormat = "@"
    #         for col in range(2, len(headers)):
    #             sheet.Cells(1, col - 1).Value = headers[col]
    #         for col in range(2, len(data.keys())):
    #             for row in range(1, len(data.get(str(col)).keys())):
    #                 if col > 4:
    #                     sheet.Cells(int(row) + 1, col - 1).Value = round(data[str(col)][str(row)], 0)
    #                 else:
    #                     sheet.Cells(int(row) + 1, col - 1).Value = data[str(col)][str(row)]
    #             self.ui.progressBar.setValue(progress)
    #             progress += 1
    #         sheet.Columns.AutoFit()
    #         lastColumn = sheet.UsedRange.Columns.Count
    #         lastRow = sheet.UsedRange.Rows.Count
    #         sheet.Range("A1").AutoFilter(Field=1)
    #         for col in range(4, lastColumn + 1):
    #             sheet.Cells(lastRow + 1, col).Value = f"=SUM(R[{1 - lastRow}]C:R[-1]C)"
    #         sheet.Range(sheet.Cells(1, 1), sheet.Cells(lastRow + 1, lastColumn)).Borders(2).Weight = 2
    #         sheet.Range(sheet.Cells(1, 1), sheet.Cells(lastRow + 1, lastColumn)).Borders(4).Weight = 2
    #         sheet.Range(sheet.Cells(1, 1), sheet.Cells(lastRow + 1, lastColumn)).Borders(7).Weight = 3
    #         sheet.Range(sheet.Cells(1, 1), sheet.Cells(lastRow + 1, lastColumn)).Borders(8).Weight = 3
    #         sheet.Range(sheet.Cells(1, 1), sheet.Cells(lastRow + 1, lastColumn)).Borders(9).Weight = 3
    #         sheet.Range(sheet.Cells(1, 1), sheet.Cells(lastRow + 1, lastColumn)).Borders(10).Weight = 3
    #         fileName = fileName.replace('/', '\\')
    #         Excel.DisplayAlerts = False
    #         normativExcel.SaveAs(Filename=fileName)
    #         normativExcel.Close()
    #         Excel.Quit()
    #         self.setEnabled(True)
    #         self.ui.progressBar.hide()
    #         path_to_folder, file_name = os.path.split(fileName)
    #         os.startfile(path_to_folder)  # открытие папки
    #
    # def saveFileDialogLayout(self):
    #     folderName = QFileDialog.getExistingDirectory(
    #         parent=self,
    #         caption="Выберите папку для сохранения выкладки",
    #         directory=os.path.expanduser('~') + r'\Desktop')
    #     if folderName:
    #         self.ui.progressBar.show()
    #         self.setEnabled(False)
    #         progress = 0
    #         folderName = folderName.replace('/',
    #                                         '\\') + f"\Выкладка {self.periodDay[0].toString('dd.MM.yyyy')} по {self.periodDay[1].toString('dd.MM.yyyy')}"
    #         if os.path.exists(folderName) == True:
    #             shutil.rmtree(folderName)
    #         os.mkdir(folderName)
    #         prognoz = self.poiskPrognozaExcel(self.periodDay)
    #         headersPrognoz = json.loads(prognoz[0].strip("\'"))
    #         dataPrognoz = json.loads(prognoz[1].strip("\'"))
    #         kdayweek = self.poiskKDayWeekExcel(self.periodDay)
    #         headersKdayweek = json.loads(kdayweek[0].strip("\'"))
    #         dataKdayweek = json.loads(kdayweek[1].strip("\'"))
    #         del headersPrognoz[:5]
    #         keysDataPrognoz = ['0', '1', '2', '6']
    #         self.ui.progressBar.setValue(progress)
    #         self.ui.progressBar.setMinimum(0)
    #         self.ui.progressBar.setMaximum(len(headersPrognoz) - 1)
    #         for key in keysDataPrognoz:
    #             dataPrognoz.pop(key, None)
    #         keysDataKdayweek = ['0']
    #         for key in keysDataKdayweek:
    #             dataKdayweek.pop(key, None)
    #         Excel = win32com.client.Dispatch("Excel.Application")
    #         pointCounter = 7
    #         for point in headersPrognoz:
    #             pointExcel = Excel.Workbooks.Add()
    #             sheet = pointExcel.ActiveSheet
    #             sheet.Columns(1).NumberFormat = "@"
    #             sheet.Columns(6).NumberFormat = "@"
    #             sheet.Columns(11).NumberFormat = "@"
    #             sheet.Columns(16).NumberFormat = "@"
    #             sheet.Columns(21).NumberFormat = "@"
    #             sheet.Columns(26).NumberFormat = "@"
    #             sheet.Columns(31).NumberFormat = "@"
    #             dayCol = 1
    #             for day in range(0, 7):
    #                 DayInPeriod = self.periodDay[0].addDays(day)
    #                 date = (datetime.date(int(DayInPeriod.toString('yyyy')), int(DayInPeriod.toString('MM')),
    #                                       int(DayInPeriod.toString('dd')))).isoweekday()
    #                 sheet.Cells(1, dayCol).Value = point
    #                 sheet.Cells(1, dayCol + 2).Value = DayInPeriod.toString('dd.MM.yyyy')
    #                 sheet.Cells(2, dayCol).Value = "Код"
    #                 sheet.Columns(dayCol).ColumnWidth = 6
    #                 sheet.Cells(2, dayCol + 1).Value = "Наименование"
    #                 sheet.Columns(dayCol + 1).ColumnWidth = 45
    #                 sheet.Cells(2, dayCol + 2).Value = "Всего"
    #                 sheet.Columns(dayCol + 2).ColumnWidth = 6
    #                 sheet.Cells(2, dayCol + 3).Value = "Утро"
    #                 sheet.Columns(dayCol + 3).ColumnWidth = 6
    #                 sheet.Cells(2, dayCol + 4).Value = "День"
    #                 sheet.Columns(dayCol + 4).ColumnWidth = 6
    #                 sheet.Range(sheet.Cells(1, dayCol), sheet.Cells(1, dayCol + 1)).Merge()
    #                 sheet.Range(sheet.Cells(1, dayCol + 2), sheet.Cells(1, dayCol + 4)).Merge()
    #                 rowCount = 3
    #                 for poz in dataPrognoz['4']:
    #                     if poz != '0':
    #                         sheet.Cells(rowCount, dayCol).Value = dataPrognoz['4'][poz]
    #                         sheet.Cells(rowCount, dayCol + 1).Value = dataPrognoz['5'][poz]
    #                         itogo = (dataPrognoz[str(pointCounter)][poz] * dataKdayweek[str(headersKdayweek.index(point))][str(date)]) / dataPrognoz['3'][poz]
    #                         if itogo < 1:
    #                             itogo = ceil(itogo)
    #                         itogo = round(itogo * dataPrognoz['3'][poz])
    #                         sheet.Cells(rowCount, dayCol + 2).Value = itogo
    #                         morningLayout = round((itogo * 0.6) / dataPrognoz['3'][poz]) * dataPrognoz['3'][poz]
    #                         sheet.Cells(rowCount, dayCol + 3).Value = morningLayout
    #                         dayLayout = itogo - morningLayout
    #                         sheet.Cells(rowCount, dayCol + 4).Value = dayLayout
    #                         rowCount += 1
    #                 lastRow = rowCount
    #                 sheet.Cells(lastRow, dayCol + 2).Value = f"=SUM(R[{3 - lastRow}]C:R[-1]C)"
    #                 sheet.Cells(lastRow, dayCol + 3).Value = f"=SUM(R[{3 - lastRow}]C:R[-1]C)"
    #                 sheet.Cells(lastRow, dayCol + 4).Value = f"=SUM(R[{3 - lastRow}]C:R[-1]C)"
    #                 sheet.Range(sheet.Cells(1, dayCol), sheet.Cells(lastRow, dayCol+4)).Borders(2).Weight = 2
    #                 sheet.Range(sheet.Cells(1, dayCol), sheet.Cells(lastRow, dayCol+4)).Borders(4).Weight = 2
    #                 sheet.Range(sheet.Cells(1, dayCol), sheet.Cells(lastRow, dayCol+4)).Borders(7).Weight = 3
    #                 sheet.Range(sheet.Cells(1, dayCol), sheet.Cells(lastRow, dayCol+4)).Borders(8).Weight = 3
    #                 sheet.Range(sheet.Cells(1, dayCol), sheet.Cells(lastRow, dayCol+4)).Borders(9).Weight = 3
    #                 sheet.Range(sheet.Cells(1, dayCol), sheet.Cells(lastRow, dayCol+4)).Borders(10).Weight = 3
    #                 if dayCol != 1:
    #                     sheet.Columns(dayCol).PageBreak = True
    #                 dayCol += 5
    #             sortRange = sheet.Range(sheet.Cells(3, 1), sheet.Cells(sheet.UsedRange.Rows.Count, dayCol+4))
    #             sortRange.Sort(Key1=sortRange.Range("B3"), Order1=1, Orientation=1)  # Сортировка по возрастанию
    #             Excel.DisplayAlerts = False
    #             pointExcel.SaveAs(Filename=(folderName + '\\' + point + '.xlsx'))
    #             pointExcel.Close()
    #             Excel.Quit()
    #             self.ui.progressBar.setValue(progress)
    #             progress += 1
    #             pointCounter += 1
    #     self.setEnabled(True)
    #     self.ui.progressBar.hide()
    #     os.startfile(folderName)  # открытие папки
