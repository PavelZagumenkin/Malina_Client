# Form implementation generated from reading ui file 'mini_table_window.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_mini_table_window(object):
    def setupUi(self, mini_table_window):
        mini_table_window.setObjectName("mini_table_window")
        mini_table_window.resize(1280, 720)
        mini_table_window.setMinimumSize(QtCore.QSize(1280, 720))
        mini_table_window.setMaximumSize(QtCore.QSize(1280, 720))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(14)
        mini_table_window.setFont(font)
        mini_table_window.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        mini_table_window.setMouseTracking(False)
        mini_table_window.setTabletTracking(False)
        mini_table_window.setAutoFillBackground(False)
        mini_table_window.setStyleSheet("background-color: #fff")
        self.centralwidget = QtWidgets.QWidget(mini_table_window)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_back = QtWidgets.QPushButton(self.centralwidget)
        self.btn_back.setGeometry(QtCore.QRect(1030, 650, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_back.setFont(font)
        self.btn_back.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.btn_back.setStyleSheet("QPushButton {\n"
"background-color: rgb(228, 107, 134);\n"
"border: none;\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover {\n"
"border: 1px solid  rgb(0, 0, 0);\n"
"background-color: rgba(228, 107, 134, 0.9)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border:3px solid  rgb(0, 0, 0);\n"
"background-color: rgba(228, 107, 134, 1)\n"
"}")
        self.btn_back.setCheckable(False)
        self.btn_back.setObjectName("btn_back")
        self.label_windowName = QtWidgets.QLabel(self.centralwidget)
        self.label_windowName.setGeometry(QtCore.QRect(10, 10, 1261, 51))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(26)
        self.label_windowName.setFont(font)
        self.label_windowName.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_windowName.setObjectName("label_windowName")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 271, 171))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        mini_table_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(mini_table_window)
        QtCore.QMetaObject.connectSlotsByName(mini_table_window)

    def retranslateUi(self, mini_table_window):
        _translate = QtCore.QCoreApplication.translate
        mini_table_window.setWindowTitle(_translate("mini_table_window", "Таблица"))
        self.btn_back.setText(_translate("mini_table_window", "НАЗАД"))
        self.btn_back.setShortcut(_translate("mini_table_window", "Return"))
        self.label_windowName.setText(_translate("mini_table_window", "ТЕКСТ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mini_table_window = QtWidgets.QMainWindow()
    ui = Ui_mini_table_window()
    ui.setupUi(mini_table_window)
    mini_table_window.show()
    sys.exit(app.exec())
