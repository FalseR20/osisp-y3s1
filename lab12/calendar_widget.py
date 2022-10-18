from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets


class CalendarWidget(QtWidgets.QCalendarWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget], event):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 700, 400))
        self.setObjectName("calendarWidget")
        self.clicked.connect(event)

    # def actionEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if event.type() == QtGui.QMouseEvent.Type.MouseButtonPress:
    #         self.mouse_event()
