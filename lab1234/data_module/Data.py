from __future__ import annotations

from typing import List

from data_module import CalendarEvent
from data_module.file_connector import load_data, save_data
from PyQt6.QtCore import QDate, QDateTime

# from data_module.server_connector import load_data, save_data


class Data:
    events: List[CalendarEvent]

    def __init__(self) -> None:
        self.events = load_data()

    def __getitem__(self, date: QDate) -> List[CalendarEvent]:
        events = [event for event in self.events if event.begin.date() <= date <= event.end.date()]
        events = sorted(events, key=_key_begin)
        return events

    def save(self) -> None:
        save_data(self.events)

    def append(self, calendar_event: CalendarEvent) -> None:
        self.events.append(calendar_event)
        self.save()

    def remove(self, calendar_event: CalendarEvent) -> None:
        self.events.remove(calendar_event)
        self.save()


def _key_begin(calendar_event: CalendarEvent) -> QDateTime:
    return calendar_event.begin
