from PyQt6 import QtCore, QtGui, QtWidgets

from logging_ import get_logger


class MainWindow(QtWidgets.QMainWindow):
    events_dict: dict[QtCore.QDate, list[str]] = {}

    def __init__(self):
        super().__init__()

        # Main window
        self.logger = get_logger(self.__class__.__module__)
        self.setObjectName("mainWindow")
        self.setFixedSize(700, 880)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 700, 400))
        self.calendarWidget.setObjectName("calendarWidget")
        self.setCentralWidget(self.centralwidget)

        # Scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(QtCore.QRect(50, 430, 600, 400))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Layout
        self.eventsLayout = QtWidgets.QVBoxLayout(self.scrollArea)
        self.eventsLayout.setObjectName("eventsLayout")
        self.elementsSize = QtCore.QSize(self.scrollArea.geometry().width() - 40, 50)

        # Button for adding new event
        self.newEventButton = QtWidgets.QPushButton()
        self.newEventButton.setObjectName("newEventButton")
        self.newEventButton.setFixedSize(self.elementsSize)
        self.newEventButtonFont = QtGui.QFont()
        self.newEventButtonFont.setPointSize(20)
        self.newEventButtonFont.setWeight(50)
        self.newEventButton.setFont(self.newEventButtonFont)
        self.newEventButton.setObjectName("pushButton")

        self.update_scroll_bar()
        self.retranslate()
        QtCore.QMetaObject.connectSlotsByName(self)

    def update_scroll_bar(self):
        # self.eventsLayout.  # Clear
        # date = self.calendarWidget.selectedDate()
        # if events := self.events_dict.get(date):
        #      pass
        self.eventsLayout.addWidget(self.newEventButton)

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Календарь"))
        self.newEventButton.setText(_translate("mainWindow", "Добавить событие"))
        self.newEventButton.clicked.connect(self.add_event)  # type: ignore

    def add_event(self, _):
        text, is_ok = QtWidgets.QInputDialog.getText(self, "Event", "Enter name of event")
        self.logger.debug("Input dialog: text = '%s', is_ok = %s", text, is_ok)
