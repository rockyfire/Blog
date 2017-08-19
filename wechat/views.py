from django.shortcuts import render

from django.http import HttpResponse
from hashlib import sha1

from lxml import etree
from django.utils.encoding import smart_str





# Create your views here.
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

        return HttpResponse(echostr)
    if request.method == 'POST':
        data = smart_str(request.body)
        xml = etree.fromstring(data)
        response_xml = main_handle(xml)
        return HttpResponse(response_xml)

def main_handle(xml):
    return 'success'