import slack
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
env_path=Path('.') / '.env'
app= Flask(__name__)
load_dotenv()
slack_event_adapter=SlackEventAdapter(os.environ['SIGNING_SECRETE'],'/slack/events', app)
client=slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID=client.api_call("auth.test")['user_id']
welcome_message={}

class welcomemessage:

    START_TEXT= {
        'type':'section',
        'text': {
            'type': 'mrkdwn',
            'text':(
                "Hey there! I am here to help you resolve your queries \n"
                "Please Type 'Hello chatbot' into devops-chatsupport group to get started "
            )
        }
    }

    DIVIDER= {'type':'divider'}
    def __init__(self,channel,user):
        self.channel=channel
        self.user=user
        self.icon_emoji=':robot_face:'
        self.timestamp= ''
    
    def get_message(self):
        return {
            'ts': self.timestamp,
            'channel':self.channel,
            'username':'welcome robot!',
            'icon_emoji': self.icon_emoji,
            'blocks':[
                self.START_TEXT,
                self.DIVIDER
            ]
        }
def send_welcome_message(channel,user):
    welcome=welcomemessage(channel,user)
    message=welcome.get_message()
    response=client.chat_postMessage(**message)

@slack_event_adapter.on('message')
def message(payLoad):
    event=payLoad.get('event',{})
    channel_id=event.get('channel')
    user_id=event.get('user')
    text=event.get('text')
    if text.lower() == 'start':
        send_welcome_message(f'@{user_id}',user_id)
    if text.lower() =='hello chatbot':
        client.chat_postMessage(channel=channel_id,text="Hello, welcome to DevOps support kindly type ' chatbot-support' to see all the available option")
    if text.lower()=='chatbot-support':
        START_TEXT1={
            'type': 'section',
            'text':{
                'type':'mrkdwn',
                'text':(
                    "1) Db Issue\n"
                    "2) Credentials \n"
                    "3) Server Restart \n"
                    "4) Jenkins Pipeline"

                )
            }
        }
        timestamp=event.get('ts')
        message={
            'ts':timestamp,
            'channel':channel_id,
            'blocks':[
                START_TEXT1
            ]
        }
        client.chat_postMessage(channel=channel_id,text="Kindly select from the below option and type that key word \n")
        client.chat_postMessage(**message)
    if text.lower() == 'db issue':
        START_TEXT={
            'type': 'section',
            'text':{
                'type':'mrkdwn',
                'text':(
                    
                    "1) Provide DB Dump \n"
                    "2) Other DB Issue "
                )
            }
        }
        timestamp=event.get('ts')
        message={
            'ts':timestamp,
            'channel':channel_id,
            'blocks':[
                START_TEXT 
            ]
        }
        client.chat_postMessage(channel=channel_id,text="Kindly select from below option and Enter that Option")
        client.chat_postMessage(**message)
    if text.lower() =='provide db dump':
        client.chat_postMessage(channel=channel_id,text="This will be done on your own, DevOps team will only provide credentials.")
    if text.lower()== 'other db issue':
        client.chat_postMessage(channel=channel_id,text="Kindly contact DevOps team for other DB Related issues.")
    if text.lower() =='credentials':
        START_TEXT={
            'type': 'section',
            'text':{
                'type':'mrkdwn',
                'text':(
                    
                    "1) Create Credentials For Environment \n"
                    "2) Provide Credentials \n "
                )
            }
        }
        timestamp=event.get('ts')
        message={
            'ts':timestamp,
            'channel':channel_id,
            'blocks':[
                START_TEXT 
            ]
        }
        client.chat_postMessage(channel=channel_id,text="Kindly select from below option and Enter the option")
        client.chat_postMessage(**message)
    if text.lower()=='create credentials for environment':
        client.chat_postMessage(channel=channel_id,text="Ask the TLs, else TLs will have to explain there requirements by sending a mail to DevOps Team.")
    if text.lower() =='provide credentials':
        client.chat_postMessage(channel=channel_id,text="Credentials will be provided by TLs.If TL don't have then TL will have to ask for the credentials from DevOps team through mail.")
    if text.lower() =='server restart':
        client.chat_postMessage(channel=channel_id,text="Will be done by DevOps team kindly Provide server details.")
    if text.lower()=='jenkins pipeline':
        START_TEXT={
            'type': 'section',
            'text':{
                'type':'mrkdwn',
                'text':(
                    
                    "1) Run Jenkins Pipeline  \n"
                    "2) Other Jenkins Issue \n "
                )
            }
        }
        timestamp=event.get('ts')
        message={
            'ts':timestamp,
            'channel':channel_id,
            'blocks':[
                START_TEXT 
            ]
        }
        client.chat_postMessage(channel=channel_id,text="Kindly select from below option and Enter that option")
        client.chat_postMessage(**message)
    if text.lower() == 'run jenkins pipeline':
        client.chat_postMessage(channel=channel_id,text="Pipeline will be run by TLs.")
    if text.lower() == 'other jenkins issue':
        client.chat_postMessage(channel=channel_id,text="Kindly contact DevOps team for other jenkins related issues.")
if __name__=="__main__":
    app.run(host="0.0.0",port=8080)
