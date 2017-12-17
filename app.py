#!/usr/bin/python
# -*- coding: utf-8 -*-
import apiai
from flask import Flask, request
from flask_cors import CORS
from zalo.sdk.oa.ZaloOaClient import ZaloOaClient
from zalo.sdk.oa.ZaloOaInfo import ZaloOaInfo

from helpers import *

# ==========================================================

app = Flask(__name__)
CORS(app)
# ==========================================================
DIALOGFLOW_CLIENT_ACCESS_TOKEN = '4cae8727e6fb4aaeb818eb8bb15cdcac'
dialogflow = apiai.ApiAI(DIALOGFLOW_CLIENT_ACCESS_TOKEN)
# ==========================================================
ZALO_APP_ID = '488785924369824329'
ZALO_SECRET_KEY = '1sqL17v9m2MnC0NXXUkM'
oa_info = ZaloOaInfo(oa_id=ZALO_APP_ID, secret_key=ZALO_SECRET_KEY)
zalo_oa_client = ZaloOaClient(oa_info)
# ==========================================================
contexts = {}
database = read_json('data/shop.json')


def get_profile_name(user_id):
    profile = zalo_oa_client.get('/getprofile', {'uid': user_id})
    return profile['data']['displayName']


def text_request_dialogflow(user_id, query):
    res = dialogflow.text_request()
    res.session_id = user_id
    res.query = query
    return json.loads(res.getresponse().read().decode('UTF-8'))


def send_text_zalo(user_id, message):
    data = {
        'uid': user_id,
        'message': message
    }
    params = {'data': data}
    send_text_message = zalo_oa_client.post('/sendmessage/text', params)
    return send_text_message['errorMsg'] == 'Success'


def send_image_zalo(user_id, image_path, message=None):
    upload_photo_from_path = zalo_oa_client.post('/upload/image', {'file': image_path})
    if upload_photo_from_path['errorMsg'] != 'Success':
        return False

    data = {
        'uid': user_id,
        'imageid': upload_photo_from_path['data']['imageId'],
        'message': message
    }
    params = {
        'data': data
    }
    send_image_message = zalo_oa_client.post('/sendmessage/image', params)
    return send_image_message['errorMsg'] == 'Success'


def send_receipt(user_id, receipt):
    msg = 'Mã sản phẩm: %s\nTên sản phẩm: %s\nTên người mua: %s\nĐiện thoại: %s\nĐịa chỉ: %s\nGiá: %s' % (
        receipt['product_id'], receipt['product'], receipt['name'], receipt['phone'], receipt['location'],
        receipt['price'])
    send_text_zalo(user_id, msg)


@app.route('/')
def index():
    return 'Insight Bot is running!'


