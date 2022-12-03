from dataclasses import dataclass

from PyQt6 import QtCore


@dataclass
class CalendarEventData:
    description: str
    begin: QtCore.QTime
    end: QtCore.QTime


Data = dict[QtCore.QDate, list[CalendarEventData]]
