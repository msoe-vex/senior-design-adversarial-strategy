from dataclasses import dataclass
import json
from typing import Dict
from logging import getLogger
from functools import partial
from src.entities.constants import PARSER_LOGGER_NAME


class Config:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)    


def dict_config_parser(config_file_path: str) -> Dict:
    loaded_dict = dict()

    with open(config_file_path, 'r') as f:
            loaded_dict = json.load(f)

    return loaded_dict


def init_config_parser(obj_base: partial, config_file_path: str=None, config_dict: Dict=dict()) -> object:
    if config_file_path is None and not config_dict:
        getLogger(PARSER_LOGGER_NAME).warning("init_config_parser not given dict or file, continuing without args")

    if config_file_path is not None:
        config_dict = dict_config_parser(config_file_path)

    configured_obj = obj_base(**config_dict) # Dict unpacking into partial constructor

    return configured_obj


def obj_config_parser(config_file_path: str=None, config_dict: Dict=dict()) -> Config:
    return init_config_parser(partial(Config), config_file_path, config_dict)