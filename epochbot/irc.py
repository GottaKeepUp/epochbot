import json
import socket
import sys
import threading

import requests
import time

TWITCH_CHAT_VIEWER_URL = 'http://tmi.twitch.tv/group/user/{channelName}/chatters'


# http://tmi.twitch.tv/group/user/twitch/chatters


class irc:
    def __init__(self, config):
        self._config = config
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._messageCallbacks = []
        self._paused = False

    def connect(self):
        self._conn.settimeout(10)
        try:
            self._conn.connect((self._config['twitch']['server'], self._config['twitch']['port']))
        except:
            print 'Cannot connect to server ({}:{}).'.format(self._config['twitch']['server'],
                                                             self._config['twitch']['port']), 'error'
            sys.exit()

        self._conn.settimeout(None)

        self._conn.send('PASS {}\r\n'.format(self._config['twitch']['oauth_password']))
        self._conn.send('NICK {}\r\n'.format(self._config['twitch']['username']))

        # check if succesfully connected

        # start recv'ing messages from IRC
        threading.Thread(target=self.ircRecvMessageWorker).start()

    def join_channel(self, channelName):
        self._sendRawCommand('JOIN #{channelName}'.format(channelName=channelName))
        pass

    def getViewers(self, channelName):
        data = requests.get(TWITCH_CHAT_VIEWER_URL.format(channelName=channelName)).json()
        print type(data)
        allChatters = []
        for category, chatters in data['chatters'].iteritems():
            allChatters += chatters
        return allChatters

    def _sendRawCommand(self, cmd):
        print 'sending _sendRawCommand:', cmd
        self._conn.send(cmd)

    def sendMessage(self, channelName, msg):
        formattedMsg = 'PRIVMSG #{channelName} :{msg}'.format(channelName=channelName, msg=msg)
        print 'sending msg:', formattedMsg
        self._conn.send(formattedMsg)

    def addMessageCallback(self, callback):
        self._messageCallbacks.append(callback)

    def ircRecvMessageWorker(self):
        while not self._paused:
            print 'reading conn...'
            data = self._conn.recv(1024)
            print data
            for callback in self._messageCallbacks:
                callback(self, data)

    def _readline(self):
        pass

def test(chatIRC, line):
    # PING :tmi.twitch.tv
    pass


print "asdfasdf"

with open('../config.json', 'r') as f:
    config = json.load(f)
chat = irc(config)
chat.addMessageCallback(test)
chat.connect()

time.sleep(1)
chat.join_channel('cvballa3g0')
while True:
    pass

viewers = chat.getViewers("imaqtpie")
print viewers
