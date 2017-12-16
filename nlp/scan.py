#!/usr/bin/python
# -*- coding: utf8 -*-
import itertools
import logging
import re

import utils


class Scan(object):
    def __init__(self, keywords=None):
        self._logger = logging.getLogger(__name__)
        # Builds keywords
        self.keywords = {}
        if keywords is not None:
            for id, keyword in keywords:
                new_keywords = itertools.permutations(keyword.split(' '))
                for new_keyword in new_keywords:
                    self.keywords[' '.join(new_keyword).lower()] = id
        self.regex = re.compile('|'.join(sorted(self.keywords.keys(), key=len, reverse=True)), re.IGNORECASE)

    def extract_keywords(self, string):
        ids = set()
        try:
            matcher = self.regex.findall(string.lower())
            for m in matcher:
                ids.add(self.keywords[m])
        except Exception as e:
            self._logger.exception(e)
        return list(ids)

    """
    Lưu cấu hình
    """

    def load(self, file_name):
        self.keywords, self.regex = utils.deserialize(file_name)

    """
    Phục hồi cấu hình
    """

    def store(self, file_name):
        utils.serialize((self.keywords, self.regex), file_name)
