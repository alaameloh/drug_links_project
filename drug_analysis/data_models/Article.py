# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    """
    since pubmed and clinical_trials data samples share the same structure, this class can be used as a common model
     for both
    """
    id: str
    date: datetime
    title: str
    journal: str
