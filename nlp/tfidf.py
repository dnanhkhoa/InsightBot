#!/usr/bin/python
# -*- coding: utf8 -*-
import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import utils
from nlp import Tokenizer


class TFIDF(object):
    def __init__(self, default_tokenizer=True, stopwords=None):
        self.map = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.default_tokenizer = default_tokenizer
        self.stopwords = stopwords
        self._logger = logging.getLogger(__name__)

    @staticmethod
    def tokenize(string):
        return Tokenizer().tokenize(string.lower(), pattern=Tokenizer().COMMON_TOKENS)

    """
    Lập chỉ mục danh sách các documents
    """

    def index(self, documents):
        try:
            self.map, documents = zip(*documents)
            self.map = dict(enumerate(self.map))

            if self.default_tokenizer:
                self.tfidf_vectorizer = TfidfVectorizer(stop_words=self.stopwords)
            else:
                self.tfidf_vectorizer = TfidfVectorizer(tokenizer=self.tokenize, stop_words=self.stopwords)

            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(list(documents))
        except Exception as e:
            self.map = None
            self.tfidf_vectorizer = None
            self.tfidf_matrix = None
            self._logger.exception(e)

    """
    Tìm và trả về indices theo thứ tự điểm giảm dần
    """

    def search(self, document):
        assert self.tfidf_vectorizer is not None and self.tfidf_matrix is not None, \
            'Please index documents before searching'
        distance = cosine_similarity(self.tfidf_vectorizer.transform([document]), self.tfidf_matrix)[0]
        return sorted((map(lambda x: (self.map[x[0]], x[1]), enumerate(distance))), key=lambda x: x[1],
                      reverse=True)

    """
    Lưu cấu hình
    """

    def load(self, file_name):
        self.tfidf_vectorizer, self.tfidf_matrix, self.map, self.default_tokenizer = utils.deserialize(file_name)

    """
    Phục hồi cấu hình
    """

    def store(self, file_name):
        utils.serialize((self.tfidf_vectorizer, self.tfidf_matrix, self.map, self.default_tokenizer), file_name)
