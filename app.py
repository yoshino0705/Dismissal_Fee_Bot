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

from Switcher import Switcher
from Access_Database import Access_Info

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
    if event.source.type == "room":
        r_id = event.source.room_id # should've named room id, which is unique
    else:
        r_id = event.source.user_id
        
    ai_con = Access_Info(r_id)
    ai_con.create_info()
    sw = Switcher(ai_con, event.message.text)
    text = sw.execute()
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))

if __name__ == "__main__":
    app.run()
