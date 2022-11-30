from .paths import DATA_FILE


def save_data(data: bytes) -> None:
    with open(DATA_FILE, "wb") as file:
        file.write(data)


def load_data() -> bytes:
    if not DATA_FILE.exists():
        return b"{}"
    with open(DATA_FILE, "rb") as file:
        data = file.read()
        return data


def load_data_str() -> str:
    if not DATA_FILE.exists():
        return "{}"
    with open(DATA_FILE, "rb") as file:
        data = str(file.read())
        return data
