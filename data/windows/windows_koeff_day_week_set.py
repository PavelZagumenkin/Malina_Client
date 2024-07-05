import sys

from PyQt6 import QtWidgets, QtGui
import textwrap
import pandas as pd
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox
from data.requests.db_requests import Database
from data.signals import Signals
from data.active_session import Session
from data.ui.autozakaz_table import Ui_autozakaz_table
import data.windows.windows_bakery

class WindowKoeffDayWeekSet(QtWidgets.QMainWindow):
    def __init__(self, wb_OLAP_dayWeek, periodDay, points):
        super().__init__()
        self.ui = Ui_autozakaz_table()
        self.ui.setupUi(self)
        self.database = Database()
        self.signals = Signals()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        self.periodDay = periodDay
        self.column_title = ['Кф. дня недели', 'День недели']
        self.column_title = self.column_title + points
        self.column_title_for_excel = ['День недели'] + points
        wb_OLAP_dayWeek = wb_OLAP_dayWeek[self.column_title_for_excel]
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.tableWidget.setRowCount(wb_OLAP_dayWeek.shape[0] + 1)
        self.ui.tableWidget.setColumnCount(len(self.column_title))
        self.wrap = []
        for header in self.column_title:
            wrap = textwrap.fill(header, width=10)
            self.wrap.append(wrap)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.wrap)
        self.font = QtGui.QFont("Times", 10, QFont.Weight.Bold)
        self.ui.tableWidget.horizontalHeader().setFont(self.font)
        for col in range(0, wb_OLAP_dayWeek.shape[1]):
            for row in range(0, wb_OLAP_dayWeek.shape[0]):
                if pd.isna(wb_OLAP_dayWeek.iloc[row, col]):
                    item = QTableWidgetItem('0')
                else:
                    item = QTableWidgetItem(str(wb_OLAP_dayWeek.iloc[row, col]))
                self.ui.tableWidget.setItem(row + 1, col + 1, item)
        global saveZnach
        saveZnach = {}
        for col in range(2, self.ui.tableWidget.columnCount()):
            saveZnach[col] = {}
            for row in range(1, self.ui.tableWidget.rowCount()):
                saveZnach[col][row] = float(self.ui.tableWidget.item(row, col).text())
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem("Кф. кондитерской"))
        self.ui.tableWidget.item(0, 1).setFont(self.font)
        for col_spin in range(2, self.ui.tableWidget.columnCount()):
            self.DspinboxCol = QtWidgets.QDoubleSpinBox()
            self.DspinboxCol.wheelEvent = lambda event: None
            self.ui.tableWidget.setCellWidget(0, col_spin, self.DspinboxCol)
            self.ui.tableWidget.cellWidget(0, col_spin).setValue(1.00)
            self.ui.tableWidget.cellWidget(0, col_spin).setMinimum(0.00)
            self.ui.tableWidget.cellWidget(0, col_spin).setSingleStep(0.01)
            self.ui.tableWidget.cellWidget(0, col_spin).valueChanged.connect(self.raschetKDayWeek)
        for row_spin in range(1, self.ui.tableWidget.rowCount()):
            self.DspinboxRow = QtWidgets.QDoubleSpinBox()
            self.DspinboxRow.wheelEvent = lambda event: None
            self.ui.tableWidget.setCellWidget(row_spin, 0, self.DspinboxRow)
            self.ui.tableWidget.cellWidget(row_spin, 0).setValue(1.00)
            self.ui.tableWidget.cellWidget(row_spin, 0).setMinimum(0.00)
            self.ui.tableWidget.cellWidget(row_spin, 0).setSingleStep(0.01)
            self.ui.tableWidget.cellWidget(row_spin, 0).valueChanged.connect(self.raschetKDayWeek)
        self.SaveAndClose = QtWidgets.QPushButton()
        self.ui.tableWidget.setCellWidget(0, 0, self.SaveAndClose)
        self.ui.tableWidget.cellWidget(0, 0).setText('Сохранить и закрыть')
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(12)
        font.bold()
        font.setWeight(50)
        self.ui.tableWidget.cellWidget(0, 0).setFont(font)
        self.ui.tableWidget.cellWidget(0, 0).setStyleSheet(open('data/css/QPushButton.qss').read())
        self.ui.tableWidget.cellWidget(0, 0).clicked.connect(self.saveAndCloseDef)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.setColumnWidth(0, 190)
        self.ui.tableWidget.cellChanged.connect(lambda row, col: self.on_cell_changed(row, col))
        #     self.addPeriod(self.periodDay)


        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)

    def on_cell_changed(self, row, col):
        if row >= 1 and col >= 2:
            # Получаем содержимое ячейки и проверяем, является ли оно числом
            try:
                value = float(self.ui.tableWidget.item(row, col).text())
            except ValueError:
                value = None

            # Если содержимое не является числом, то заменяем его на 0.0
            if value is None:
                QtWidgets.QMessageBox.information(self, "Error", 'Вы ввели не число')
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(0.0)))
        else:
            return

    # Увеличение или уменьшение доли продаж.
    def raschetKDayWeek(self):
        buttonClicked = self.sender()
        index = self.ui.tableWidget.indexAt(buttonClicked.pos())
        if index.row() == 0:
            for i in range(1, self.ui.tableWidget.rowCount()):
                result = round(float(saveZnach[index.column()][i]) * float(
                    self.ui.tableWidget.cellWidget(0, index.column()).value()) * float(
                    self.ui.tableWidget.cellWidget(i, 0).value()), 4)
                self.ui.tableWidget.setItem(i, index.column(), QTableWidgetItem(str(result)))
        else:
            for i in range(2, self.ui.tableWidget.columnCount()):
                result = round(float(saveZnach[i][index.row()]) * float(
                    self.ui.tableWidget.cellWidget(index.row(), 0).value()) * float(
                    self.ui.tableWidget.cellWidget(0, i).value()), 4)
                self.ui.tableWidget.setItem(index.row(), i, QTableWidgetItem(str(result)))


    # Сохранение в БД и закрытие таблицы
    def saveAndCloseDef(self):
        start_date = self.periodDay[0].toString('yyyy-MM-dd')
        end_date = self.periodDay[1].toString('yyyy-MM-dd')
        matrix_table_koeff_day_week = []
        # Проход по каждому столбцу начиная с начала названия ТТ
        for column_index in range(2, self.ui.tableWidget.columnCount()):
            if self.ui.tableWidget.horizontalHeaderItem(column_index).text() == 'Крытый\nрынок':
                column_name = 'Крытый рынок'
            elif self.ui.tableWidget.horizontalHeaderItem(column_index).text() == 'Усть-Курдю\nмская':
                column_name = 'Усть-Курдюмская'
            elif self.ui.tableWidget.horizontalHeaderItem(column_index).text() == 'Фридриха\n11':
                column_name = 'Фридриха 11'
            else:
                column_name = self.ui.tableWidget.horizontalHeaderItem(column_index).text().replace('\n', '')
            # Проход по каждой строке для текущего столбца
            for row_index in range(1, self.ui.tableWidget.rowCount()):
                row_data = [start_date, end_date, column_name, 'Выпечка пекарни']
                day_week = self.ui.tableWidget.item(row_index, 1)
                if day_week is not None:
                    row_data.append(day_week.text())
                else:
                    return
                koeff_day_week = float(self.ui.tableWidget.cellWidget(row_index, 0).value())
                if koeff_day_week is not None:
                    row_data.append(koeff_day_week)
                else:
                    return
                koeff_points = float(self.ui.tableWidget.cellWidget(0, column_index).value())
                if koeff_points is not None:
                    row_data.append(koeff_points)
                else:
                    return
                data_null = float(saveZnach[column_index][row_index])
                if data_null is not None:
                    row_data.append(data_null)
                else:
                    row_data.append(0)  # или любое значение по умолчанию для пустых ячеек
                data_koeff_day_week = float(self.ui.tableWidget.item(row_index, column_index).text())
                if data_koeff_day_week is not None:
                    row_data.append(data_koeff_day_week)
                else:
                    row_data.append(0)  # или любое значение по умолчанию для пустых ячеек
                author = self.session.get_username()  # Получение имени пользователя из экземпляра класса Session
                row_data.append(author)
                # Добавление строки в матрицу
                matrix_table_koeff_day_week.append(row_data)
        save_result = self.database.save_koeff_day_week(matrix_table_koeff_day_week)
        print(save_result)
        self.close()
    #
    # def addPeriod(self, period):
    #     self.check_db.thr_addPeriodKDayWeek(period)
    #
    # def delPeriodInDB(self, period):
    #     self.check_db.thr_delPeriodKDayWeek(period)
    #
    # def insertInDB(self, savePeriod, saveHeaders, saveDB, saveNull):
    #     self.check_db.thr_updateDayWeek(savePeriod, saveHeaders, saveDB, saveNull)
    #
    # def proverkaPerioda(self, period):
    #     self.check_db.thr_proverkaPeriodaKDayWeek(period)
    #     return otvetPeriod
    #
    # def signal_period(self, value):
    #     global otvetPeriod
    #     if value == 'Пусто':
    #         otvetPeriod = 0
    #     elif value == 'За этот период есть сформированные коэффициенты долей продаж':
    #         otvetPeriod = 1

    def show_success_message(self, message):
        pass

    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def closeEvent(self, event):
        self.session.set_work_date(
            self.periodDay[0].toString('yyyy-MM-dd'))  # Сохраняем время периода, скоторым работаем
        global WindowBakery
        if event.spontaneous():
            reply = QMessageBox()
            reply.setWindowTitle("Завершение работы с таблицой")
            reply.setWindowIcon(QtGui.QIcon("data/images/icon.png"))
            reply.setText("Вы хотите завершить работу с таблицей?")
            reply.setIcon(QMessageBox.Icon.Question)
            reply.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply.setDefaultButton(QMessageBox.StandardButton.Cancel)
            otvet = reply.exec()
            if otvet == QMessageBox.StandardButton.Yes:
                event.accept()
                WindowBakery = data.windows.windows_bakery.WindowBakery()
                WindowBakery.show()
            else:
                event.ignore()
        else:
            event.accept()
            WindowBakery = data.windows.windows_bakery.WindowBakery()
            WindowBakery.show()