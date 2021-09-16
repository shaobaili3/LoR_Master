from enum import Enum
import configparser
import constants as c


class Server(str, Enum):
    NA = 'americas'
    EU = 'europe'
    ASIA = 'asia'
    SEA = 'sea'


class Setting():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.port = c.PORT_IP
        self.config.read('config.ini')
        self.check()
        self.writeConfig()
        self.riotServer = self.config['network']['server']
        self.autoOpenDeck = self.config['track'].getboolean('isAutoOpenDeck')
        self.playerId = 'UNKNOW'
        return

    def check(self):
        section = self.config.sections()
        if 'network' not in section:
            self.config.add_section('network')
            self.config['network']['server'] = Server.NA.value
        # if 'track' not in section:
        #     self.config.add_section('track')
        #     self.config['track']['isAutoOpenDeck'] = 'false'

    def setServer(self, server):
        self.riotServer = server.value

    def saveServer(self):
        self.config['network']['server'] = self.riotServer
        self.check()
        self.writeConfig()

    def writeConfig(self):
        self.check()
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
            configfile.close()

    def getServer(self):
        return self.riotServer

    def getPort(self):
        return self.port
