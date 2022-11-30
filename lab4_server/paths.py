from pathlib import Path

SRC_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = SRC_FOLDER.joinpath("data")
DATA_FOLDER.mkdir(exist_ok=True)
DATA_FILE = DATA_FOLDER.joinpath("data1.txt")
