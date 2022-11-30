import sys

from PyQt6 import QtWidgets
from widgets.main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
