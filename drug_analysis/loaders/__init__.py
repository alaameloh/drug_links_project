# -*- coding: utf-8 -*-

import csv
import json5
from typing import List, Dict


class Loader:
    """
    Generic class for loading data.
    for now the sources can be a csv or json file, but it can be a remote storage, DB, distruted FS etc
    """

    def __init__(self):
        pass

    def load_data(self, file_path):
        self.file_path = file_path
        if file_path.endswith(".csv"):
            raw_data = self.read_csv(file_path)
        elif file_path.endswith(".json"):
            raw_data = self.read_json(file_path)
        else:
            raise NotImplementedError("non handled file format")
        return raw_data

    @staticmethod
    def read_csv(file_path: str):
        """
        This function reads a csv file
        :param file_path: the path to the csv file
        :return: list of dicts that contains the csv rows (dict key is the first row name)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = csv.DictReader(f)
            return list(data)

    @staticmethod
    def read_json(file_path: str):
        """
        This function reads a json file
        :param file_path: the path to the json file
        :return: the json file as a python dict
        """
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json5.load(f)
            return data

    def preprocess_data(self, raw_data: List[Dict]):
        pass
