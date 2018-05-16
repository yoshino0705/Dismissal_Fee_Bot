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

from Decode import Decode
from Contract import Contract

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
    decoded_plans = Decode(event.message.text)
    plans_text = '\n'.join([k for k in decoded_plans.plans.keys()])    
    if not plans_text:
        plans_text = '無此方案或未提電信名，或關鍵詞中間無空格，例如: " 中699 " 應為 " 中 699 "'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=plans_text))

if __name__ == "__main__":
    app.run()
