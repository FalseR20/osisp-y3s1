from functools import partial

from data_module import Data, EventUnit, load_data, save_data
from logging_ import get_logger
from PyQt6 import QtCore, QtGui, QtWidgets

from lab12.add_event_dialog import AddEventDialog


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

        self.events_dict: Data = load_data()
        self.save_data = partial(save_data, self.events_dict)
        self.update_layout()

        # Retranslate
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Календарь"))
        self.newEventButton.setText(_translate("mainWindow", "Добавить событие"))

        QtCore.QMetaObject.connectSlotsByName(self)

    def add_new_event(self):
        event_unit, is_ok = AddEventDialog().exec_new()
        self.logger.debug("Dialog exec: event_unit = %s, is_ok = %s", event_unit, is_ok)
        if not is_ok:
            return
        if not self.events_dict.get(self.current_selected_date):
            self.events_dict[self.current_selected_date] = []
        self.events_dict[self.current_selected_date].append(event_unit)
        self.save_data()
        self.update_layout()

    def select_new_date_event(self, date: QtCore.QDate):
        self.current_selected_date = date
        self.update_layout()

    def update_layout(self):
        self.logger.debug("Selected date: %s", self.current_selected_date)
        for i in reversed(range(self.eventsLayout.count())):  # Clear layout
            self.eventsLayout.removeWidget(self.eventsLayout.itemAt(i).widget())
        if events_list := self.events_dict.get(self.current_selected_date):
            for event_dict in events_list:
                self.eventsLayout.addWidget(self.create_event_widget(event_dict))
        self.eventsLayout.addStretch()

    def create_event_widget(self, event_unit: EventUnit):
        button = QtWidgets.QPushButton()
        button.setFixedSize(QtCore.QSize(620, 48))
        button.clicked.connect(partial(self.change_event, event_unit))  # type: ignore
        time_label = QtWidgets.QLabel(button)
        time_label.setGeometry(QtCore.QRect(10, 10, 600, 26))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(50)
        time_label.setFont(font)
        time_label.setText(f"{event_unit.time.toString('hh:mm') :10}{event_unit.description}")
        return button

    def change_event(self, event_unit: EventUnit):
        self.logger.debug("Dialog exec before: event_unit = %s", event_unit)
        is_ok = AddEventDialog().exec_change(event_unit)
        self.logger.debug("Dialog exec after: event_unit = %s, is_ok = %s", event_unit, is_ok)
        if is_ok:
            self.save_data()
            self.update_layout()
