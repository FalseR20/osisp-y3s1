import json
import pathlib
import pickle
from dataclasses import dataclass
from pprint import pprint

from PyQt6 import QtCore

_DATA_FOLDER = pathlib.Path(__file__).resolve().parent.joinpath("data")
_DATA_FOLDER.mkdir(exist_ok=True)
_DATA_FILE = _DATA_FOLDER.joinpath("data-v1.pkl")


@dataclass
class CalendarEventData:
    description: str
    time: QtCore.QTime


Data = dict[QtCore.QDate, list[CalendarEventData]]


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


def save_data(data: Data) -> None:
    with open(_DATA_FILE, "wb") as file:
        pickle.dump(data, file)


def load_data() -> Data:
    if not _DATA_FILE.exists():
        return {}
    with open(_DATA_FILE, "rb") as file:
        data = pickle.load(file)
        pprint(data)
        pprint(data_to_json(data))
        return data
