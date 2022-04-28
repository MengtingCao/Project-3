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
<<<<<<< HEAD
    def listChats_GroupMe(self,token):
=======
    def listChats(self,token):
>>>>>>> 0b32c798ed5f04ef51961df9bf9d5e72287516b6
        params = (
            ('per_page', 100),
        )
        response = requests.get(gbaseurl + '?token=' + str(token), params=params, verify=False)

        return response.content
    
<<<<<<< HEAD
    def listGroups_GroupMe(self,token):
=======
    def listGroups(self,token):
>>>>>>> 0b32c798ed5f04ef51961df9bf9d5e72287516b6
        params = (
            ('per_page', 100),
        )
        response = requests.get(gbaseurl + '?token=' + str(token), params=params, verify=False)

        return response.content

<<<<<<< HEAD
    def sendMessage_GroupMe(self, message, group, token):
=======
    def sendMessageG(self, message, group, token):
>>>>>>> 0b32c798ed5f04ef51961df9bf9d5e72287516b6
        headers = {
            'Host': 'api.groupme.com',
            'X-Access-Token': token,
            'Content-Type': 'application/json',
        }
        data = '{"message":{"source_guid":"'+self.randomString(25)+'","attachments":[],"text":"'+message+'"}}'

        response = requests.post(gbaseurl+'/'+str(group)+'/messages', headers=headers, data=data, verify=False)

        return response.content
    
<<<<<<< HEAD
    def getMessages_GroupMe(self, group, token):
=======
    def getMessagesG(self, group, token):
>>>>>>> 0b32c798ed5f04ef51961df9bf9d5e72287516b6
        params = (
            ('limit', 100),
        )
        response = requests.get(gbaseurl+'/'+str(group)+'/messages?token=' + str(token), params=params, verify=False)

        return(response.content)

<<<<<<< HEAD
    def getLastMessage_GroupMe(self, group, token):
=======
    def getLastMessageG(self, group, token):
>>>>>>> 0b32c798ed5f04ef51961df9bf9d5e72287516b6
        params = (
            ('limit', 100),
        )
        response = requests.get(gbaseurl+'/'+str(group)+'/messages?token=' + str(token), params=params, verify=False)

        return(response.content)

<<<<<<< HEAD
    def getGroupName_GroupMe(self, group, token):
=======
    def getGroupName(self, group, token):
>>>>>>> 0b32c798ed5f04ef51961df9bf9d5e72287516b6
        response = requests.get(gbaseurl+'/'+str(group)+'?token=' + str(token), verify=False)

        return(response.content)
