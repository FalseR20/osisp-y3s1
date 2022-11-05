from functools import partial

import constants
from data_module import CalendarEventData, Data, load_data, save_data
from logging_ import get_logger
from PyQt6 import QtCore, QtWidgets, QtGui
from widgets.add_event_dialog import AddEventDialog


class MainWindow(QtWidgets.QMainWindow):
    current_selected_date: QtCore.QDate

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = get_logger(self.__class__.__module__)

        # Main window
        self.setObjectName("mainWindow")
        self.setFixedSize(constants.MAIN_WINDOW_SIZE)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        # Menu
        self.menu_bar = self.menuBar()
        self.help_menu = self.menu_bar.addMenu("&Help")
        self.info_action = QtGui.QAction("&Info")
        self.help_menu.addAction(self.info_action)
        self.info_action.triggered.connect(self.info_event)  # type: ignore

        # Calendar widget
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setGeometry(constants.CALENDAR_WIDGET_GEOMETRY)
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.selectionChanged.connect(self.selection_changed_event)  # type: ignore

        # Button for adding new calendar event
        self.addCalendarEventButton = QtWidgets.QPushButton(self.centralwidget)
        self.addCalendarEventButton.setObjectName("newEventButton")
        self.addCalendarEventButton.setGeometry(constants.ADD_CALENDAR_EVENT_BUTTON_GEOMETRY)
        self.addCalendarEventButton.setFont(constants.ADD_CALENDAR_EVENT_BUTTON_FONT)
        self.addCalendarEventButton.clicked.connect(self.add_calendar_event)  # type: ignore

        # Scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(constants.SCROLL_AREA_GEOMETRY)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)

        # Scroll area widget
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidget.setObjectName("scrollAreaWidget")
        self.scrollArea.setWidget(self.scrollAreaWidget)

        # Layout
        self.eventsLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
        self.eventsLayout.setObjectName("eventsLayout")
        self.eventsLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Retranslate
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Календарь"))
        self.addCalendarEventButton.setText(_translate("mainWindow", "Добавить событие"))

        # Pre-run logic
        self.events_dict: Data = load_data()
        self.save_data = partial(save_data, self.events_dict)
        self.selection_changed_event()
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_calendar_event(self) -> None:
        event_unit, is_ok = AddEventDialog().exec_new()
        self.logger.debug("Dialog exec: event_unit = %s, is_ok = %s", event_unit, is_ok)
        if not is_ok:
            return
        if not self.events_dict.get(self.current_selected_date):
            self.events_dict[self.current_selected_date] = []
        self.events_dict[self.current_selected_date].append(event_unit)
        self.save_data()
        self.update_layout()

    def selection_changed_event(self) -> None:
        self.current_selected_date = self.calendarWidget.selectedDate()
        self.update_layout()

    def update_layout(self) -> None:
        self.logger.debug("Selected date: %s", self.current_selected_date)
        for i in reversed(range(self.eventsLayout.count())):  # Clear layout
            self.eventsLayout.removeWidget(self.eventsLayout.itemAt(i).widget())
        if events_list := self.events_dict.get(self.current_selected_date):
            for event_dict in events_list:
                self.eventsLayout.addWidget(self.create_calendar_event_widget(event_dict))

    def create_calendar_event_widget(self, event_unit: CalendarEventData) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        widget.setFixedSize(constants.CALENDAR_EVENT_WIDGET_SIZE)
        change_button = QtWidgets.QPushButton(widget)
        change_button.setFixedSize(constants.CALENDAR_EVENT_CHANGE_BUTTON_SIZE)
        change_button.clicked.connect(partial(self.change_calendar_event_event, event_unit))  # type: ignore
        change_button.setFont(constants.CALENDAR_EVENT_BUTTON_FONT)
        change_button.setStyleSheet(constants.CALENDAR_EVENT_CHANGE_BUTTON_STYLE)
        change_button.setText(f"{event_unit.time.toString('hh:mm'):10}{event_unit.description}")
        delete_button = QtWidgets.QPushButton(widget)
        delete_button.setGeometry(constants.CALENDAR_EVENT_DELETE_BUTTON_GEOMETRY)
        delete_button.setFont(constants.CALENDAR_EVENT_BUTTON_FONT)
        delete_button.setStyleSheet(constants.CALENDAR_EVENT_DELETE_BUTTON_STYLE)
        delete_button.setText("del")
        delete_button.clicked.connect(partial(self.delete_calendar_event_event, event_unit))  # type: ignore
        return widget

    def delete_calendar_event_event(self, event_unit: CalendarEventData) -> None:
        self.events_dict[self.current_selected_date].remove(event_unit)
        self.save_data()
        self.update_layout()

    def change_calendar_event_event(self, event_unit: CalendarEventData) -> None:
        self.logger.debug("Dialog exec before: event_unit = %s", event_unit)
        is_ok = AddEventDialog().exec_change(event_unit)
        self.logger.debug("Dialog exec after: event_unit = %s, is_ok = %s", event_unit, is_ok)
        if not is_ok:
            return
        self.save_data()
        self.update_layout()

    @staticmethod
    def info_event():
        msg_box = QtWidgets.QMessageBox()
        # msg_box.setFont(constants.)
        msg_box.setFixedSize(QtCore.QSize(700, 880))
        msg_box.setWindowTitle("Info")
        msg_box.setText("Created by FalseR\n(c) All rights reserved")
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg_box.exec()
