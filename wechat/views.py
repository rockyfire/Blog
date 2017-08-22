from django.shortcuts import render

from django.http import HttpResponse
from hashlib import sha1
from lxml import etree
from django.utils.encoding import smart_str
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

import time
import logging

global last_time
last_time = 1


# Create your views here.
#logging.basicConfig(filename='logger.log',level=logging.DEBUG)
logger=logging.getLogger("wechat")
@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        signature = request.GET.get('signature','')
        timestamp = request.GET.get('timestamp','')
        nonce = request.GET.get('nonce','')
        echostr = request.GET.get('echostr','')

        token = 'rockyfire'

        raw = ''.join(sorted([token,timestamp,nonce])).encode('utf8')
        key = sha1(raw).hexdigest()

        if key.upper() != signature.upper():
            echostr = 'failure'
            logger.info('Get test')
            logger.debug("---------------")
        return HttpResponse(echostr)
    else:
        data = smart_str(request.body)
        xml = etree.fromstring(data)

        logger.info(str(xml))

        response_xml = main_handle(xml)
        return HttpResponse(response_xml)

def main_handle(xml):
    global  last_time

    # Event 事件类型，subscribe(订阅)、unsubscribe(取消订阅)
    try:
        event=xml.find('Event').text
    except:
        event='noting'

    try:
        msg_type=xml.find('MsgType').text
        msg_content=xml.find('Content').text
    except:
        msg_type=''
        msg_content=''

    print ('*************')
    print (msg_type,msg_content)

    if event == 'subscribe':
        text = '欢迎关注公众号'
        return parser_text(xml,text)

    if msg_type == 'text':
        if msg_content == 'hello':
            text = 'world'
            return parser_text(xml,text)
        else:
            return 'success'

    return 'success'




def parser_text(xml,text):
    '''
        待处理的文本数据 转为xml发送给微信服务器
    '''

    print ("--------------------------")
    print (text)

    # 反转
    fromUser = xml.find('ToUserName').text
    toUser = xml.find('FromUserName').text

    # 关于重试的消息排重，推荐使用msgid排重。 用户发给微信服务器的消息每一个都有MsgId防止重发

    try:
        message_id=xml.find('MsgId').text
    except:
        message_id=''

    # 时间戳
    nowtime=str(int(time.time()))

    context={
        'FromUserName':fromUser,
        'ToUserName':toUser,
        'Content':text,
        'time':nowtime,
        'id':message_id,
    }

    return render_to_string('wechat/format.xml',context=context)









