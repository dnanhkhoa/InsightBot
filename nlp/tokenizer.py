#!/usr/bin/python
# -*- coding: utf8 -*-
import json
import logging

import requests


class Tokenizer(object):
    class __Impl(object):

        COMMON_TOKENS = 'date|hhmmss|percent|name|phrase|allcaps|fraction|email|number\\d+|entity|word'

        def __init__(self, service_url):
            self._logger = logging.getLogger(__name__)
            self.service_url = service_url

        def tokenize(self, text, pattern=None):
            try:
                data = {'text': text.encode('UTF-8')}
                if pattern is not None:
                    data['pattern'] = pattern.encode('UTF-8')
                response = requests.post(self.service_url + '/tokenize', data=data, timeout=15)
                if response.status_code == 200:
                    return json.loads(response.content.decode('UTF-8'))
            except Exception as e:
                self._logger.exception(e)
            return None

        def advanced_tokenize(self, text, pattern=None):
            try:
                data = {'text': text.encode('UTF-8')}
                if pattern is not None:
                    data['pattern'] = pattern.encode('UTF-8')
                response = requests.post(self.service_url + '/advanced_tokenize', data=data, timeout=15)
                if response.status_code == 200:
                    tokens = json.loads(response.content.decode('UTF-8'))
                    return [(token[0], token[1]) for token in tokens]
            except Exception as e:
                self._logger.exception(e)
            return None

    __instance = None

    def __new__(cls, service_url=None):
        if cls.__instance is None:
            assert service_url is not None, 'Please provide service url!'
            cls.__instance = cls.__Impl(service_url)
        return cls.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
