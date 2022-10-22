import pathlib
import pickle
from dataclasses import dataclass

from PyQt6 import QtCore

_DATA_FOLDER = pathlib.Path(__file__).resolve().parent.joinpath("data")
_DATA_FOLDER.mkdir(exist_ok=True)
_DATA_FILE = _DATA_FOLDER.joinpath("data.pkl")


@dataclass
class EventUnit:
    description: str
    time: QtCore.QTime


Data = dict[QtCore.QDate, list[EventUnit]]


def save_data(data: Data) -> None:
    with open(_DATA_FILE, "wb") as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


def load_data() -> Data:
    if not _DATA_FILE.exists():
        return {}
    with open(_DATA_FILE, "rb") as file:
        return pickle.load(file)
