# -*- coding: utf-8 -*-

from drug_analysis.loaders import Loader
from drug_analysis.data_models.Drug import Drug
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DrugLoader(Loader):
    """
    Load drug data.
    """

    def __init__(self):
        super().__init__()

    def preprocess_data(self, raw_data: List[Dict]):
        """
        validate the presence of two non-null values (according to sample data) 
        :return: cleaned data in list of dict format
        """
        drugs_list = []
        for ix, data_line in enumerate(raw_data):
            if len(data_line) != 2:
                raise Exception(f"was expecting 2 columns in {self.file_path}, but {len(data_line)} was found")

            if not all(data_line.values()):
                logger.warning(f"line {ix +1} in {self.file_path}, investigate")
                continue

            drugs_list.append(Drug(data_line["atccode"], data_line["drug"].lower()))

        return drugs_list
