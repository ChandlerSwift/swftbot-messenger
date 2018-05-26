#!/usr/bin/python3

from fbchat import Client
from fbchat.models import *

# Don't include trailing spaces
# Haha you thought I was going to include these in plaintext? asd
file = open("facebook-username.txt", "r") 
facebook_username = file.read()
file = open("facebook-password.txt", "r")
facebook_password = file.read()

class SwftBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        if message_object.text.startswith('@swftbot time'):
            self.send(Message(text='4eva'), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot hello'):
            self.send(Message(text='Hello World!'), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot'):
            msg_text = ("swftbot usage:\n"
                    "@swftbot hello: displays \"Hello World!\"\n"
                    "@swftbot help: displays this help text")
            self.send(Message(text=msg_text), thread_id=thread_id, thread_type=thread_type)

client = SwftBot(facebook_username, facebook_password)
client.listen()