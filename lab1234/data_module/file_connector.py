import pickle
from logging import getLogger
from typing import List

from data_module.CalendarEvent import CalendarEvent
from data_module.paths import DATA_FILE

logger = getLogger()


def save_data(data: List[CalendarEvent]) -> None:
    with open(DATA_FILE, "wb") as file:
        pickle.dump(data, file)
    logger.debug("Save data: %s", data)


def load_data() -> List[CalendarEvent]:
    if not DATA_FILE.exists():
        logger.debug("Load data: no file")
        return []
    with open(DATA_FILE, "rb") as file:
        data = pickle.load(file)
        logger.debug("Load data: %s", data)
        return data
