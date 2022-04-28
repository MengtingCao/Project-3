import requests
import string
import random
import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class groupmeapi:
    global gbaseurl
    gbaseurl = 'https://api.groupme.com/v3/groups'

    def randomString(self, stringLength):
        letters = string.ascii_lowercase + "1234567890"
        return ''.join(random.choice(letters) for i in range(stringLength))

    #api to get chat data
    def listChats_GroupMe(self,token):
        params = (
            ('per_page', 100),
        )
        response = requests.get(gbaseurl + '?token=' + str(token), params=params, verify=False)

        return response.content
    
    def listGroups_GroupMe(self,token):
        params = (
            ('per_page', 100),
        )
        response = requests.get(gbaseurl + '?token=' + str(token), params=params, verify=False)

        return response.content

    def sendMessage_GroupMe(self, message, group, token):
        headers = {
            'Host': 'api.groupme.com',
            'X-Access-Token': token,
            'Content-Type': 'application/json',
        }
        data = '{"message":{"source_guid":"'+self.randomString(25)+'","attachments":[],"text":"'+message+'"}}'

        response = requests.post(gbaseurl+'/'+str(group)+'/messages', headers=headers, data=data, verify=False)

        return response.content
    
    def getMessages_GroupMe(self, group, token):
        params = (
            ('limit', 100),
        )
        response = requests.get(gbaseurl+'/'+str(group)+'/messages?token=' + str(token), params=params, verify=False)

        return(response.content)

    def getLastMessage_GroupMe(self, group, token):
        params = (
            ('limit', 100),
        )
        response = requests.get(gbaseurl+'/'+str(group)+'/messages?token=' + str(token), params=params, verify=False)

        return(response.content)

    def getGroupName_GroupMe(self, group, token):
        response = requests.get(gbaseurl+'/'+str(group)+'?token=' + str(token), verify=False)

        return(response.content)
