import os
from DiscordAPI import discordapi as dapi
from datetime import datetime
import json

d = dapi()

access_token = input("Input your access token")
channel_id = input("Input Channel ID")

def get_name():
    channels = json.loads(d.get_channel(channel_id, access_token))
    print(channels['name'])

get_name()


def show_messages():
    msgs = json.loads(d.retrieve_messages(channel_id, access_token))
    for value in msgs:
        print(value['timestamp'], " | ", value['author']['username'],": ", value['content'], '\n')

show_messages()

send_message = input("")
while (send_message != "q") :
    os.system('clear')
    d.send_messages(send_message, channel_id, access_token)
    show_messages()
    send_message = input("")