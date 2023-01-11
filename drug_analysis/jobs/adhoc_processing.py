# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from drug_analysis.loaders import Loader

logger = logging.getLogger(__name__)

def run(json_path):
    """
    check which journal has most appearances
    :param json_path: path of the graph json file
    :return: void
    """
    graph = Loader.read_json(json_path)
    journal_to_drug_tracker = defaultdict(set)
    for drug_entry in graph:
        journal_references_list = drug_entry["journals"]

        for journal_reference in journal_references_list:
            journal_to_drug_tracker[journal_reference["referenced_in"]].add(drug_entry["drug_name"])

    best_journal = max(journal_to_drug_tracker, key=lambda journal: len(journal_to_drug_tracker[journal]))
    mentioned_drugs = journal_to_drug_tracker[best_journal]

    logger.info(f"the journal mentioning the most different drugs is {best_journal} with {len(mentioned_drugs)} : {mentioned_drugs}")

    return best_journal, mentioned_drugs