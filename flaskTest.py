from os import name
from flask import Flask, jsonify
import json

from flask.json import tag
from Models import player
from Models.setting import Server
from Models.player import Player
from Models.network import Network
from Models.riot import Riot
from Models.local import Local
from Models.setting import Setting
from Models.leaderboard import checkRank
import time
import threading
from Models.process import updateTrackServer

settingInspect = Setting()
networkInspect = Network(settingInspect)
riotInspect = Riot(networkInspect)
playerInspect = Player(riotInspect)
localInspect = Local(settingInspect)

settingOnly = Setting()

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self.processWork()

    def processWork(self):
        def run_job():
            while True:
                updateTrackServer(settingOnly)
                # port equal to real setting for all other restful api, server can be changed during inspection so no need to set
                settingInspect.port = settingOnly.port
                time.sleep(2)
        t1 = threading.Thread(target=run_job)
        t1.start()

app = FlaskApp(__name__)


def processMatchDetail(detail):
    try:
        playerPuuids = detail['metadata']['participants']
    except Exception as e:
        print('processMatchDetail error:', e)
        return detail
    playernames = []
    player_info = []
    for puuid in playerPuuids:
        name, tag = riotInspect.getPlayerName(puuid)
        rank, lp = checkRank(name, Server.NA.value)
        playernames.append(name + '#' + tag)
        player_info.append({'name':name, 'tag':tag, 'rank':rank, 'lp':lp})
    detail['playernames'] = playernames
    detail['player_info'] = player_info
    return detail

@app.route("/process", methods = ['get'])
def process():
    process_info = {}
    process_info['server'] = settingOnly.riotServer
    process_info['port'] = settingOnly.port
    return jsonify(process_info)

@app.route("/track", methods = ['get'])
def track():
    return jsonify(localInspect.updateStatusFlask())

@app.route("/history/<string:server>/<string:name>/<string:tag>", methods = ['get'])
def history(server, name, tag):
    settingInspect.setServer(Server._value2member_map_[server])
    playerInspect.inspectFlask(name, tag)
    playerInspect.loadMatchsToFlask()
    return jsonify(playerInspect.historyFlask.__dict__['history'])

@app.route("/name/<string:server>/<string:playername>", methods = ['get'])
def get_names(server, playername):
    settingInspect.setServer(Server._value2member_map_[server])
    localInspect.updatePlayernames()
    playerList = set()
    for name in localInspect.playernames:
        if name[0:len(playername)].lower() == playername.lower():
            playerList.add(name)

    returnList = jsonify(list(playerList))
    print(returnList)
    return returnList

@app.route("/search/<string:server>/<string:name>/<string:tag>", methods = ['get'])
def search(name, tag, server):
    settingInspect.setServer(Server._value2member_map_[server])
    allMatches = []
    try:
        puuid = riotInspect.getPlayerPUUID(name, tag)
        matchIds = riotInspect.getMatches(puuid)
        print(matchIds)
        for matchId in matchIds:
            allMatches.append(processMatchDetail(riotInspect.getDetail(matchId, 5)))
    except Exception as e:
        print(e)
        return 'Error'
    return jsonify(allMatches)

@app.route("/inspect/<string:server>/<string:name>/<string:tag>", methods = ['get'])
def inspect(name, tag, server):
    settingInspect.setServer(Server._value2member_map_[server])
    playerInspect.inspectFlask(name, tag)
    inspection = {} 
    inspection['history'] = playerInspect.historyFlask.__dict__['history']
    inspection['matches'] = playerInspect.matchesJson
    return jsonify(inspection)


app.run(port=6123)

