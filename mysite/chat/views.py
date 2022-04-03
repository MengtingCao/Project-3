from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from .GroupMeAPI import groupmeapi as grme
from datetime import datetime
import json, requests

g = grme()

#GLOBAL USER VAR
groupid = 1
redirectURL = "https://oauth.groupme.com/oauth/authorize?client_id=HJomQxYT0hNMcBmzCzMyFHjKby4jxjo3Fgl5ptINs4BgOqqo"


def messages(request):
    print(accesstoken)
    convos = json.loads(g.listChats(accesstoken))
    data = {}
    conversations = []

    for chat in convos['response']:
        lastmsg = json.loads(g.getLastMessageG(convos['group_id'] , accesstoken))['response']
        data['name'] = convos['name']
        data['platform'] = 'GroupMe'
        data['snippet'] = lastmsg['text']
        data['time'] = datetime.fromtimestamp(lastmsg['messages']['last_message_created_at'])
    
    context = {
        'title': 'Messages',
        'conversations': sorted(conversations, key = lambda i: (i['date'], i['user']))
    }
    return render(request, 'messages.html', context)

def groupMe_login(request: HttpRequest):
    return redirect(redirectURL)

def groupMe_login_redirect(request:  HttpRequest):
    global accesstoken
    accesstoken = request.GET.get('access_token')
    return render(request, 'redirect.html')

def index(request):
    gc = json.loads(g.getGroupName(groupid , accesstoken))['response']

    msgs = json.loads(g.getMessagesG(groupid , accesstoken))['response']

    for msg in msgs['messages']:
        msg['created_at'] = datetime.fromtimestamp(msg['created_at'])

    return render(request, 'chat.html', {'msgs':msgs['messages'],'gc':gc})

#constantly requests
def update(request):
    gc = json.loads(g.getGroupName(groupid , accesstoken))['response']

    msgs = json.loads(g.getMessagesG(groupid , accesstoken))['response']

    for msg in msgs['messages']:
       msg['created_at'] = datetime.fromtimestamp(msg['created_at'])

    return JsonResponse(msgs)

#sends message
def send(request):

    text = request.POST['text']

    g.sendMessageG(text, groupid,accesstoken)

    return None
   