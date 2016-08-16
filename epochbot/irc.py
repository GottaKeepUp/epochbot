import json
import re

import requests
import socket
import sys
import threading
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

        self._sendRawCommand('PASS {}\r\n'.format(self._config['twitch']['oauth_password']))
        self._sendRawCommand('NICK {}\r\n'.format(self._config['twitch']['username']))

        # check if succesfully connected

        # start recv'ing messages from IRC
        threading.Thread(target=self.ircRecvMessageWorker).start()
        time.sleep(1)
        self._sendRawCommand('CAP REQ :twitch.tv/membership\r\n')
        time.sleep(1)

    def join_channel(self, channelName):
        self._sendRawCommand('JOIN #{channelName}\r\n'.format(channelName=channelName))

    def leave_channel(self, channelName):
        self._sendRawCommand('PART #{channelName}\r\n'.format(channelName=channelName))

    def getViewers(self, channelName):
        data = requests.get(TWITCH_CHAT_VIEWER_URL.format(channelName=channelName)).json()
        print type(data)

        allChatters = []
        for category, chatters in data['chatters'].iteritems():
            allChatters += chatters
        return allChatters

    def _sendRawCommand(self, cmd):
        print 'sending command:', cmd
        self._conn.send(cmd)

    def pong(self):
        self._sendRawCommand('PONG :tmi.twitch.tv\r\n')

    def sendMessage(self, channelName, msg, hasCLRF=True):
        formattedMsg = 'PRIVMSG #{channelName} :{msg}'.format(channelName=channelName, msg=msg)
        if not hasCLRF:
            formattedMsg += '\r\n'
        self._sendRawCommand(formattedMsg)

    def addMessageCallback(self, callback):
        self._messageCallbacks.append(callback)

    def ircRecvMessageWorker(self):
        while not self._paused:
            print 'reading conn...'
            data = self._conn.recv(1024)
            print 'thread recv', data
            for callback in self._messageCallbacks:
                callback(self, data)

    def _readline(self):
        pass