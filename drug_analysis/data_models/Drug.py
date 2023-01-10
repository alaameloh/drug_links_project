# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class Drug:
    atc_code: str
    name: str

    def is_valid(self):
        """validate the format of the atc_code"""
        pass
