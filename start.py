from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from PIL import Image
from io import StringIO

import requests
import random
import json
import math
import time
import datetime

#---------------- self define module ----------------
import text_push as text_push
import text_reply as text_reply

#---------------- self define variables ----------------
from mykey import *
from tourist_spots import *
from food import *
from drink import *

#---------------- line settings ----------------
# Channel Access Token
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#---------------------------------------------------

app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# instruction of pushing code to heroku
# git add .
# git commit -am'ok'
# git push heroku master

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Messgae Types
# 1. Text Message
# 2. Sticker Message
# 3. Image Message
# 4. Video Message
# 5. Audio Message
# 6. Location Message
# 7. Imgaemap Message
# 8. Template Message
# 9. Flex Message

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    print(event)
    message_send_time = float(event.timestamp)/1000
    message_get_time = float(time.time())
    msg_type = event.message.type

    if event.message.text == "info":
        output_message = TextSendMessage(text=str(event))  
        line_bot_api.reply_message(event.reply_token, output_message)

    if event.message.text.lower() == "speed" :
        output_message = ("【收到訊息時間】\n{} 秒\n【處理訊息時間】\n{} 秒".format(message_get_time-message_send_time,float(time.time())-message_get_time))
        output_message = text_reply.text_reply_message(user_message)
        line_bot_api.reply_message(event.reply_token, output_message)

    if msg_type == "sticker":
        output_message = StickerSendMessage(package_Id='1',sticker_Id='1')
        #output_message = StickerSendMessage(package_id='2',sticker_id=str(random.randint(140,180)))
        line_bot_api.reply_message(event.reply_token, output_message)

    elif msg_type == "text":
        user_message = event.message.text

        if user_message == "可樂": 
            output_message = text_reply.text_reply_message("可樂好喝")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == "宏宏的愛人":
            output_message = text_reply.text_reply_message("嵐嵐<3")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == "宏宏的家在哪裡":
            output_message = LocationSendMessage(
                title = "宏宏的家",
                address = "台中市北屯區陳平一街76巷2號5樓-2",
                latitude = "24.186120316114284",
                longitude = "120.66672397075935"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == "肥宅快樂水":
            output_message = ImageSendMessage(
                original_content_url = "https://f.share.photo.xuite.net/chungming01/1fe45d1/10789161/501035944_m.jpg",
                preview_image_url = "https://f.share.photo.xuite.net/chungming01/1fe45d1/10789161/501035944_m.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #首頁
        # elif user_message == "台南旅遊" or "台南" or "旅遊":
        #     output_message = TemplateSendMessage(
        #         alt_text = "此裝置不支援樣板。", #無法支援格式所顯示的文字
        #         template = ButtonsTemplate(
        #             thumbnail_image_url = "https://nurseilife.cc/wp-content/uploads/20170526115242_44.jpg",
        #             title = "台南旅遊",
        #             text = "帶你玩遍美食之都台南",
        #             actions = [
        #                 MessageTemplateAction(
        #                     label = "景點",
        #                     text = "景點"
        #                 ),
        #                 MessageTemplateAction(
        #                     label = "吃的",
        #                     text = "吃的"
        #                 ),
        #                 MessageTemplateAction(
        #                     label = "喝的",
        #                     text = "喝的"
        #                 )
        #             ]
        #         )
        #     )
        #     line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == "台南旅遊":
            reply_arr = []
            output_message1 = text_reply.text_reply_message("您好，請問想查詢什麼呢？")
            
            output_message2 = ImagemapSendMessage(
                base_url = "https://i.imgur.com/0tztQt1.jpg",
                alt_text = "此裝置不支援樣板。", #無法支援格式所顯示的文字
                base_size = BaseSize(height = 2000, width = 2000),
                actions =[
                    #1
                    MessageImagemapAction(
                        text = "台南景點",
                        area = ImagemapArea(x = 0, y= 0, width = 1000, height = 1000)
                    ),
                    #2
                    MessageImagemapAction(
                        text = "台南美食",
                        area = ImagemapArea(x = 1000, y= 0, width = 1000, height = 1000)
                    ),
                    #3
                    MessageImagemapAction(
                        text = "台南飲料",
                        area = ImagemapArea(x = 0, y= 1000, width = 1000, height = 1000)
                    ),
                    #4
                    MessageImagemapAction(
                        text = "台南咖啡廳",
                        area = ImagemapArea(x = 1000, y= 1000, width = 1000, height = 1000)
                    )
                ]
            )
            reply_arr.append(output_message1)
            reply_arr.append(output_message2)
            line_bot_api.reply_message(event.reply_token, reply_arr)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #景點
        elif user_message == "台南景點":
            output_message = tourist_carousel_template()
            line_bot_api.reply_message(event.reply_token, output_message)


        #景點位置區域

        #1
        elif user_message ==f"可由此打開{place1}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place1}",
                address = "台南市中西區民族路二段212號",
                latitude = "22.99762337852117",
                longitude = "120.2024704919533"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #2
        elif user_message == f"可由此打開{place2}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place2}",
                address = "台南市安平區國勝路82號",
                latitude = "23.001593229535548",
                longitude = "120.1606351263452"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #3
        elif user_message == f"可由此打開{place3}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place3}",
                address = "台南市仁德區文華路二段66號",
                latitude = "22.93480286259137",
                longitude = "120.2260482551798"
            )
            line_bot_api.reply_message(event.reply_token, output_message)
        
        #4
        elif user_message == f"可由此打開{place4}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place4}",
                address = "台南市中西區民族路二段212號",
                latitude = "22.99753585895218",
                longitude = "120.19648398291852"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #5
        elif user_message == f"可由此打開{place5}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place5}",
                address = "台南市安平區漁光路114號",
                latitude = "22.98054329215947",
                longitude = "120.15580504320876"
            )            
            line_bot_api.reply_message(event.reply_token, output_message)

        #6
        elif user_message == f"可由此打開{place6}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place6}",
                address = "台南市安平區古堡街108號",
                latitude = "23.003306864536732",
                longitude = "120.15982008130227"
            )            
            line_bot_api.reply_message(event.reply_token, output_message)

        #7
        elif user_message == f"可由此打開{place7}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place7}",
                address = "台南市北區海安路三段533號",
                latitude = "23.01159041194204",
                longitude = "120.20039541306427"
            )            
            line_bot_api.reply_message(event.reply_token, output_message)

        #8
        elif user_message == f"可由此打開{place8}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place8}",
                address = "台南市安平區古堡街196號",
                latitude = "23.002783289337064",
                longitude = "120.15633702634503"
            )            
            line_bot_api.reply_message(event.reply_token, output_message)

        #9
        elif user_message == f"可由此打開{place9}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place9}",
                address = "台南市中西區南門路2號",
                latitude = "22.990712678956807",
                longitude = "120.20431901470467"
            )            
            line_bot_api.reply_message(event.reply_token, output_message)

        #10
        elif user_message == f"可由此打開{place10}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{place10}",
                address = "台南市七股區鹽埕里66號",
                latitude = "23.154298515853103",
                longitude = "120.09994515333189"
            )            
            line_bot_api.reply_message(event.reply_token, output_message)


