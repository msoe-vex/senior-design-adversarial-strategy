from asyncio.log import logger
from dataclasses import dataclass
from logging import Logger


@dataclass
class LoggingManager():
    logger: Logger = Logger()

    @classmethod
    def get_logger(cls):
        return logger
