# -*- coding: utf-8 -*-

import argparse
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Options for the drug analysis pipeline')
parser.add_argument("-d", "--drugs", help="Path for the drugs csv file")
parser.add_argument("-c", "--clinical_trials", help="Path for the clinical trials csv file")
parser.add_argument("-pc", "--pubmed_csv", help="Path for the pubmed csv file")
parser.add_argument("-pj", "--pubmed_json", help="Path for the pubmed json file")
parser.add_argument("-o", "--output", help="Path for the output json file")

args = parser.parse_args()

def link_drugs():
    """
    run the drug linking pipeline
    :return:
    """
    from drug_analysis.jobs import drug_linking as job

    # set params
    job.run(drug_file_path=args.drugs,
            clinical_trials_path=args.clinical_trials,
            pubmed_csv_path=args.pubmed_csv,
            pubmed_json_path=args.pubmed_json,
            output_path=args.output,

            )


def adhoc_processing():
    """
    run the adhoc processing task
    :return:
    """
    from drug_analysis.jobs import adhoc_processing as job

    # set params
    job.run(json_path=args.output)