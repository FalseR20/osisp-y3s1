from functools import partial
from logging import getLogger

from data_module import CalendarEvent, Data
from PyQt6 import QtCore, QtGui, QtWidgets
from widgets import constants
from widgets.CalendarEventDialog import CalendarEventDialog


class MainWindow(QtWidgets.QMainWindow):
    current_selected_date: QtCore.QDate

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = getLogger(self.__class__.__module__)

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
        self.data = Data()
        self.selection_changed_event()
        QtCore.QMetaObject.connectSlotsByName(self)

    def selection_changed_event(self) -> None:
        self.current_selected_date = self.calendarWidget.selectedDate()
        self.update_layout()

    def update_layout(self) -> None:
        self.logger.debug("Selected date: %s", self.current_selected_date)
        for i in reversed(range(self.eventsLayout.count())):  # Clear layout
            self.eventsLayout.removeWidget(self.eventsLayout.itemAt(i).widget())
        if events_list := self.data[self.current_selected_date]:
            for event in events_list:
                self.eventsLayout.addWidget(self.create_calendar_event_widget(event))

    def create_calendar_event_widget(self, event_unit: CalendarEvent) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        widget.setFixedSize(constants.CALENDAR_EVENT_WIDGET_SIZE)
        change_button = QtWidgets.QPushButton(widget)
        change_button.setFixedSize(constants.CALENDAR_EVENT_CHANGE_BUTTON_SIZE)
        change_button.clicked.connect(partial(self.change_calendar_event_event, event_unit))  # type: ignore
        change_button.setFont(constants.CALENDAR_EVENT_BUTTON_FONT)
        change_button.setStyleSheet(constants.CALENDAR_EVENT_CHANGE_BUTTON_STYLE)
        change_button.setAutoFillBackground(True)
        change_button.setPalette(QtGui.QPalette(event_unit.color))

        time_format = "hh:mm"
        datetime_format = f"dd.MM.yyyy {time_format}"
        text = f"""{
        event_unit.begin.time().toString(time_format) 
        if self.current_selected_date == event_unit.begin.date() 
        else event_unit.begin.toString(datetime_format)
        } - {
        event_unit.end.time().toString(time_format)
        if self.current_selected_date == event_unit.end.date()
        else event_unit.end.toString(datetime_format)
        }"""
        change_button.setText(f"{text} | {event_unit.description}")
        ##
        # diff = QtCore.QDateTime.currentDateTime().secsTo(event_unit.end)
        # if diff > 0:
        #     timer = QtCore.QTimer(widget)
        #     timer.t
        #     timer.timeout.connect(self.timeout)  # type: ignore
        #     timer.start(1000)
        ##
        delete_button = QtWidgets.QPushButton(widget)
        delete_button.setGeometry(constants.CALENDAR_EVENT_DELETE_BUTTON_GEOMETRY)
        delete_button.setFont(constants.CALENDAR_EVENT_BUTTON_FONT)
        delete_button.setStyleSheet(constants.CALENDAR_EVENT_DELETE_BUTTON_STYLE)
        delete_button.setText("del")
        delete_button.clicked.connect(partial(self.delete_calendar_event_event, event_unit))  # type: ignore
        return widget

    def add_calendar_event(self) -> None:
        calendar_event, is_ok = CalendarEventDialog(self.current_selected_date).exec_new()
        self.logger.debug("Dialog exec: event_unit = %s, is_ok = %s", calendar_event, is_ok)
        if not is_ok:
            return
        self.data.append(calendar_event)
        self.update_layout()

    def delete_calendar_event_event(self, event_unit: CalendarEvent) -> None:
        self.data.remove(event_unit)
        self.update_layout()

    def change_calendar_event_event(self, event_unit: CalendarEvent) -> None:
        self.logger.debug("Dialog exec before: event_unit = %s", event_unit)
        is_ok = CalendarEventDialog(self.current_selected_date).exec_change(event_unit)
        self.logger.debug("Dialog exec after: event_unit = %s, is_ok = %s", event_unit, is_ok)
        if not is_ok:
            return
        self.data.save()
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

    # def timeout(self, *_):
    #     print(_)
