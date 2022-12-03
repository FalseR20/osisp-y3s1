from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from PyQt6 import QtCore


@dataclass
class CalendarEventBegin:
    description: str
    begin: QtCore.QDateTime
    end: Optional[CalendarEventEnd]


@dataclass
class CalendarEventEnd:
    end: QtCore.QDateTime
    begin: CalendarEventBegin


Data = dict[QtCore.QDate, list[Union[CalendarEventBegin, CalendarEventEnd]]]
