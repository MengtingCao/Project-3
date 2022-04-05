import os
from GroupMeAPI import groupmeapi as grme
from datetime import datetime
import json
from . import views

g = grme()

accesstoken = views.accesstoken

chats = json.loads(g.listChats(accesstoken))
for chat in chats['response']:
    print("--------------------------------")
    print(chat['name'], "  //---ID: ",chat['id'])
    print(datetime.fromtimestamp(chat['messages']['last_message_created_at']))

groupid = input("Input Group ID: ")

#for linux use 'clear'
#for windows use 'cls'
os.system('clear')

def showMessages():
    msgs = json.loads(g.getMessagesG(groupid , accesstoken))['response']

    for msg in reversed(msgs['messages']):
        print("--------------------------------")
        print(datetime.fromtimestamp(msg['created_at'])," | " ,msg['name'],": ",msg['text'])


 

showMessages()

smsg = input("")
while(smsg != "q"):
    os.system('clear')
    g.sendMessageG(smsg, groupid,accesstoken)
    showMessages()
    smsg = input("")

