import sys

from PyQt6 import QtWidgets, QtGui, QtCore
import textwrap
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox
from data.requests.db_requests import Database
from data.signals import Signals
from data.ui.autozakaz_table import Ui_autozakaz_table
import data.windows.windows_bakery


class WindowKoeffDayWeekView(QtWidgets.QMainWindow):
    def __init__(self, periodDay, category):
        super().__init__()
        self.ui = Ui_autozakaz_table()
        self.ui.setupUi(self)
        self.database = Database()
        self.signals = Signals()
        self.category = category
        self.periodDay = periodDay
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.column_title = ['Кф. дня недели', 'День недели']
        koeff_day_week_data = self.get_koeff_day_week_data()
        unique_points = []
        unique_day_week = []
        for row in koeff_day_week_data:
            point = row[2]
            day_week = row[4]
            if point not in unique_points:
                unique_points.append(point)
            if day_week not in unique_day_week:
                unique_day_week.append(day_week)
        self.column_title = self.column_title + unique_points
        self.ui.tableWidget.setRowCount(len(unique_day_week)+1)
        self.ui.tableWidget.setColumnCount(len(self.column_title))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.column_title)
        self.font = QtGui.QFont("Times", 10, QFont.Weight.Bold)
        self.ui.tableWidget.horizontalHeader().setFont(self.font)
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem("Кф. кондитерской"))
        self.ui.tableWidget.item(0, 1).setFont(self.font)
        for row in range(0, self.ui.tableWidget.rowCount()):
            if row > 0:
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(unique_day_week[row-1])))
                day_week_in_table = self.ui.tableWidget.item(row, 1).text()
                for spisok in koeff_day_week_data:
                    if spisok[4] == day_week_in_table:
                        self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(spisok[5])))
                        self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(spisok[4])))
                        break
                for col in range(2, self.ui.tableWidget.columnCount()):
                    for spisok in koeff_day_week_data:
                        if spisok[4] == day_week_in_table and spisok[2] == self.ui.tableWidget.horizontalHeaderItem(col).text():
                            self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(spisok[8])))
                            break
            else:
                for col in range(2, self.ui.tableWidget.columnCount()):
                    for spisok in koeff_day_week_data:
                        if spisok[2] == self.ui.tableWidget.horizontalHeaderItem(col).text():
                            self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(spisok[6])))
                            break
        self.wrap = []
        for header in self.column_title:
            wrap = textwrap.fill(header, width=10)
            self.wrap.append(wrap)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.wrap)
        self.ui.tableWidget.resizeColumnsToContents()
        for row in range(0, self.ui.tableWidget.rowCount()):
            for col in range(0, self.ui.tableWidget.columnCount()):
                if self.ui.tableWidget.item(row, col) is not None:
                    self.ui.tableWidget.item(row, col).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                else:
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.tableWidget.setItem(row, col, item)
                    self.ui.tableWidget.item(row, col).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)


    def get_koeff_day_week_data(self):
        category = self.category
        start_date = self.periodDay[0].toString('yyyy-MM-dd')
        end_date = self.periodDay[1].toString('yyyy-MM-dd')
        koeff_day_week_data = self.database.get_koeff_day_week_data_in_DB(start_date, end_date, category)
        if "Ошибка" in koeff_day_week_data:
            self.show_DB_error_message(koeff_day_week_data)
            return
        else:
            return koeff_day_week_data

    def show_success_message(self, message):
        pass

    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def closeEvent(self, event):
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