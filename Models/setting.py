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
        self.riotServer = 'americas'
        self.playerId = ''
        self.language = c.DefaultLanguage
        self.isLorRunning = False
