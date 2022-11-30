import pickle

from .dataclasses import Data
from .paths import DATA_FILE


def save_data(data: Data) -> None:
    print(f"{repr(data)=}")
    with open(DATA_FILE, "wb") as file:
        pickle.dump(data, file)


def load_data() -> Data:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "rb") as file:
        data = pickle.load(file)
        return data