#-----------------------------------------------------------------------------
        #景點照片區域

        #1
        elif user_message == f"{place1}圖片":
            output_message = image_carousel_message1()
            line_bot_api.reply_message(event.reply_token, output_message)

        #2
        elif user_message == f"{place2}圖片":
            output_message = image_carousel_message2()
            line_bot_api.reply_message(event.reply_token, output_message)
        
        #3
        elif user_message == f"{place3}圖片":
            output_message = image_carousel_message3()
            line_bot_api.reply_message(event.reply_token, output_message)

        #4
        elif user_message == f"{place4}圖片":
            output_message = image_carousel_message4()
            line_bot_api.reply_message(event.reply_token, output_message)

        #5
        elif user_message == f"{place5}圖片":
            output_message = image_carousel_message5()
            line_bot_api.reply_message(event.reply_token, output_message)

        #6
        elif user_message == f"{place6}圖片":
            output_message = image_carousel_message6()
            line_bot_api.reply_message(event.reply_token, output_message)
        
        #7
        elif user_message == f"{place7}圖片":
            output_message = image_carousel_message7()
            line_bot_api.reply_message(event.reply_token, output_message)

        #8
        elif user_message == f"{place8}圖片":
            output_message = image_carousel_message8()
            line_bot_api.reply_message(event.reply_token, output_message)
        
        #9
        elif user_message == f"{place9}圖片":
            output_message = image_carousel_message9()
            line_bot_api.reply_message(event.reply_token, output_message)
        
        #10
        elif user_message == f"{place10}圖片":
            output_message = image_carousel_message10()
            line_bot_api.reply_message(event.reply_token, output_message)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #美食主界面
        elif user_message == "台南美食":
            output_message = TemplateSendMessage(
                alt_text = "此裝置不支援樣板。", #無法支援格式所顯示的文字
                template = ButtonsTemplate(
                    thumbnail_image_url = "https://nurseilife.cc/wp-content/uploads/20170526115242_44.jpg",
                    title = "台南美食",
                    text = "所有的台南佳餚都在這",
                    actions = [
                        MessageTemplateAction(
                            label = "台南美食part1",
                            text = "台南美食part1"
                        ),
                        MessageTemplateAction(
                            label = "台南美食part2",
                            text = "台南美食part2"
                        ),
                        MessageTemplateAction(
                            label = "台南點心",
                            text = "台南點心"
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, output_message)

    #---------------------------------------------------------------------

        #美食part1
        elif user_message == "台南美食part1":
            output_message = food_carousel_template1()
            line_bot_api.reply_message(event.reply_token, output_message)

    #----------------------------------------------------------------------

        #美食part2
        elif user_message == "台南美食part2":
            output_message = food_carousel_template2()
            line_bot_api.reply_message(event.reply_token, output_message)

    #----------------------------------------------------------------------



            #-------------------------------------------------------------

            #菜單
        elif user_message == f"{food1}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://i.imgur.com/4pw7i8S.jpg",
                preview_image_url = "https://i.imgur.com/4pw7i8S.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food2}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://img.rainieis.tw/uploads/20180211203240_42.jpg",
                preview_image_url = "https://img.rainieis.tw/uploads/20180211203240_42.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food3}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://pic.pimg.tw/tainanlohas/1415102681-4123707573.jpg",
                preview_image_url = "https://pic.pimg.tw/tainanlohas/1415102681-4123707573.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food4}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://fengtaiwanway.com/wp-content/uploads/pixnet/1464808199-26107633.jpg",
                preview_image_url = "https://fengtaiwanway.com/wp-content/uploads/pixnet/1464808199-26107633.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food5}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://pic.pimg.tw/nikitarh/1606665478-1026621535-g_n.jpg",
                preview_image_url = "https://pic.pimg.tw/nikitarh/1606665478-1026621535-g_n.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food6}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://pic.pimg.tw/matsurica/4bf3f7ec949f7.jpg",
                preview_image_url = "https://pic.pimg.tw/matsurica/4bf3f7ec949f7.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food7}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://img.bopomo.tw/20190305233812_61.jpg",
                preview_image_url = "https://img.bopomo.tw/20190305233812_61.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food8}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://images.zi.org.tw/bigfang/2020/09/15165908/1600160347-bf78e344a5b5b63be889d19218eb6be2.jpg",
                preview_image_url = "https://images.zi.org.tw/bigfang/2020/09/15165908/1600160347-bf78e344a5b5b63be889d19218eb6be2.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food9}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://i.imgur.com/I1y3CAm.jpg",
                preview_image_url = "https://i.imgur.com/I1y3CAm.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food10}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://scontent.ftpe10-1.fna.fbcdn.net/v/t1.6435-9/131766081_1751405925021066_2159747408668762709_n.jpg?_nc_cat=106&ccb=1-3&_nc_sid=730e14&_nc_ohc=a5PNNlgVa_0AX8AawrR&tn=DbO66jLhb-cjliWk&_nc_ht=scontent.ftpe10-1.fna&oh=a06711c4688174efe464754ecb19d0e0&oe=60FC98FF",
                preview_image_url = "https://scontent.ftpe10-1.fna.fbcdn.net/v/t1.6435-9/131766081_1751405925021066_2159747408668762709_n.jpg?_nc_cat=106&ccb=1-3&_nc_sid=730e14&_nc_ohc=a5PNNlgVa_0AX8AawrR&tn=DbO66jLhb-cjliWk&_nc_ht=scontent.ftpe10-1.fna&oh=a06711c4688174efe464754ecb19d0e0&oe=60FC98FF"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food11}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://4.bp.blogspot.com/-yOzQNhbI4aQ/XoBuboSpDsI/AAAAAAAAOqs/mi6VjloP1akm49P5Feez3ixOgM02ygXjwCKgBGAsYHg/s1600/IMG_2672.jpg",
                preview_image_url = "https://4.bp.blogspot.com/-yOzQNhbI4aQ/XoBuboSpDsI/AAAAAAAAOqs/mi6VjloP1akm49P5Feez3ixOgM02ygXjwCKgBGAsYHg/s1600/IMG_2672.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food12}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://img.rainieis.tw/uploads/20180212114310_48.jpg",
                preview_image_url = "https://img.rainieis.tw/uploads/20180212114310_48.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food13}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://img.13shaniu.tw/uploads/20190721233842_54.jpeg",
                preview_image_url = "https://img.13shaniu.tw/uploads/20190721233842_54.jpeg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food14}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://sillybaby.tw/wp-content/uploads/20180510115225_38.jpg",
                preview_image_url = "https://sillybaby.tw/wp-content/uploads/20180510115225_38.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food15}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://3.bp.blogspot.com/-lRJyFRbEn2c/W-RrUQ0QUII/AAAAAAAAgqI/bONSCYpIaksmZD6NRrzfRk_NgA0JPn59gCKgBGAs/s1600/IMG_7797.jpg",
                preview_image_url = "https://3.bp.blogspot.com/-lRJyFRbEn2c/W-RrUQ0QUII/AAAAAAAAgqI/bONSCYpIaksmZD6NRrzfRk_NgA0JPn59gCKgBGAs/s1600/IMG_7797.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food16}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://scontent.ftpe10-1.fna.fbcdn.net/v/t1.6435-9/133250809_3597804996939301_1854083568135046080_n.jpg?_nc_cat=102&ccb=1-3&_nc_sid=c4c01c&_nc_ohc=-pQMW5XjPLUAX_MPySk&_nc_ht=scontent.ftpe10-1.fna&oh=62be5f40928f5d3a2fa5a21890236084&oe=60FC7D44",
                preview_image_url = "https://scontent.ftpe10-1.fna.fbcdn.net/v/t1.6435-9/133250809_3597804996939301_1854083568135046080_n.jpg?_nc_cat=102&ccb=1-3&_nc_sid=c4c01c&_nc_ohc=-pQMW5XjPLUAX_MPySk&_nc_ht=scontent.ftpe10-1.fna&oh=62be5f40928f5d3a2fa5a21890236084&oe=60FC7D44"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food17}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://scontent.ftpe10-1.fna.fbcdn.net/v/t1.6435-9/186528711_6049655938385449_4302705472193818662_n.jpg?_nc_cat=100&ccb=1-3&_nc_sid=8bfeb9&_nc_ohc=0gbsHfVco7UAX8DE_mJ&_nc_ht=scontent.ftpe10-1.fna&oh=b45fa57fa1f10cd5200d51a4a94559f3&oe=60FD6060",
                preview_image_url = "https://scontent.ftpe10-1.fna.fbcdn.net/v/t1.6435-9/186528711_6049655938385449_4302705472193818662_n.jpg?_nc_cat=100&ccb=1-3&_nc_sid=8bfeb9&_nc_ohc=0gbsHfVco7UAX8DE_mJ&_nc_ht=scontent.ftpe10-1.fna&oh=b45fa57fa1f10cd5200d51a4a94559f3&oe=60FD6060"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food18}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://lh3.googleusercontent.com/zebMrQBQ5Rp4Fp_jM9eZJ_ZbC011ePVodvu40cp5xEjc7jxzbSrREwYJMEj0330Fq1ITg2Pz-OqtOIlL0CiEDUEOfRCwu3g=s600",
                preview_image_url = "https://lh3.googleusercontent.com/zebMrQBQ5Rp4Fp_jM9eZJ_ZbC011ePVodvu40cp5xEjc7jxzbSrREwYJMEj0330Fq1ITg2Pz-OqtOIlL0CiEDUEOfRCwu3g=s600"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food19}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://img.rainieis.tw/uploads/20180212120801_68.jpg",
                preview_image_url = "https://img.rainieis.tw/uploads/20180212120801_68.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food20}菜單":
            output_message = ImageSendMessage(
                original_content_url = "https://img.rainieis.tw/uploads/20200330234808_8.jpg",
                preview_image_url = "https://img.rainieis.tw/uploads/20200330234808_8.jpg"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

            #-------------------------------------------------------------

            #營業時間
        elif user_message == f"{food1}營業時間":
            output_message = text_reply.text_reply_message(f"{food1}營業時間\n\n星期一：休息\n星期二：休息\n星期三：11:00–17:00\n星期四：11:00–17:00\n星期五：11:00–17:00\n星期六：11:00–17:00\n星期日：11:00–17:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food2}營業時間":
            output_message = text_reply.text_reply_message(f"{food2}營業時間\n\n星期一：08:30–19:30\n星期二：休息\n星期三：08:30–19:30\n星期四：08:30–19:30\n星期五：08:30–19:30\n星期六：08:30–19:30\n星期日：08:30–19:30")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food3}營業時間":
            output_message = text_reply.text_reply_message(f"{food3}營業時間\n\n星期一：08:00–18:00\n星期二：08:00–18:00\n星期三：08:00–18:00\n星期四：休息\n星期五：08:00–18:00\n星期六：08:00–18:00\n星期日：08:00–18:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food4}營業時間":
            output_message = text_reply.text_reply_message(f"{food4}營業時間\n\n星期一：休息\n星期二：10:00–02:00\n星期三：10:00–02:00\n星期四：10:00–02:00\n星期五：10:00–02:00\n星期六：10:00–02:00\n星期日：10:00–00:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food5}營業時間":
            output_message = text_reply.text_reply_message(f"{food5}營業時間\n\n星期一：06:00–21:00\n星期二：06:00–21:00\n星期三：06:00–21:00\n星期四：06:00–21:00\n星期五：06:00–21:00\n星期六：06:00–21:00\n星期日：06:00–21:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food6}營業時間":
            output_message = text_reply.text_reply_message(f"{food6}營業時間\n\n星期一：18:00–04:00\n星期二：18:00–04:00\n星期三：18:00–04:00\n星期四：18:00–04:00\n星期五：18:00–04:00\n星期六：18:00–04:00\n星期日：18:00–04:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food7}營業時間":
            output_message = text_reply.text_reply_message(f"{food7}營業時間\n\n星期一：\n09:30–15:00, 17:00–20:00\n星期二：\n09:30–15:00, 17:00–20:00\n星期三：\n09:30–15:00, 17:00–20:00\n星期四：\n09:30–15:00, 17:00–20:00\n星期五：\n09:30–15:00, 17:00–20:00\n星期六：\n09:30–15:00, 17:00–20:00\n星期日：休息")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food8}營業時間":
            output_message = text_reply.text_reply_message(f"{food8}營業時間\n\n星期一：04:00–14:00\n星期二：04:00–14:00\n星期三：04:00–14:00\n星期四：04:00–14:00\n星期五：04:00–14:00\n星期六：04:00–15:00\n星期日：04:00–15:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food9}營業時間":
            output_message = text_reply.text_reply_message(f"{food9}營業時間\n\n星期一：休息\n星期二：17:00–00:00\n星期三：17:00–00:00\n星期四：17:00–00:00\n星期五：17:00–00:00\n星期六：17:00–00:00\n星期日：17:00–00:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food10}營業時間":
            output_message = text_reply.text_reply_message(f"{food10}營業時間\n\n星期一：10:00–21:30\n星期二：10:00–21:30\n星期三：10:00–21:30\n星期四：10:00–21:30\n星期五：10:00–21:30\n星期六：10:00–21:30\n星期日：10:00–21:30")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food11}營業時間":
            output_message = text_reply.text_reply_message(f"{food11}營業時間\n\n星期一：16:30–01:00\n星期二：16:30–01:00\n星期三：16:30–01:00\n星期四：16:30–01:00\n星期五：16:30–01:30\n星期六：16:30–01:30\n星期日：16:30–01:30")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food12}營業時間":
            output_message = text_reply.text_reply_message(f"{food12}營業時間\n\n星期一：07:00–17:30\n星期二：07:00–17:30\n星期三：07:00–17:30\n星期四：休息\n星期五：07:00–17:30\n星期六：07:00–17:30\n星期日：07:00–17:30")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food13}營業時間":
            output_message = text_reply.text_reply_message(f"{food13}營業時間\n\n星期一：休息\n星期二：06:30–18:30\n星期三：06:30–18:30\n星期四：06:30–18:30\n星期五：06:30–18:30\n星期六：06:30–18:30\n星期日：06:30–18:30")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food14}營業時間":
            output_message = text_reply.text_reply_message(f"{food14}營業時間\n\n星期一：10:30–19:30\n星期二：10:30–19:30\n星期三：10:30–19:30\n星期四：10:30–19:30\n星期五：10:30–19:30\n星期六：10:30–19:30\n星期日：10:30–19:30")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food15}營業時間":
            output_message = text_reply.text_reply_message(f"{food15}營業時間\n\n星期一：07:00–14:30\n星期二：07:00–14:30\n星期三：07:00–14:30\n星期四：休息\n星期五：07:00–14:30\n星期六：07:00–14:30\n星期日：07:00–14:30")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food16}營業時間":
            output_message = text_reply.text_reply_message(f"{food16}營業時間\n\n星期一：07:00–22:00\n星期二：07:00–22:00\n星期三：休息\n星期四：07:00–22:00\n星期五：07:00–22:00\n星期六：07:00–22:00\n星期日：07:00–22:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food17}營業時間":
            output_message = text_reply.text_reply_message(f"{food17}營業時間\n\n星期一：休息\n星期二：休息\n星期三：12:00–18:00\n星期四：12:00–18:00\n星期五：12:00–18:00\n星期六：12:00–18:00\n星期日：12:00–18:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food18}營業時間":
            output_message = text_reply.text_reply_message(f"{food18}營業時間\n\n星期一：17:00–00:00\n星期二：17:00–00:00\n星期三：17:00–00:00\n星期四：17:00–00:00\n星期五：17:00–00:00\n星期六：17:00–00:00\n星期日：17:00–00:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food19}營業時間":
            output_message = text_reply.text_reply_message(f"{food19}營業時間\n\n星期一：11:00–21:00\n星期二：11:00–21:00\n星期三：11:00–21:00\n星期四：11:00–21:00\n星期五：11:00–21:00\n星期六：11:00–21:00\n星期日：11:00–21:00")
            line_bot_api.reply_message(event.reply_token, output_message)

        elif user_message == f"{food20}營業時間":
            output_message = text_reply.text_reply_message(f"{food20}營業時間\n\n星期一：05:00–12:30\n星期二：休息\n星期三：05:00–12:30\n星期四：05:00–12:30\n星期五：05:00–12:30\n星期六：05:00–12:30\n星期日：05:00–12:30")
            line_bot_api.reply_message(event.reply_token, output_message)

            #-------------------------------------------------------------

            #地圖位置
        #1
        elif user_message ==f"可由此打開{food1}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food1}",
                address = "台南市中西區國華街三段5號",
                latitude = "22.99355830555154",
                longitude = "120.197479227042"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #2
        elif user_message ==f"可由此打開{food2}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food2}",
                address = "台南市中西區海安路一段66號",
                latitude = "22.98897454659431",
                longitude = "120.19527211288802"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #3
        elif user_message ==f"可由此打開{food3}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food3}",
                address = "台南市中西區國華街三段181號",
                latitude = "22.99756243319255",
                longitude = "120.19890510920264"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #4
        elif user_message ==f"可由此打開{food4}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food4}",
                address = "708台南市安平區安平路590號",
                latitude = "22.998750218851384",
                longitude = "120.16973447085927"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #5
        elif user_message ==f"可由此打開{food5}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food5}",
                address = "台南市中西區保安路53號",
                latitude = "22.99025382562354",
                longitude = "120.19640750231954"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #6
        elif user_message ==f"可由此打開{food6}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food6}",
                address = "台南市東區勝利路119號",
                latitude = "22.99467882677812",
                longitude = "120.21792580970332"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #7
        elif user_message ==f"可由此打開{food7}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food7}",
                address = "台南市中西區中山路8巷5號",
                latitude = "22.992811497425294",
                longitude = "120.20594536499986"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #8
        elif user_message ==f"可由此打開{food8}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food8}",
                address = "台南市安平區安平路612號",
                latitude = "22.998934777722237",
                longitude = "120.16887777875954"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #9
        elif user_message ==f"可由此打開{food9}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food9}",
                address = "台南市中西區民族路三段89號",
                latitude = "22.998364945021",
                longitude = "120.19696113865045"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #10
        elif user_message ==f"可由此打開{food10}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food10}",
                address = "台南市安平區安平路408-1號",
                latitude = "22.998097253954455",
                longitude = "120.17459910476686"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #11
        elif user_message ==f"可由此打開{food11}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food11}",
                address = "台南市中西區友愛街143號",
                latitude = "22.991519859859444",
                longitude = "120.1991163002723"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #12
        elif user_message ==f"可由此打開{food12}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food12}",
                address = "台南市中西區民族路三段11號",
                latitude = "22.997607846744017",
                longitude = "120.19921193444611"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #13
        elif user_message ==f"可由此打開{food13}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food13}",
                address = "台南市中西區府前路一段215號",
                latitude = "22.989144129134928",
                longitude = "120.2037448190117"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #14
        elif user_message ==f"可由此打開{food14}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food14}",
                address = "台南市中西區大德街38號",
                latitude = "22.989456875210564",
                longitude = "120.19569979202385"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #15
        elif user_message ==f"可由此打開{food15}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food15}",
                address = "台南市中西區民族路三段104號",
                latitude = "22.99888561400458",
                longitude = "120.19721339754601"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #16
        elif user_message ==f"可由此打開{food16}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food16}",
                address = "台南市北區成功路380號",
                latitude = "23.000357785827312",
                longitude = "120.20017912913502"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #17
        elif user_message ==f"可由此打開{food17}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food17}",
                address = "台南市中西區國華街三段22號",
                latitude = "22.99341779274471",
                longitude = "120.19754275895937"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #18
        elif user_message ==f"可由此打開{food18}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food18}",
                address = "台南市中西區保安路72號",
                latitude = "22.990495165451254",
                longitude = "120.19612642519014"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #19
        elif user_message ==f"可由此打開{food19}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food19}",
                address = "台南市中西區中正路康樂市場180號",
                latitude = "22.992374990454337",
                longitude = "120.19615810739693"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #20
        elif user_message ==f"可由此打開{food20}的google地圖位置":
            output_message = LocationSendMessage(
                title = f"{food20}",
                address = "台南市中西區西門路一段728號",
                latitude = "22.98996871769685",
                longitude = "120.19788844000415"
            )
            line_bot_api.reply_message(event.reply_token, output_message)

        #----------------------------------------------------------------------

        #點心
        elif user_message == "台南點心":
            output_message = dessert_carousel_template()
            line_bot_api.reply_message(event.reply_token, output_message)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        elif user_message == "台南飲料":
            output_message = TemplateSendMessage(
            alt_text = "要顯示的字",
                template = ImageCarouselTemplate(
                    colunms = [
                        ImageCarouselColumn(
                            image_url = "",
                            action = URITemplateAction(
                                label = "標題",
                                uri = "網址"
                            )
                        ),
                        ImageCarouselColumn(
                            image_url = "",
                            action = URITemplateAction(
                                label = "標題",
                                uri = "網址"
                            )
                        ),
                        ImageCarouselColumn(
                            image_url = "",
                            action = URITemplateAction(
                                label = "標題",
                                uri = "網址"
                            )
                        ),
                        ImageCarouselColumn(
                            image_url = "",
                            action = URITemplateAction(
                                label = "標題",
                                uri = "網址"
                            )
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, output_message)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
        else:
            output_message = text_reply.text_reply_message("請輸入有效指令！")
            line_bot_api.reply_message(event.reply_token, output_message)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# instruction of pushing code to heroku
# git add .
# git commit -am'ok'
# git push heroku master

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)