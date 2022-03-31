import requests
import string
import random
import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class groupmeapi:

    def randomString(self, stringLength):
        letters = string.ascii_lowercase + "1234567890"
        return ''.join(random.choice(letters) for i in range(stringLength))

    #api to get chat data
    def listChats(self,token):
        params = (
            ('per_page', 100),
        )
        response = requests.get('https://api.groupme.com/v3/groups?token=' + str(token), params=params, verify=False)

        return response.content

    def sendMessageG(self, message, group, token):
        headers = {
            'Host': 'api.groupme.com',
            'X-Access-Token': token,
            'Content-Type': 'application/json',
        }
        data = '{"message":{"source_guid":"'+self.randomString(25)+'","attachments":[],"text":"'+message+'"}}'

        response = requests.post('https://api.groupme.com/v3/groups/'+str(group)+'/messages', headers=headers, data=data, verify=False)

        return response.content
    
    def getMessagesG(self, group, token):
        params = (
            ('limit', 100),
        )
        response = requests.get('https://api.groupme.com/v3/groups/'+str(group)+'/messages?token=' + str(token), params=params, verify=False)

        return(response.content)
