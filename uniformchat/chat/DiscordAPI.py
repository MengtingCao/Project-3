from urllib import response
import requests
import json
import asyncio


API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '963435798294847488'
CLIENT_SECRET = 'Mg4wT50ZRzw4iqHqMLutrioK14NLClkS'
REDIRECT_URI = 'http://localhost:8000/chat/discordauth/'

bot_key= "Bot OTYzNDM1Nzk4Mjk0ODQ3NDg4.YlWDgg.nClAStmvmlmgCDVMSfQBqHqEO8s"

class discordapi:
    def getMessages_Discord(self,channelID):
        headers = {
            'Authorization': bot_key,
            'Content-Type': 'application/json'
        }
        params = (
            ('limit', 100),
        )
        response = requests.get('https://discordapp.com/api/channels/'+str(channelID)+'/messages' , params=params,headers=headers,verify=False)
        return(response.content)


    def exchange_code(self, code):
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('https://discord.com/api/v8/oauth2/token', data=data, headers=headers)
        return r.content

    def refresh_token(refresh_token):
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('https://discord.com/api/v8/oauth2/token', data=data, headers=headers)
        return r.json()

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
    def get_channel(self, channelid):
        headers = {
            'authorization' : bot_key
        }
        r = requests.get(f'https://discord.com/api/v9/channels/{channelid}', headers=headers)
        return r.content

    