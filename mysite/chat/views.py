from django.shortcuts import render
from django.http import HttpResponse
from .GroupMeAPI import groupmeapi as grme
from datetime import datetime
import json
from django.shortcuts import redirect
from django.http import JsonResponse



g = grme()

#GLOBAL USER VAR
#accesstoken = 
#groupid =


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
   