@app.route('/zalo_webhook', methods=['GET'])
def zalo_webhook():
    args = request.args
    event = args.get('event')
    if event in ['sendmsg', 'sendlocationmsg']:
        user_id = args.get('fromuid')
        message = args.get('message')

        # Get profile name
        if user_id not in contexts or 'profile_name' not in contexts[user_id]:
            if contexts.get('user_id') is None:
                contexts[user_id] = {'receipts': []}
            contexts[user_id]['profile_name'] = get_profile_name(user_id)

        # Convert to lowercase
        message = message.lower()
        debug('Before: %s' % message)

        # Correct spelling if needed
        message = correct_spelling(msg=message)
        debug('After: %s' % message)

        if event == 'sendlocationmsg':
            params = json.loads(args.get('params'))
            message = get_address(params.get('latitude'), params.get('longitude'))
            debug(message)

        # Hook something here
        if 'wait_location' in contexts[user_id]:
            contexts[user_id]['location'] = message
            del contexts[user_id]['wait_location']
            if 'phone' in contexts[user_id]:
                # Create receipt
                receipt = {
                    'product_id': contexts[user_id]['temp_product']['productId'],
                    'product': contexts[user_id]['temp_product']['name'],
                    'name': contexts[user_id]['profile_name'],
                    'phone': contexts[user_id]['phone'],
                    'location': contexts[user_id]['location'],
                    'price': contexts[user_id]['temp_product']['price']
                }
                contexts[user_id]['receipts'].append(receipt)
                send_receipt(user_id, receipt)
            else:
                contexts[user_id]['wait_phone'] = True
                send_text_zalo(user_id, 'Bạn cho mình xin thông tin số điện thoại nhé.')
                return 'Zalo Webhook'
        elif 'wait_phone' in contexts[user_id]:
            contexts[user_id]['phone'] = message
            # Create receipt
            receipt = {
                'product_id': contexts[user_id]['temp_product']['productId'],
                'product': contexts[user_id]['temp_product']['name'],
                'name': contexts[user_id]['profile_name'],
                'phone': message,
                'location': contexts[user_id]['location'],
                'price': contexts[user_id]['temp_product']['price']
            }
            contexts[user_id]['receipts'].append(receipt)
            send_receipt(user_id, receipt)
            del contexts[user_id]['wait_phone']
            return 'Zalo Webhook'
        # End hook

        response = text_request_dialogflow(user_id, message)
        debug(response)
        if response['status']['errorType'] == 'success':
            if response['result']['action'].startswith('##') or response['result']['action'] in ['input.unknown',
                                                                                                 'input.welcome',
                                                                                                 'product.search.suggest']:
                send_text_zalo(user_id,
                               response['result']['fulfillment']['speech'].replace('$profile_name',
                                                                                   contexts[user_id]['profile_name']))
            elif response['result']['action'] == 'product.search':
                # Promo
                item = ''
                if len(response['result']['parameters']['item']) > 0:
                    item = response['result']['parameters']['item']
                if len(response['result']['parameters']['category']) > 0:
                    item = response['result']['parameters']['category']

                items = []
                for i in database:
                    if len(items) == 5:
                        break
                    if 'name' not in i or 'category' not in i:
                        continue
                    if item in i['name'].lower() or item in i['category'].lower():
                        items.append(i)

                if len(items) > 0:
                    for item in items:
                        msg = '[%s] - %s - Giá chỉ từ: %s' % (item['productId'], item['name'], item['price'])
                        send_image_zalo(user_id, 'data/images/' + item['imgUrl'], msg)
                    send_text_zalo(user_id,
                                   'Có vài sản phẩm thỏa yêu cầu của bạn, chỉ cần nhập mã sản phẩm bạn muốn mua và mình sẽ hoàn tất việc đặt hàng giùm bạn. :D')
                else:
                    send_text_zalo(user_id, 'Tiếc quá, hiện tại bên mình không có sản phẩm mà bạn cần tìm. :(')

            elif response['result']['action'] == 'order':
                product_id = response['result']['parameters']['productid']
                product = None
                flag = True
                for item in database:
                    if item['productId'] == product_id:
                        product = item
                        flag = False
                        break
                if flag:
                    send_text_zalo(user_id, 'Mã số sản phẩm bạn chọn không đúng. :(')
                else:
                    if 'location' in contexts[user_id] and 'phone' in contexts[user_id]:
                        # Create receipt
                        receipt = {
                            'product_id': product['productId'],
                            'product': product['name'],
                            'name': contexts[user_id]['profile_name'],
                            'phone': message,
                            'location': contexts[user_id]['location'],
                            'price': contexts[user_id]['temp_product']['price']
                        }
                        contexts[user_id]['receipts'].append(receipt)
                        send_receipt(user_id, receipt)
                    else:
                        contexts[user_id]['temp_product'] = product
                        if 'location' not in contexts[user_id]:
                            contexts[user_id]['wait_location'] = True
                            send_text_zalo(user_id, 'Bạn cho mình xin thông tin địa chỉ để giao hàng nhé.')
                        elif 'phone' not in contexts[user_id]:
                            contexts[user_id]['wait_phone'] = True
                            send_text_zalo(user_id, 'Bạn cho mình xin thông tin số điện thoại nhé.')
            elif response['result']['action'] == 'receipts':
                if len(contexts[user_id]['receipts']) > 0:
                    for receipt in contexts[user_id]['receipts']:
                        send_receipt(user_id, receipt)
                else:
                    send_text_zalo(user_id, 'Hiện không có hóa đơn nào.')
    return 'Zalo Webhook'


def main():
    global contexts
    context_file = 'contexts.json'
    if path_info(context_file):
        contexts = read_json(context_file)

    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)
    write_json(contexts, context_file)


if __name__ == '__main__':
    main()
