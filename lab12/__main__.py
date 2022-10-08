import sys
from PyQt6 import QtWidgets
from lab12.main_window import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
