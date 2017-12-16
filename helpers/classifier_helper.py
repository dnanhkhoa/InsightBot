#!/usr/bin/python
# -*- coding: utf8 -*-
import logging

from nltk import NaiveBayesClassifier, apply_features

import nlp
import utils


class NaiveBayes(object):
    def __init__(self, stopwords=None):
        self._logger = logging.getLogger(__name__)
        self.classifier = None
        self.stopwords = [] if stopwords is None else stopwords

    def extract_features(self, sentence):
        tokens = nlp.Tokenizer().tokenize(sentence.lower(),
                                          pattern=nlp.Tokenizer().COMMON_TOKENS)
        return {token: True for token in tokens if token not in self.stopwords}

    def train(self, sentences):
        try:
            training_set = apply_features(self.extract_features, sentences)
            self.classifier = NaiveBayesClassifier.train(training_set)
        except Exception as e:
            self.classifier = None
            self._logger.exception(e)

    def prob_classify(self, sentence):
        assert self.classifier is not None, 'Please train model before classifying'
        dist = self.classifier.prob_classify(self.extract_features(sentence))
        return {label: dist.prob(label) for label in dist.samples()}

    def classify(self, sentence):
        assert self.classifier is not None, 'Please train model before classifying'
        dist = self.classifier.prob_classify(self.extract_features(sentence))
        label = dist.max()
        return label, dist.prob(label)

    def save(self, file_name):
        utils.serialize((self.classifier, self.stopwords), file_name)

    def load(self, file_name):
        self.classifier, self.stopwords = utils.deserialize(file_name)
