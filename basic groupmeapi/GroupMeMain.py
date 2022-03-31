import os
from GroupMeAPI import groupmeapi as grme
from datetime import datetime
import json

g = grme()

print("https://oauth.groupme.com/oauth/authorize?client_id=9CGnISIh98iHAwy8hyTeOnAjLmeLZ32BVV5ovf6LG5nM3JPB")
accesstoken = input("Input Access Token: ")

chats = json.loads(g.listChats(accesstoken))
for chat in chats['response']:
    print("--------------------------------")
    print(chat['name'], "  //---ID: ",chat['group_id'])
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

