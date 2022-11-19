import logging


def get_logger(name: str = "lab12"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger
