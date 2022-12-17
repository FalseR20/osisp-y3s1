from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import QDateTime
from PyQt6.QtGui import QColor


@dataclass
class CalendarEvent:
    description: str
    begin: QDateTime
    end: QDateTime
    color: QColor
    repeat: int

    def __lt__(self, other: CalendarEvent):
        return self.begin < other.begin
