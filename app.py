#!/usr/bin/python
# -*- coding: utf-8 -*-
import apiai
import pyrebase
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DIALOGFLOW_ACCESS_TOKEN = ''

dialogflow = apiai.ApiAI(DIALOGFLOW_ACCESS_TOKEN)

FIREBASE_CONFIG = {
    'apiKey': 'AIzaSyB1ZrIfwcoz2lauEqCxeaHVIW0WOUuMyP0',
    'authDomain': 'zalo-insightbot.firebaseapp.com',
    'databaseURL': 'https://zalo-insightbot.firebaseio.com',
    'storageBucket': 'zalo-insightbot.appspot.com',
    'serviceAccount': 'configs/InsightBot-ca1f02be4bf2.json'
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()


@app.route('/')
def index():
    return 'Insight Bot is running!'


@app.route('/zalo_webhook', methods=['POST'])
def zalo_webhook():
    """
    params = request.form
    if 'application/json' in request.content_type:
        params = json.loads(request.data.decode('UTF-8'))
    user_id = params['uid']
    message = params['message']
    command = params['command']
    return core.process(platform=service, request=Request(user_id, message, command))
    """


def main():
    # data = {"name": "Mortimer 'Morty' Smith"}
    # db.child("users").push(data)
    # db.child('users').remove()
    # db.remove()
    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
