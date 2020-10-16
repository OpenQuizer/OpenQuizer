import math
from func import proc
from flask import Flask, request

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = '2x2e71Yb1o+cjufGxWSfdUdYgVICAPAYITenyiLW3tBPA0NtmqapJtezdjn0NqC63B/4TfXBjUkMES+hE62mg6oLbOaPBZF0bnMZQoX4pxRDZjKy80yti82Oa0lCjmgLdZAUYByXU1QhPcrsffqhOgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'b304f3ce9c97b39885f9439032ed3f51'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))






@app.route('/')
def main():
    return 'Hello, this is willywangkaa first Heroku project! Autobuildtest'

@app.route('/test')
def test():
    return 'test 12 12'

@app.route('/package')
def package():
    return str(math.pi)

@app.route('/page')
def htmlpage():
    with open('main_page.html', 'r') as f:
        contents = f.read()
    return contents

@app.route('/coop')
def coop():
    return proc()

if __name__ == "__main__":
    app.run()