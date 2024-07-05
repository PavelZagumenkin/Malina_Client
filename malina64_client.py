import sys
from PyQt6 import QtWidgets
from data.windows.windows_authorization import WindowAuthorization


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    WindowAuthorization = WindowAuthorization()
    WindowAuthorization.show()
    WindowAuthorization.check_update()
    sys.exit(app.exec())