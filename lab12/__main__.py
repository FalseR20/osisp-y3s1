import sys
from pathlib import Path

from PyQt6 import QtWidgets

from lab12.main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.setStyle("Linux")
    styles_path = Path(__file__).resolve().parent / "styles.qss"
    app.setStyleSheet(open(styles_path).read())
    app.exec()
