from pathlib import Path
from appdirs import user_data_dir
import os
PORT_IP = '21337'

LOCAL_MATCH = '/positional-rectangles'
LOCAL_DECK = '/static-decklist'
LOCAL_RESULT = '/game-result'
IP_KEY = 'http://127.0.0.1:'

LEADERBOARD_KEY = '.api.riotgames.com/lor/ranked/v1/leaderboards/'
VERSION_NUM = 'v0.12.6'
SERVER_NUM = 'v2.0'
DISPLAY_TITLE = 'LoR Master Tracker'
MAX_NUM_INSPECT = 10
MAX_NUM_TRACK = 10
MAX_NUM_ALL = 20

DefaultLanguage = 'en-US'

UNSUPPORTED_MODE = ['Expeditions', 'Mods_URF', 'Power2', 'Mods_Power_1', 'Power_4']
UNSUPPORTED_TYPE = ['AI']
# temp remove AI for debug
# UNSUPPORTED_TYPE = []
SUPPORTED_MODE = ['SeasonalTournamentLobby',
                  'LastCallQualifierGauntletLobby', 'Bo3ChallengeLobby', 'StandardGauntlet', 'Constructed']

appDir = user_data_dir('LMT', DISPLAY_TITLE)


def getCacheFilePath(fileName, subDir='backend'):
    filePath = Path(appDir, subDir, fileName)
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    return filePath
