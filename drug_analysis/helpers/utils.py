# -*- coding: utf-8 -*-

import json5
from typing import Dict, List
from dateutil import parser
import logging
logger = logging.getLogger(__name__)

def date_parser(date_str: str):
    """
    parses a string into a datetime object if possible, otherwise raises ValueError
    :raises ValueError if the format is unknown
    :param date_str
    :return: date in datetime object
    """
    try:
        date = parser.parse(date_str)
        return date
    except ValueError:
        logger.exception(f"unknown date format : {date_str}")
        raise ValueError


def write_graph(graph: List[Dict], file_path):
    """
    This function write object (dict, list of dicts) in json file
    :param result: object that will be written in json file
    :param file_path: output path
    :return: void
    """
    with open(file_path, 'w', encoding='utf8') as f:
        json5.dump(graph, f)
