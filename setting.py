from enum import Enum
import configparser
import constants as c


class Setting():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.check()
        self.writeConfig()
        return

    def check(self):
        section = self.config.sections()
        if 'network' not in section:
            self.config.add_section('network')
            self.config['network']['server'] = Server.NA.value
        if 'local' not in section:
            self.config.add_section('local')
            self.config['local']['port'] = c.PORT_IP
        #server = self.config.get('network', 'server')
        port = self.config.get('local', 'port')
        # if not server in list(map(str, Server)):
        #     #self.config.add_section('network')
        #     self.config['network']['server'] = Server.NA.value
        if not port.isnumeric():
            self.config['local']['port'] = c.PORT_IP

    def setServer(self, server):
        self.config['network']['server'] = server.value
        self.check()
        self.writeConfig()

    def setPort(self, port):
        self.config['local']['port'] = port
        self.check()
        self.writeConfig()

    def writeConfig(self):
        self.check()
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
            configfile.close()

    def getServer(self):
        return self.config.get('network', 'server')

    def getPort(self):
        return self.config.get('local', 'port')


class Server(str, Enum):
    NA = 'americas'
    EU = 'europe'
    ASIA = 'asia'
