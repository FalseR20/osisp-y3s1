from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import QDateTime


@dataclass
class CalendarEvent:
    description: str
    begin: QDateTime
    end: QDateTime

    def __lt__(self, other: CalendarEvent):
        return self.begin < other.begin
