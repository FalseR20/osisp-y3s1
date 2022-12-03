from logging import getLogger

import requests
from data_module.Data import Data
from data_module.serializers import data_from_json, data_to_json

logger = getLogger()

URL = "http://127.0.0.1:5000/"


def save_data(data: Data) -> None:
    data_json = data_to_json(data)
    logger.debug("Save data: %s", data_json)
    requests.post(URL, data_json)


def load_data() -> Data:
    data_json = requests.get(URL).content.decode()
    logger.debug("Load data: %s", data_json)
    return data_from_json(data_json)
