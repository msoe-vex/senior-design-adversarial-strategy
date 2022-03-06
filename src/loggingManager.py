import logging
from entities.constants import REPRESENTATION_LOGGER_NAME, SIMULATION_LOGGER_NAME

def configure_loggers() -> None:
    representation_logger = logging.getLogger(REPRESENTATION_LOGGER_NAME)
    representation_logger.setLevel(logging.INFO)

    simulation_logger = logging.getLogger(SIMULATION_LOGGER_NAME)
    simulation_logger.setLevel(logging.INFO)