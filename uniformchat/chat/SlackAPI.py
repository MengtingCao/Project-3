import os
import pathlib
import slack_sdk

oauthKey = "xoxp-3374157642694-3380818343395-3399215698614-ba9d9a96775c27582bc8d9f37a2cbbf8"
#client.chat_postMessage(channel = 'general', text="Hellow World!")

class slackapi:
    def get_messages_slack(self,channelID):
        headers = {
            'Authorization' : oauthKey
        }
        client = slack_sdk.WebClient(oauthKey)
        result = client.conversations_history(channel= channelID)
        conversation_history = []
        conversation_history = result["messages"]
        return conversation_history

    def send_message_slack(self, textToSend, channelID):
        headers = {
            'Authorization' : oauthKey
        }
        client = slack_sdk.WebClient(oauthKey)
        client.chat_postMessage(channel = channelID, text=textToSend)

    def get_channel_slack(self, name):
        headers = {
            'Authorization' : oauthKey
        }
        client = slack_sdk.WebClient(oauthKey)
        for result in client.conversations_list():
            for channel in result["channels"]:
                if channel["name"] == name:
                    conversation_id = channel["id"]
                    return conversation_id
        