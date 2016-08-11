import socket
import sys


# http://tmi.twitch.tv/group/user/twitch/chatters

class irc:
    def __init__(self, config):
        self.config = config
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.conn.settimeout(10)
        try:
            self.conn.connect((self.config['server'], self.config['port']))
        except:
            print 'Cannot connect to server ({}:{}).'.format(self.config['server'], self.config['port']), 'error'
            sys.exit()

        self.conn.settimeout(None)
        self.conn.send('PASS {}\r\n'.format(self.config['oauth_password']))
        self.conn.send('NICK {}\r\n'.format(self.config['username']))

        # check if succesfully connected

    def join_channel(self, channelName):
        pass


print "asdfasdf"
