from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
import requests
import vk


def index(request):
    access_token = request.COOKIES.get('access_token', None)
    if not access_token:
        return auth(request)

    vk_api = vk.API(vk.Session(access_token=access_token))

    friends = vk_api.friends.get(count=5, fields='nickname', v=5.80).get('items')
    user = vk_api.users.get(v=5.80)[0]

    return render(request, 'interview/index.html', {'friends': friends, 'user': user})


def auth(request):
    url = 'https://oauth.vk.com/authorize?' + \
          'client_id=' + settings.VK_CLIENT_ID + \
          '&display=page' + \
          '&scope=friends' + \
          '&redirect_uri=' + settings.SITE_URL + '/code'
    return render(request, 'interview/auth.html', {'url': url})


def code(request):
    url = 'https://oauth.vk.com/access_token?' + \
          'client_id=' + settings.VK_CLIENT_ID + \
          '&client_secret=' + settings.VK_CLIENT_SECRET + \
          '&code=' + request.GET.get('code') + \
          '&redirect_uri=' + settings.SITE_URL + '/code'
    response = requests.get(url)
    data = response.json()
    if 'access_token' not in data:
        return HttpResponse('An error happened <br> %s <br> %s' % (url, response.content))

    http_response = HttpResponseRedirect('/')
    http_response.set_cookie('access_token', data['access_token'], data['expires_in'])
    return http_response


def token(request):
    return HttpResponse(
        "<pre>Request: %s\nRequest.GET: %s\nRequest.GET.keys: %s" % (dir(request), request.GET, request.GET.keys()))
