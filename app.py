import os
from flask import Flask, request, abort, make_response

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

import requests

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['Channel_Access_Token'])
handler = WebhookHandler(os.environ['Channel_Secret'])

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
