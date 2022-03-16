import logging
from entities.constants import (
    PARSER_LOGGER_NAME,
    REPRESENTATION_LOGGER_NAME,
    SIMULATION_LOGGER_NAME,
)


def configure_loggers() -> None:
    formatter = logging.Formatter("[%(created)f] | [%(levelname)s] | %(filename)s:%(lineno)d | %(message)s")

    parser_logger = logging.getLogger(PARSER_LOGGER_NAME)
    parser_logger.setLevel(logging.DEBUG)

    representation_logger = logging.getLogger(REPRESENTATION_LOGGER_NAME)
    representation_logger.setLevel(logging.DEBUG)

    simulation_logger = logging.getLogger(SIMULATION_LOGGER_NAME)
    simulation_logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    parser_logger.addHandler(sh)
    representation_logger.addHandler(sh)
    simulation_logger.addHandler(sh)