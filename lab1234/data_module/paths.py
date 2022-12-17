from paths import SRC_FOLDER

DATA_FOLDER = SRC_FOLDER.joinpath("data")
DATA_FOLDER.mkdir(exist_ok=True)
DATA_FILE = DATA_FOLDER.joinpath("data-v5.pkl")
