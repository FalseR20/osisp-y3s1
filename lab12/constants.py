from pathlib import Path
from typing import Final

PROJECT_PATH: Final = Path(__file__).resolve().parent.joinpath("styles")
STYLES_PATH: Final = PROJECT_PATH.joinpath("common.qss")
