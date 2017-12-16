#!/usr/bin/python
# -*- coding: utf-8 -*-
from clarifai.rest import ClarifaiApp

from helpers.common_helper import *

"""
insightbot001@muimail.com|123456|fd39233efbb3404db3c928911bd9f2d7
insightbot002@muimail.com|123456|e8757c0b54484c74994db97aea112ebd
insightbot003@muimail.com|123456|d1708e8c17394744b73bfbb95b0f7cfd
"""

CLARIFAI_API_KEY = 'fb5a8a64f0964e1499c04886f34f0d66'

clarifai_app = ClarifaiApp(api_key=CLARIFAI_API_KEY)

image_embedding_model = clarifai_app.models.get('general-v1.3', model_type='embed')
apparel_model = clarifai_app.models.get('apparel')


def get_image_embedding_from_urls(urls):
    assert isinstance(urls, list) and len(urls) > 0, 'URLs is invalid!'
    try:
        images = []
        for url in urls:
            images.append(clarifai_app.inputs.create_image_from_url(url=url, allow_duplicate_url=True))
        response = image_embedding_model.predict(inputs=images)
        if response['status']['code'] == 10000:
            results = []
            for item in response['outputs']:
                if response['status']['code'] != 10000:
                    debug(item['input']['data']['image']['url'])
                results.append(item['data']['embeddings'][0]['vector'])
            return results
    except Exception as e:
        log(e)
    return None


def get_image_embedding_from_objects(objects):
    assert isinstance(objects, list) and len(objects) > 0, 'Objects is invalid!'
    try:
        images = []
        for obj in objects:
            images.append(clarifai_app.inputs.create_image_from_bytes(img_bytes=obj, allow_duplicate_url=True))
        response = image_embedding_model.predict(inputs=images)
        if response['status']['code'] == 10000:
            results = []
            for item in response['outputs']:
                if response['status']['code'] != 10000:
                    debug(item['input']['data']['image']['url'])
                results.append(item['data']['embeddings'][0]['vector'])
            return results
    except Exception as e:
        log(e)
    return None


def get_image_concepts_from_objects(objects):
    assert isinstance(objects, list) and len(objects) > 0, 'Objects is invalid!'
    try:
        images = []
        for obj in objects:
            images.append(clarifai_app.inputs.create_image_from_bytes(img_bytes=obj, allow_duplicate_url=True))
        response = apparel_model.predict(inputs=images)
        if response['status']['code'] == 10000:
            results = []
            for item in response['outputs']:
                if response['status']['code'] != 10000:
                    debug(item['input']['data']['image']['url'])

                concepts = item['data']['concepts']
                for concept in concepts:
                    del concept['id']
                    del concept['app_id']

                results.append(concepts)

            return results
    except Exception as e:
        log(e)
    return None


def main():
    pass


if __name__ == '__main__':
    main()
