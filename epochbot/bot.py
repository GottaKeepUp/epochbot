import json
import re
import sys
import time

from epochbot.db.db import db
from epochbot.irc import irc

CONFIG_FILE = '../config.json'
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)


def ircMessagesCallback(chatIRC, line):
    if re.search('PING :tmi.twitch.tv', line):
        chatIRC.pong()

    cmdRegex = r'^:(\b\w+)!\1@\1.tmi.twitch.tv PRIVMSG #(\b\w+) :!(\w*)\s?(.*)'
    # word starting with 't' then another word
    regex = re.compile(cmdRegex)
    match = regex.search(line)
    if match:
        print match.group(1), match.group(2), match.group(3), match.group(4)
        userMessageHandler(match.group(1), match.group(2), match.group(3), match.group(4))


def userMessageHandler(channel, viewer, cmd, value):
    cmd = cmd.lower()

    if channel == config['twitch']['username']:  # command in the bot channel
        if cmd == 'init':
            if db.initChannel(channel):
                irc.join_channel(channel)
            else:
                print >> sys.stderr, "Unable to init streamer channel:", channel
        elif cmd == 'fini':
            irc.leave_channel(channel)
            pass
    elif cmd == 'points':
        print cmd
    pass


db = db(config)
chat = irc(config)
chat.addMessageCallback(ircMessagesCallback)
chat.connect()

time.sleep(1)
chat.join_channel('epochbottv')
time.sleep(2)
viewers = chat.getViewers("imaqtpie")
print viewers
while True:
    pass
