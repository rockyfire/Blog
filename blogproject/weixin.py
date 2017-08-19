from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from hashlib import sha1





def weixin(request):
    signature=request.GET.get('signature','')
    timestamp=request.GET.get('timestamp','')
    nonce=request.GET.get('nonce','')
    echostr=request.GET.get('echostr','')
    token='rockyfire'
    raw=''.join(sorted([token,timestamp,nonce])).encode('utf8')
    key=sha1(raw).hexdigest()
    if key.upper() !=signature.upper():
        echostr=''
    return HttpResponse(echostr)






