import logging
import sys

from PyQt6 import QtWidgets

from main_window import MainWindow

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s:%(lineno)d - \"%(message)s\"",
    datefmt="%H:%M:%S"
)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.setStyle("Linux")
    app.exec()
