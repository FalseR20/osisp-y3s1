from functools import partial

import data_saver
from logging_ import get_logger
from PyQt6 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window
        self.logger = get_logger(self.__class__.__module__)
        self.setObjectName("mainWindow")
        self.setFixedSize(700, 880)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        # Central widget
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 700, 400))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.clicked.connect(self.select_new_date_event)  # type: ignore
        self.calendarWidget.setGridVisible(True)
        self.current_selected_date: QtCore.QDate = self.calendarWidget.selectedDate()

        # Button for adding new event
        self.newEventButton = QtWidgets.QPushButton(self.centralwidget)
        self.newEventButton.setObjectName("newEventButton")
        self.newEventButton.setGeometry(QtCore.QRect(20, 420, 660, 60))
        self.newEventButtonFont = QtGui.QFont()
        self.newEventButtonFont.setPointSize(20)
        self.newEventButtonFont.setWeight(50)
        self.newEventButton.setFont(self.newEventButtonFont)
        self.newEventButton.clicked.connect(self.add_new_event)  # type: ignore

        # Scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(QtCore.QRect(20, 500, 660, 360))
        # self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        # Layout
        self.eventsLayout = QtWidgets.QVBoxLayout()
        self.eventsLayout.setObjectName("eventsLayout")

        self.scrollAreaWidget.setLayout(self.eventsLayout)

        self.events_dict: dict[QtCore.QDate, list[str]] = data_saver.load_data()
        self.select_new_date()
        self.retranslate()
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_new_event(self):
        text, is_ok = QtWidgets.QInputDialog.getText(self, "Event", "Enter name of event")
        self.logger.debug("Input dialog: text = '%s', is_ok = %s", text, is_ok)
        if not is_ok:
            return
        if not self.events_dict.get(self.current_selected_date):
            self.events_dict[self.current_selected_date] = [text]
        else:
            self.events_dict[self.current_selected_date].append(text)
        data_saver.save_data(self.events_dict)
        self.select_new_date()

    def select_new_date_event(self, date: QtCore.QDate):
        self.current_selected_date = date
        self.select_new_date()

    def select_new_date(self):
        self.logger.debug("Selected date: %s", self.current_selected_date)
        for i in reversed(range(self.eventsLayout.count())):  # Clear layout
            self.eventsLayout.removeWidget(self.eventsLayout.itemAt(i).widget())

        if events_list := self.events_dict.get(self.current_selected_date):
            for event_desc in events_list:
                self.eventsLayout.addWidget(self.create_event_widget(event_desc))
        self.eventsLayout.addStretch()

    def create_event_widget(self, event_desc: str):
        button = QtWidgets.QPushButton()
        button.setFixedSize(QtCore.QSize(620, 50))
        button.clicked.connect(partial(self.change_event, event_desc))  # type: ignore
        button.setText(event_desc)
        button.setFont(self.newEventButtonFont)
        return button

    def change_event(self, event: str):
        text, is_ok = QtWidgets.QInputDialog.getText(self, "Event", "Enter new name of event")
        self.logger.debug("Input dialog (change %s): text = '%s', is_ok = %s", event, text, is_ok)
        if not is_ok:
            return
        events_list = self.events_dict[self.current_selected_date]
        event_i = events_list.index(event)
        events_list[event_i] = text
        data_saver.save_data(self.events_dict)
        self.select_new_date()

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Календарь"))
        self.newEventButton.setText(_translate("mainWindow", "Добавить событие"))
