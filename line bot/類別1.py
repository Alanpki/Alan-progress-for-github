from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Wj9T82/vSGVl88Y5xF0S4k0Hq20uwtVNjRPCrnW1jMsk9S3/SiXDDXMs1hJI3tovRu+BPdU8G4QCbMX+2qmbCFhouipWDv9YTJShk6T5Orkl25I2qAzpSrso0pZCVwNyaOI9kgyB2Fcsq389DdwrYgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1fe894ab85e47ff1ee0d47b24b15dde9')


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


if __name__ == "__main__":
    app.run()