from linebot.models import FlexSendMessage
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

line_bot_api = LineBotApi('9bVl3s9/2vOkd/N+8uozWtusOyAReJjDYBNxF9j7ujE9cLHifXRMDu7oducQXlj8Ru+BPdU8G4QCbMX+2qmbCFhouipWDv9YTJShk6T5Orl6Ozu0OcH1G04TUegc4V5o2Ga409Y2lRBT+ZduhRIyAwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1fe894ab85e47ff1ee0d47b24b15dde9')

@handler.add(MessageEvent, message=TextMessage)
IMGUR_CLIENT_ID = imgur_client_id

def plot_stcok_k_chart(IMGUR_CLIENT_ID,stock="0050" , date_from='2020-01-01' ):
    """
    進行個股K線繪製，回傳至於雲端圖床的連結。將顯示包含5MA、20MA及量價關係，起始預設自2020-01-01起迄昨日收盤價。
    :stock :個股代碼(字串)，預設0050。
    :date_from :起始日(字串)，格式為YYYY-MM-DD，預設自2020-01-01起。
    """
    stock = str(stock)+".tw"
    df = web.DataReader(stock, 'yahoo', date_from) 
    mpf.plot(df,type='candle',mav=(5,20),volume=True, ylabel=stock.upper()+' Price' ,savefig='testsave.png')
    PATH = "testsave.png"
    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=stock+" candlestick chart")
    return uploaded_image.link

def plot_stcok_k_chart(IMGUR_CLIENT_ID,stock="0050" , date_from='2020-01-01' ):
    """
    進行個股K線繪製，回傳至於雲端圖床的連結。將顯示包含5MA、20MA及量價關係，起始預設自2020-01-01起迄昨日收盤價。
    :stock :個股代碼(字串)，預設0050。
    :date_from :起始日(字串)，格式為YYYY-MM-DD，預設自2020-01-01起。
    """
    stock = str(stock)+".tw"
    df = web.DataReader(stock, 'yahoo', date_from) 
    mpf.plot(df,type='candle',mav=(5,20),volume=True, ylabel=stock.upper()+' Price' ,savefig='testsave.png')
    PATH = "testsave.png"
    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=stock+" candlestick chart")
    return uploaded_image.link

def handle_message(event):
    if event.message.text[:2].upper() == "#K":
        input_word = event.message.text.replace(" ","") #合併字串取消空白
        stock_name = input_word[2:6] #0050
        start_date = input_word[6:] #2020-01-01
        content = plot_stcok_k_chart(IMGUR_CLIENT_ID,stock_name,start_date)

        flex_message = FlexSendMessage(
            alt_text=stock_name, #alt_text
            contents={
                'type': 'bubble',
                'direction': 'ltr',
                'hero': {
                    'type': 'image',
                    'url': content,
                    'size': 'full',
                    'aspectRatio': '20:13',
                    'aspectMode': 'cover',
                    'action': { 'type': 'uri', 'uri': content, 'label': 'label' }
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message) 