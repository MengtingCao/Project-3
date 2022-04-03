from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from .GroupMeAPI import groupmeapi as grme
from datetime import datetime
import json, requests

g = grme()

#GLOBAL USER VAR
groupid = 0
redirectURL = "https://oauth.groupme.com/oauth/authorize?client_id=HJomQxYT0hNMcBmzCzMyFHjKby4jxjo3Fgl5ptINs4BgOqqo"


def messages(request):
    global accesstoken
    accesstoken = request.GET.get('access_token')
    listOfChats = g.listChats(accesstoken)
    convos = json.loads(listOfChats)
    conversations = []

    for chat in convos['response']:
        data = {}
        data['name'] = chat['name']
        data['platform'] = 'GroupMe'
        data['snippet'] = chat['messages']['preview']['text']
        data['time'] = datetime.fromtimestamp(chat['messages']['last_message_created_at'])
        print(data)
        conversations.append(data)
    
    context = {
        'title': 'Messages',
        'conversations': reversed(sorted(conversations, key = lambda i: (i['time'], i['name'])))
    }
    return render(request, 'messages.html', context)

def groupMe_login(request: HttpRequest):
    return redirect(redirectURL)

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