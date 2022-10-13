from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QInputDialog

from logging_ import get_logger


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = get_logger(self.__class__.__module__)
        self.setObjectName("mainWindow")
        self.resize(700, 900)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 700, 400))
        self.calendarWidget.setObjectName("calendarWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 430, 500, 80))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslate()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Календарь"))
        self.pushButton.setText(_translate("mainWindow", "Добавить событие"))
        self.pushButton.clicked.connect(self.add_event)  # type: ignore

    def add_event(self, _):
        text, ok = QInputDialog.getText(self, "Event", "Enter name of event")
        self.logger.debug("%s", text)
