from enum import Enum
import configparser
import constants as c


class Server(str, Enum):
    NA = 'americas'
    EU = 'europe'
    ASIA = 'asia'


class Setting():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.port = c.PORT_IP
        self.config.read('config.ini')
        self.check()
        self.writeConfig()
        self.clientServer = Server.NA.value
        return

    def check(self):
        section = self.config.sections()
        if 'network' not in section:
            self.config.add_section('network')
            self.config['network']['server'] = Server.NA.value

    def setServer(self, server):
        self.config['network']['server'] = server.value
        self.check()
        self.writeConfig()

    def writeConfig(self):
        self.check()
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
            configfile.close()

    def getServer(self):
        #return self.config['network']['server']
        return self.config.get('network', 'server')

    def getPort(self):
        return self.port
