# -*- coding: utf-8 -*-
import logging

import pytest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from unittest.mock import patch
from tests.data import inputs
from drug_analysis.loaders import Loader
from drug_analysis.loaders.DrugLoader import DrugLoader
from drug_analysis.loaders.ArticleLoader import ArticleLoader
from drug_analysis.jobs.drug_linking import build_drug_linking_graph
from drug_analysis.jobs import adhoc_processing


def mock_load_data(self, file_path):
    """
    we only use this class to set "file_path" param and bypass loading data from local file. we'll be parametrizing the tests
    instead.
    the scope is simple for our usecase and doesnt really require a mock / patch, but if we were loading data
    from a remote source or required network com, we'd need to mock that behavior for the tests
    """
    self.file_path = file_path
    return "placeholder_result"

# proposing two versions of fixtures : patched loaders and normal loaders
#  patched loaders allow us to quickly test validation logic on data without having to modify raw input files
#  normal loaders allow us to test the logic of graph generation.
@pytest.fixture
def patched_drug_loader_fixture():
    with patch.object(DrugLoader, "load_data", mock_load_data):
        yield DrugLoader()

@pytest.fixture
def patched_article_loader_fixture():
    with patch.object(ArticleLoader, "load_data", mock_load_data):
        yield ArticleLoader()


@pytest.mark.parametrize("drug_data", inputs.non_valid_drug_data())
def test_exceptions_are_raised_when_drug_data_is_not_valid(drug_data, patched_drug_loader_fixture):
    with pytest.raises(ValueError):
        patched_drug_loader_fixture.load_data("mock_file")  # only to set the file_name attribute
        drugs_list = patched_drug_loader_fixture.preprocess_data(drug_data)

@pytest.mark.parametrize("article_data", inputs.non_valid_article_data())
def test_if_exceptions_are_raised_when_article_data_is_not_valid(article_data, patched_article_loader_fixture):
    with pytest.raises(ValueError):
        patched_article_loader_fixture.load_data("mock_file")  # only to set the file_name attribute
        drugs_list = patched_article_loader_fixture.preprocess_data(article_data)


# when having multiple test cases, we can have a fixture that lists the folders's content and maps the filenames
#  to the correct paramaeter
def test_graph_generation():
    output_graph = build_drug_linking_graph(
        drug_file_path="data/test_files/case_1/drugs.csv",
        clinical_trials_path="data/test_files/case_1/clinical_trials.csv",
        pubmed_csv_path="data/test_files/case_1/pubmed.csv",
        pubmed_json_path="data/test_files/case_1/pubmed.json"
    )
    expected_graph = Loader.read_json("data/test_files/case_1/expected_graph.json5")
    assert output_graph == expected_graph


def test_adhoc_processing():
    best_journal, mentioned_drugs = adhoc_processing.run("data/test_files/case_1/expected_graph.json5")
    expected_results = Loader.read_json("data/test_files/case_1/expected_best_journal.json5")
    assert best_journal == expected_results["best_journal"] and len(mentioned_drugs) == expected_results["nb_mentioned_drugs"]
