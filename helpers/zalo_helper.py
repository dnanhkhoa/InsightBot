#!/usr/bin/python
# -*- coding: utf-8 -*-
from helpers.common_helper import *
from zalo.sdk.app.Zalo3rdAppClient import Zalo3rdAppClient
from zalo.sdk.app.ZaloAppInfo import ZaloAppInfo

APP_ID = ''
SECRET_KEY = ''

ZALO_ERROR_CODES = {
    '-201': 'Invalid parameter',
    '-202': 'Mac invalid',
    '-204': 'Official Account deleted',
    '-205': 'Official Account does not exist',
    '-207': 'Official Account are not a 3rd party',
    '-208': 'Official Account no secret key',
    '-209': 'This API is not supported',
    '-210': 'Parameter exceeds the permissible limits',
    '-211': 'all quota',
    '-212': 'Official Account unregistered this api',
    '-213': 'Users not interested Official Account',
    '-214': 'Article being processed',
    '-215': 'App id is invalid',
    '-216': 'Invalid access token',
    '-217': 'The user has blocked message inviting interested',
    '-218': 'All quota received',
    '-219': 'Unregistered phone numbers Zalo',
    '0': 'Message sent successfully invited interested',
    'first': 'Api was called success',
    '-20 109': 'Send a message to the phone number or account not interested OA',
    '-20 009': 'Picture does not exist or is invalid'
}

# Initialize Zalo
zalo_info = ZaloAppInfo(app_id=APP_ID, secret_key=SECRET_KEY)
zalo_3rd_app_client = Zalo3rdAppClient(zalo_info)


def build_shop_from_data():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
