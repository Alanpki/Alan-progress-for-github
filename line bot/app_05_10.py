import requests
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

line_bot_api = LineBotApi('9bVl3s9/2vOkd/N+8uozWtusOyAReJjDYBNxF9j7ujE9cLHifXRMDu7oducQXlj8Ru+BPdU8G4QCbMX+2qmbCFhouipWDv9YTJShk6T5Orl6Ozu0OcH1G04TUegc4V5o2Ga409Y2lRBT+ZduhRIyAwdB04t89/1O/w1cDnyilFU=')
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
    input_text = event.message.text
    
    resp = requests.get('https://tw.rter.info/capi.php')
    currency_data = resp.json()

    if input_text == '查詢匯率' or input_text == '匯率查詢':
        
        usd_to_jpd = currency_data['USDJPY']['Exrate']
        usd_to_twd = currency_data['USDTWD']['Exrate']
        twd_to_jpd =usd_to_twd/usd_to_jpd
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'台幣 TWD 對日幣 JPY：1:{twd_to_jpd}'))
    elif '換' in input_text:
        have_coin=input_text[0:3]
        want_coin=input_text[-3:]
        have_change=currency_data["USD"+have_coin]['Exrate']
        want_change=currency_data["USD"+want_coin]['Exrate']
        need_change=want_change/have_change
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="{}換{}=1:{}".format(have_coin,want_coin,need_change)))

    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
if __name__ == "__main__":
    app.run(port=5000)