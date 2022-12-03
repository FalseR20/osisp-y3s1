import json

from data_module.data_classes import CalendarEventBegin, Data
from PyQt6 import QtCore


def data_to_json(data: Data) -> str:
    return json.dumps(
        {
            date.toString(): [
                {
                    "description": calendar_event.description,
                    "begin": calendar_event.begin.toString(),
                    "end": calendar_event.end.toString(),
                }
                for calendar_event in calendar_events
            ]
            for date, calendar_events in data.items()
        }
    )


def data_from_json(data_json: str) -> Data:
    data_dict = json.loads(data_json)
    data = {
        QtCore.QDate.fromString(date_str): [
            CalendarEventBegin(
                calendar_event["description"],
                QtCore.QTime.fromString(calendar_event["begin"]),
                QtCore.QTime.fromString(calendar_event["end"]),
            )
            for calendar_event in calendar_events
        ]
        for date_str, calendar_events in data_dict.items()
    }
    return data
