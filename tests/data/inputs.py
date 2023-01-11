# -*- coding: utf-8 -*-

def non_valid_drug_data():
    data = (
        [{"atccode": "1", "drug": "drug_1", "extra_field": "abc"}],
        [{"atccode": "2"}],
    )
    yield from data


def non_valid_article_data():
    data = (
        [{"id": "1", "title": "article_1", "date": "01/01/2023", "journal": "journal_1", "extra_field": "extra_text"}],
        [{"id": "1", "title": "article_1", "date": "01/01/2023"}],
    )
    yield from data