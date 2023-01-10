# -*- coding: utf-8 -*-

import logging
import uuid
from typing import List, Dict
from drug_analysis.helpers.utils import date_parser
from drug_analysis.loaders import Loader
from drug_analysis.data_models.Article import Article

logger = logging.getLogger(__name__)

class ArticleLoader(Loader):
    """
    Load article data.
    """

    def __init__(self):
        super().__init__()


    def preprocess_data(self, raw_data: List[Dict]):
        """
        Load article data and conduct some sanity checks :
         - check number of columns should be 4 for each data_line
         - try to parse date
        :return: list of objects of type JournalArticles
        """
        article_list = []
        for ix, data_line in enumerate(raw_data):
            if len(data_line) != 4:
                raise Exception(f"was expecting 4 columns in {self.file_path}, but {len(data_line)} was found")

            title_column = "scientific_title" if "scientific_title" in data_line else "title" # to adapt to article format

            if data_line["date"] and data_line[title_column]:
                obj_id = str(uuid.uuid4()) #assuming the ids on the sample are just csv row numbers
                parsed_date = date_parser(data_line["date"])

                # we can apply some text processing here (checking unicode, removing stop words, case, stripping spaces etc ...
                #  i'll only apply lower casing to avoid missing drugs
                # another way to handle this is to use fuzzy regex expression to allow a certain degree of flexibility
                title = data_line[title_column].lower()
                journal = data_line["journal"]

                article_list.append(Article(id=obj_id, date=parsed_date, title=title, journal=journal))
            else:
                logger.warning(f"missing data in line {ix +1} in {self.file_path}, investigate")

        return article_list