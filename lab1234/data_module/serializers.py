import json

from data_module.data_classes import CalendarEventData, Data
from PyQt6 import QtCore


def data_to_json(data: Data) -> str:
    return json.dumps(
        {
            date.toString(): [
                {"description": calendar_event.description, "time": calendar_event.time.toString()}
                for calendar_event in calendar_events
            ]
            for date, calendar_events in data.items()
        }
    )


def data_from_json(data_json: str) -> Data:
    data_dict = json.loads(data_json)
    data = {
        QtCore.QDate.fromString(date_str): [
            CalendarEventData(calendar_event["description"], QtCore.QTime.fromString(calendar_event["time"]))
            for calendar_event in calendar_events
        ]
        for date_str, calendar_events in data_dict.items()
    }
    return data
