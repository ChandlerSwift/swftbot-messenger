#!/usr/bin/python3

from fbchat import Client
from fbchat.models import *
import datetime
import xkcd
import wikipedia

# Don't include trailing spaces
# Haha you thought I was going to include these in plaintext? asd
facebook_username = open("facebook-username.txt", "r").read()
facebook_password = open("facebook-password.txt", "r").read()

sections = []
num_sections = 0

class SwftBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # Check for blank (picture, for one) messages
        if message_object.text == None:
            return

        if message_object.text.startswith('@swftbot time'):
            time_remaining = datetime.datetime(2018, 6, 6, 13, 54) - datetime.datetime.now()
            self.send(Message(text="About {} days, {} hours, and {} minutes left!".format(time_remaining.days, time_remaining.seconds // 3600, time_remaining.seconds % 3600 // 60)), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot hours'):
            time_remaining = datetime.datetime(2018, 6, 6, 13, 54) - datetime.datetime.now()
            self.send(Message(text="About {} hours and {} minutes left!".format(int(time_remaining.total_seconds() // 3600), time_remaining.seconds % 3600 // 60)), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot hello'):
            self.send(Message(text='Hello World!'), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot insult'):
            insultee = message_object.text[16:]
            if insultee.startswith("Cha") or insultee.startswith("cha"):
                self.send(Message("Chandler is great! Can't insult him... :D"), thread_id=thread_id, thread_type=thread_type)
            else:
                self.send(Message(text=insultee + " smells funny!"), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot xkcd'):
            xkcd_command = message_object.text[14:]
            xkcd_comic = None
            if xkcd_command == "help":
                self.send(Message("Usage: @swftbot xkcd <1234|random|latest|help>"), thread_id=thread_id, thread_type=thread_type)
                return
            elif xkcd_command == "random":
                xkcd_comic = xkcd.getRandomComic()
            elif xkcd_command == "latest":
                xkcd_comic = xkcd.getLatestComic()
            else:
                try:
                    xkcd_number=int(xkcd_command)
                except:
                    msg_text="Error parsing command."
                    self.send(Message(text=msg_text), thread_id=thread_id, thread_type=thread_type)
                    return
                xkcd_comic=xkcd.Comic(xkcd_number)
            self.sendRemoteImage(xkcd_comic.getImageLink(), message=Message(text=xkcd_comic.getAltText()), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot wikipedia'):
          global sections
          global num_sections
          try:
            query = message_object.text[19:]
            if query == "next":
                if len(sections) > 0:
                  self.send(Message(sections.pop(0)), thread_id=thread_id, thread_type=thread_type)
                  self.send(Message("Section %i of %i" % (num_sections - len(sections), num_sections)), thread_id=thread_id, thread_type=thread_type)
                else:
                  print('No more sections!')
            else:
                current_page = wikipedia.WikipediaPage(query)
                if current_page is None:
                  print("No page found")
                else:
                  sections = current_page.content.split("\n\n\n")
                  num_sections = len(sections)
                  self.send(Message(sections.pop(0)), thread_id=thread_id, thread_type=thread_type)
                  self.send(Message("Section %i of %i" % (num_sections - len(sections), num_sections)), thread_id=thread_id, thread_type=thread_type)
          except:
            self.send(Message("Wikipedia Error"), thread_id=thread_id, thread_type=thread_type)
        elif message_object.text.startswith('@swftbot'):
            msg_text = ("swftbot usage:\n"
                    "@swftbot hello: displays \"Hello World!\"\n"
                    "@swftbot insult <name>: Sends an insult to <name>\n"
                    "@swftbot xkcd <1234|random|latest|help>: Adds an XKCD to the chat"
                    "@swftbot help: displays this help text")
            self.send(Message(text=msg_text), thread_id=thread_id, thread_type=thread_type)

client = SwftBot(facebook_username, facebook_password)
client.listen()
