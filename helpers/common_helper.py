#!/usr/bin/python
# -*- coding: utf-8 -*-
# DONE
import base64
import json
import logging
import os
import pickle
import re
from io import BytesIO
from os.path import splitext

import requests
from PIL import Image
from geopy.geocoders import Nominatim
from requests import RequestException

DEBUG = True

_LOGGER = logging.getLogger(__name__)

_APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))


def log(msg):
    _LOGGER.exception(msg=msg)


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def path(*name):
    assert name is not None, 'Name is invalid!'
    return os.path.join(_APP_PATH, *name)


def path_info(name):
    assert name is not None, 'Name is invalid!'
    name = path(name)
    if len(name) > 0 and os.path.exists(name):
        if os.path.isfile(name):
            return 1
        if os.path.isdir(name):
            return -1
    return 0


def make_dirs(name):
    assert name is not None, 'Name is invalid!'
    name = path(name)
    if len(name) > 0 and path_info(name) >= 0:
        os.makedirs(name)


def read_file(file_name):
    file_name = path(file_name)
    assert path_info(file_name) == 1, 'File do not exist!'
    with open(file_name, 'rb') as f:
        try:
            return f.read().decode('UTF-8')
        except Exception as e:
            log(e)


def write_file(data, file_name):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            f.write(data.encode('UTF-8'))
        except Exception as e:
            log(e)


def read_bytes(file_name):
    file_name = path(file_name)
    assert path_info(file_name) == 1, 'File do not exist!'
    with open(file_name, 'rb') as f:
        try:
            return f.read()
        except Exception as e:
            log(e)


def write_bytes(data, file_name):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            f.write(data)
        except Exception as e:
            log(e)


def serialize(obj, file_name):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            pickle.dump(obj, f)
        except Exception as e:
            log(e)


def deserialize(file_name):
    file_name = path(file_name)
    assert path_info(file_name) == 1, 'File do not exist!'
    with open(file_name, 'rb') as f:
        try:
            return pickle.load(f)
        except Exception as e:
            log(e)


def read_lines(file_name):
    file_name = path(file_name)
    assert path_info(file_name) == 1, 'File do not exist!'
    lines = []
    with open(file_name, 'rb') as f:
        try:
            for line in f:
                lines.append(line.decode('UTF-8').rstrip('\r\n'))
        except Exception as e:
            log(e)
    return lines


def write_lines(lines, file_name, end_line='\n'):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            for line in lines:
                f.write((line + end_line).encode('UTF-8'))
        except Exception as e:
            log(e)


def read_json(file_name):
    file_name = path(file_name)
    assert path_info(file_name) == 1, 'File do not exist!'
    with open(file_name, 'rb') as f:
        try:
            return json.loads(f.read().decode('UTF-8'))
        except Exception as e:
            log(e)


def write_json(obj, file_name):
    file_name = path(file_name)
    make_dirs(os.path.dirname(file_name))
    with open(file_name, 'wb') as f:
        try:
            f.write(json.dumps(obj, indent=4, ensure_ascii=False).encode('UTF-8'))
        except Exception as e:
            log(e)


def read_folder(folder_path, has_extension=True, extension_filter=None):
    folder_path = path(folder_path)
    assert path_info(folder_path) == -1, 'Folder do not exist!'
    files = []
    try:
        for child in os.listdir(folder_path):
            if os.path.isfile('%s/%s' % (folder_path, child)):
                parts = splitext(child)
                if extension_filter is None or parts[1] in extension_filter:
                    files.append(child if has_extension else parts[0])
    except Exception as e:
        log(e)
    return files


def download_image_file(url, file_name=None, timeout=15):
    assert url is not None, 'URL is invalid!'
    try:
        response = requests.get(url=url, timeout=timeout, allow_redirects=True)
        if response.status_code == requests.codes.ok:
            content_type = response.headers.get('Content-Type')
            if content_type is None or 'image' not in content_type:
                return None
            content = response.content
            if file_name is None:
                return Image.open(BytesIO(content))
            write_bytes(content, file_name)
    except RequestException as e:
        debug(url)
        log(e)
    return None


def get_image_bytes(image):
    with BytesIO() as f:
        image.save(f, format='PNG')
        return f.getvalue()


def encode_base64(s):
    if isinstance(s, str):
        s = s.encode('UTF-8')
    return base64.b64encode(s).decode('UTF-8')


def decode_base64(s):
    return base64.b64decode(s).decode('UTF-8')


def get_address(latitude, longitude):
    geolocator = Nominatim()
    return geolocator.reverse('%s, %s' % (latitude, longitude)).address


def correct_spelling(msg, timeout=30):
    try:
        payload = {'msg': msg}
        response = requests.post(url='http://insightbotservice.azurewebsites.net/api/googletranslate', data=payload,
                                 timeout=timeout)
        if response.status_code == requests.codes.ok:
            content = json.loads(response.content.decode('UTF-8'))
            if not content['from']['text']['didYouMean']:
                return msg
            content = content['from']['text']['value']
            return re.sub(r'\[([^\[\]]+)\]', r'\1', content, re.DOTALL)
    except Exception as e:
        log(e)
    return None
