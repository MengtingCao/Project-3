from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from .GroupMeAPI import groupmeapi as grme
from datetime import datetime, date, time
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import json, requests

g = grme()

#GLOBAL USER VAR
redirectURL = "https://oauth.groupme.com/oauth/authorize?client_id=iUNSRzS3IDBTAIEy5BSg9in8goZVVXto5i762YjI9dtXSiDb"
redirectBack = "http://localhost:8000/chat/messages"
groupid = 1

#global var to know what accounts user has connected 
groupme_conn = False
discord_conn = False
slack_conn = False

def messages(request):
    #reading key file
    keydata = open('chat/keys.txt', 'r') 
    while True:
        line = keydata.readline()
        if not line:
            break
        elif "groupme" in line:
            print(" TRUE ") 
            global groupme_conn
            groupme_conn = True
            global groupme_at
            groupme_at = (line.split(':')[1]).strip()
        elif "discord" in line:
            global discord_conn
            discord_conn = True
            global discord_at
            discord_at = line.split(':')[1]   
    keydata.close()

    #if groupme
    if groupme_conn:
        listOfChats = g.listChats(groupme_at)
        convos = json.loads(listOfChats)['response']
        conversations = []

        for chat in convos:
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
            gc = json.loads(g.getGroupName(groupid , groupme_at))['response']
            msgs = json.loads(g.getMessagesG(groupid , groupme_at))['response']

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
    listOfChats = g.listChats(groupme_at)
    convos = json.loads(listOfChats)

    for chat in convos['response']:
        chat['platform'] = 'GroupMe'
        chat['snippet'] = chat['messages']['preview']['text']
        time = datetime.fromtimestamp(chat['messages']['last_message_created_at'])
        chat['time'] = time.strftime("%b %d, %Y | %I:%M %P")
        
    return JsonResponse(convos)


def groupMe_login(request: HttpRequest):
    return redirect(redirectURL)

def groupMe_auth(request: HttpRequest):
    text_file = open("chat/keys.txt", "at")
    text_file.write("groupme:" + request.GET.get('access_token') + "\n")
    text_file.close()

    return redirect(redirectBack)



def index(request):
    gc = json.loads(g.getGroupName(groupid , groupme_at))['response']

    msgs = json.loads(g.getMessagesG(groupid , groupme_at))['response']

    for msg in msgs['messages']:
        msg['created_at'] = datetime.fromtimestamp(msg['created_at'])

    return render(request, 'chat.html', {'msgs':msgs['messages'],'gc':gc})

#constantly requests
def update(request):
    if (groupid != 1):
        gc = json.loads(g.getGroupName(groupid , groupme_at))['response']

        msgs = json.loads(g.getMessagesG(groupid , groupme_at))['response']
        msgs['name']= gc['name']
        for msg in msgs['messages']:
            time = datetime.fromtimestamp(msg['created_at'])
            msg['created_at'] = time.strftime("%b %d, %Y | %I:%M %P")

        return JsonResponse(msgs)
    else:
        return HttpResponse(status=204)

#sends message
def send(request):

    text = request.POST['text']

    g.sendMessageG(text, groupid,groupme_at)

    return HttpResponse(status=204)


#update gm id
def updategmID(request):

    global groupid
    groupid = request.POST['text']

    return None

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})
