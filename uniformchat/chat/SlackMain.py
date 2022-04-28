import os
from SlackAPI import slackapi as sapi
from datetime import datetime
import json

s = sapi

def show_messages():
    conversation_history = []
    conversation_history = s.get_messages_slack(channelID= "C03B94K7SBE")
    for value in conversation_history:
        print(value['ts'], value['user'], " : ", value['text'], '\n')
def send_messages():
    text = "gsgsgs"
    s.send_message_slack(textToSend=text, channelID= "C03BCMJLUJ3")

print(s.get_channel_slack("app"))

send_messages()

print(s.get_channel_slack("general"))
