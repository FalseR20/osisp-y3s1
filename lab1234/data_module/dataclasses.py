from dataclasses import dataclass

from PyQt6 import QtCore


@dataclass
class CalendarEventData:
    description: str
    time: QtCore.QTime


Data = dict[QtCore.QDate, list[CalendarEventData]]
