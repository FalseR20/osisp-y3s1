from PyQt6 import QtCore, QtGui, QtWidgets

from logging_ import get_logger


class MainWindow(QtWidgets.QMainWindow):
    events_dict: dict[QtCore.QDate, list[QtWidgets.QLabel]] = {}

    def __init__(self):
        super().__init__()

        # Main window and central widget
        self.logger = get_logger(self.__class__.__module__)
        self.setObjectName("mainWindow")
        self.setFixedSize(700, 880)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 700, 400))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.clicked.connect(self.select_new_date_event)  # type: ignore
        self.calendarWidget.setGridVisible(True)
        self.current_selected_date: QtCore.QDate = self.calendarWidget.selectedDate()

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

        # self.select_new_date_event()
        self.retranslate()
        QtCore.QMetaObject.connectSlotsByName(self)

    def select_new_date_event(self, date: QtCore.QDate):
        self.logger.debug("Selected date: %s", date)
        # prev_list = self.events_dict.get(self.current_selected_date)
        # if prev_list:
        #     for event_label in prev_list:
        #         event_label.hide()
        # self.current_selected_date = date
        # self.eventsLayout.  # Clear
        # if events := self.events_dict.get(date):
        #      pass

        # curr_list = self.events_dict.get(self.current_selected_date)
        # if curr_list:
        #     for event_label in curr_list:
        #         event_label.show()
        # self.newEventButton.clicked.connect(self.add_event)  # type: ignore
        # self.eventsLayout.addWidget(self.newEventButton)

    def add_event(self):
        text, is_ok = QtWidgets.QInputDialog.getText(self, "Event", "Enter name of event")
        self.logger.debug("Input dialog: text = '%s', is_ok = %s", text, is_ok)
        # label = QtWidgets.QLabel()
        # label.setText(text)
        # label.hide()
        # date = self.calendarWidget.selectedDate()
        # prev_list = self.events_dict.get(date)
        # if prev_list is None:
        #     self.events_dict[date] = [label]
        #     return
        # prev_list.append(label)

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Календарь"))
        self.newEventButton.setText(_translate("mainWindow", "Добавить событие"))

