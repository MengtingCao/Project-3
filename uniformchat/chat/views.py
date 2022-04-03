from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from .GroupMeAPI import groupmeapi as grme
from datetime import datetime, date, time
import json, requests

g = grme()

#GLOBAL USER VAR
redirectURL = "https://oauth.groupme.com/oauth/authorize?client_id=HJomQxYT0hNMcBmzCzMyFHjKby4jxjo3Fgl5ptINs4BgOqqo"
groupid = 1


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
        snippet = chat['messages']['preview']['text']
        if(len(snippet) > 50):
            snippet = snippet[:50] + "..."
        data['snippet'] = snippet
        data['date'] = date.fromtimestamp(chat['messages']['last_message_created_at']),
        data['datetime'] = datetime.fromtimestamp(chat['messages']['last_message_created_at']),
        dateTime = data['datetime']
        if(data['date'][0] == date.today()):
            data['usedate'] = dateTime[0].strftime('%I:%M %p')
        else:
            data['usedate'] = dateTime[0].strftime("%d/%m/%Y")
        conversations.append(data)
    
    if (groupid != 1):
        gc = json.loads(g.getGroupName(groupid , accesstoken))['response']
        msgs = json.loads(g.getMessagesG(groupid , accesstoken))['response']

        for msg in msgs['messages']:
            msg['created_at'] = datetime.fromtimestamp(msg['created_at'])

        context = {
            'title': 'Messages',
            'msgs':msgs['messages'],
            'gc':gc,
            'conversations': reversed(sorted(conversations, key = lambda i: (i['datetime'], i['name'])))
        }
    else:
        context = {
            'title': 'Messages',

            'conversations': reversed(sorted(conversations, key = lambda i: (i['datetime'], i['name'])))
        }

    return render(request, 'messages.html', context)

def updateM(request):
    listOfChats = g.listChats(accesstoken)
    convos = json.loads(listOfChats)

    for chat in convos['response']:
        chat['platform'] = 'GroupMe'
        chat['snippet'] = chat['messages']['preview']['text']
        time = datetime.fromtimestamp(chat['messages']['last_message_created_at'])
        chat['time'] = time.strftime("%b %d, %Y | %I:%M %P")
        
    return JsonResponse(convos)


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
    msgs['name']= gc['name']
    for msg in msgs['messages']:
        time = datetime.fromtimestamp(msg['created_at'])
        msg['created_at'] = time.strftime("%b %d, %Y | %I:%M %P")

    return JsonResponse(msgs)

#sends message
def send(request):

    text = request.POST['text']

    g.sendMessageG(text, groupid,accesstoken)

    return None


#update gm id
def updategmID(request):

    global groupid
    groupid = request.POST['text']

    return None