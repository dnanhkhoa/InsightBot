#!/usr/bin/python
# -*- coding: utf8 -*-
import itertools
import logging
import re

from nlp import Scan


class SplittedScan(Scan):
    def __init__(self, keywords=None):
        self._logger = logging.getLogger(__name__)
        # Builds keywords
        self.keywords = {}
        if keywords is not None:
            for id, keyword in keywords:
                for token in keyword.split(','):
                    token = token.strip()
                    if len(token) == 0:
                        continue
                    new_keywords = itertools.permutations(token.split(' '))
                    for new_keyword in new_keywords:
                        self.keywords[' '.join(new_keyword).lower()] = id
        self.regex = re.compile('|'.join(sorted(self.keywords.keys(), key=len, reverse=True)), re.IGNORECASE)
