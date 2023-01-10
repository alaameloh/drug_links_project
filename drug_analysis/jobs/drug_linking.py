# -*- coding: utf-8 -*-

import logging
from typing import Dict, List
from drug_analysis.loaders.DrugLoader import DrugLoader
from drug_analysis.loaders.ArticleLoader import ArticleLoader
from drug_analysis.helpers.utils import write_graph
from drug_analysis.helpers.constants import PREFERED_DATE_FORMAT

logger = logging.getLogger(__name__)


def update_drug_linking_graph(graph_entry: Dict, article_list: List, article_type: str):
    """
    insert the observation depending on the type of article in the graph element
    :param graph_entry: graph element that represents one drug
    :param article_list: list of all pubmed or clinical trials objects
    :param article_type: type of the article in article_list, either pubmed or clinical_trial
    :return: updated graph element
    """
    journal_date_appearance_tracker = set()
    for article in article_list:
        if graph_entry["drug_name"] in article.title:  # both already lower case

            graph_entry[article_type].append(
                {
                    "referenced_in": article.title,
                    "reference_date": article.date.strftime(PREFERED_DATE_FORMAT)
                }

            )

            journals_entry = (
                article.journal,
                article.date.strftime(PREFERED_DATE_FORMAT)
            )

            # avoid adding duplicates. we assume the situation doesnt arise with articles if there's no repeated article
            if journals_entry in journal_date_appearance_tracker:
                continue

            graph_entry["journals"].append(
                {
                    "referenced_in": article.journal,
                    "reference_date": article.date.strftime(PREFERED_DATE_FORMAT)
                }
            )

    return graph_entry


def build_drug_linking_graph(drug_file_path, clinical_trials_path, pubmed_csv_path, pubmed_json_path):
    """
    graph generation function
    :param drug_file_path: drug file path
    :param clinical_trials_path: clinical trials' path
    :param pubmed_csv_path: pubmed_1 file path
    :param pubmed_json_path: pubmed_2 file path
    :return: graph of drugs connected with their appearances in journals, pubmed and clinical trials
    """
    logger.info("loading and preprocessing data")

    drugs_data_loader = DrugLoader()
    raw_drugs_data = drugs_data_loader.load_data(drug_file_path)
    drugs_data = drugs_data_loader.preprocess_data(raw_drugs_data)

    article_loader = ArticleLoader()

    raw_clinical_trials = article_loader.load_data(clinical_trials_path)
    clinical_trials = article_loader.preprocess_data(raw_clinical_trials)

    raw_pubmed_csv = article_loader.load_data(pubmed_csv_path)
    pubmed_csv = article_loader.preprocess_data(raw_pubmed_csv)

    raw_pubmed_json = article_loader.load_data(pubmed_json_path)
    pubmed_json = article_loader.preprocess_data(raw_pubmed_json)

    # makes sense to concat both pubmed data
    pubmed = pubmed_csv + pubmed_json

    logger.info("Construct drug linking graph")
    output_graph = []

    for drug in drugs_data:
        drug_graph_entry = {
            "drug_name": drug.name,
            "drug_atc_code": drug.atc_code,
            "journals": [],
            "clinical_trials": [],
            "pubmed": []
        }
        drug_graph_entry = update_drug_linking_graph(drug_graph_entry, pubmed, "pubmed")
        drug_graph_entry = update_drug_linking_graph(drug_graph_entry, clinical_trials, "clinical_trials")
        output_graph.append(drug_graph_entry)
    return output_graph


def run(drug_file_path, clinical_trials_path, pubmed_csv_path, pubmed_json_path, output_path):
    """
    run drug linking pipeline and output the expected json
    :param drug_file_path
    :param clinical_trials_path
    :param pubmed_csv_path
    :param pubmed_json_path
    :param output_path
    :return:
    """
    graph = build_drug_linking_graph(drug_file_path, clinical_trials_path, pubmed_csv_path, pubmed_json_path)
    write_graph(graph, output_path)
    logger.info(f"final graph constructed  at : {output_path}")
