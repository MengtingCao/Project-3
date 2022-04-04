import requests
import json

#https://discord.com/api/v9/channels/767886713586319423/messages?limit=50
#'MTMxMjU2NzE4Mzc3MDkxMDcy.YMJoqw.bCrcoGt3rSGy84-IVgJE3TG14d8'
class discordapi:

    #retrieve messages
    def retrieve_messages(self, channelid, authorization):
        headers = {
            'authorization': authorization
        }
        r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)
        return r.content
    
    #send messages
    def send_messages(self, send_message, channelid, authorization):
        headers = {
            'authorization' : authorization
        }
        send = {
            'content' : send_message
        }
        r = requests.post(f'https://discord.com/api/v9/channels/{channelid}/messages', data=send, headers=headers)
        return r.content

    #get channel name
    def get_channel(self, channelid, authorization):
        headers = {
            'authorization' : authorization
        }
        r = requests.get(f'https://discord.com/api/v9/channels/{channelid}', headers=headers)
        return r.content


    