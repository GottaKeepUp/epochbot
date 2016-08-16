import sys

import MySQLdb


class db:
    def __init__(self, config):
        self._config = config
        try:
            self._conn = MySQLdb.connect(host=self._config['mysql']['host'],
                                         user=self._config['mysql']['username'],
                                         passwd=self._config['mysql']['password'],
                                         db=self._config['mysql']['database'])
        except MySQLdb.OperationalError, e:
            print e
            if e.args[1] == 1045:  # Access denied
                print >> sys.stderr, e
                print >> sys.stderr, 'Are you using the correct password?\r\n'
                raise MySQLdb.OperationalError
            elif e.args[0] == 1049:  # Unknown database
                print >> sys.stderr, e
                print >> sys.stderr, "Does the database exist? (run the sql db script)"
            raise MySQLdb.OperationalError

    def getMods(self, channel):
        pass

    def getViewerPoints(self, channel, viewer):
        pass

    def initChannel(self, channel):
        pass