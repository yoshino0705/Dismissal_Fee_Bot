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
    text = generate_plans_list(event.message.text)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))
    
def generate_plans_list(msg_text):
    decoded_plans = Decode(msg_text)    
    
    if not decoded_plans.plans:
        plans_text = '無此方案或未提電信名，或關鍵詞中間無空格，例如: " 中699 " 應為 " 中 699 "'
    else:
        plans_text = '請選擇一個方案: (輸入數字)\n'
        index = 0
        for k in decoded_plans.plans.keys():
            plans_text += '{}) {}\n'.format(index, k)
            index += 1
    return plans_text

if __name__ == "__main__":
    app.run()
