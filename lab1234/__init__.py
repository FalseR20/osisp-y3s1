import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s - "%(message)s"',
    datefmt="%H:%M:%S",
)
