from PyQt6 import QtCore, QtGui, QtWidgets

from lab12.add_event_dialog import AddEventDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
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
        self.pushButton.clicked.connect(self.add)  # type: ignore

    @staticmethod
    def add(_):
        dialog = AddEventDialog()
        dialog.exec()
