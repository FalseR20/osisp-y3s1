import pathlib
import pickle

from PyQt6.QtCore import QDate

DATA_FOLDER = pathlib.Path(__file__).resolve().parent.joinpath("data")
DATA_FOLDER.mkdir(exist_ok=True)
DATA_FILE = DATA_FOLDER.joinpath("data.pkl")


def save_data(data: dict[QDate, list[str]]) -> None:
    with open(DATA_FILE, "wb") as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


def load_data() -> dict[QDate, list[str]]:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "rb") as file:
        return pickle.load(file)
