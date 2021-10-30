#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
import threading
import time
from Models.leaderboard import Leaderboard
from Models.setting import Setting
from Models.riot import Riot
from Models.network import Network
from Models.player import Player
from Models.setting import Server
from Models.cache import Cache
from Models import master
import json
from flask import Flask, jsonify
from flask_cors import CORS
import os
import constants

from random import randrange

sentry_sdk.init(
    "https://1138a186a6384b00a20a6196273c3009@o958702.ingest.sentry.io/5907306",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    debug=True,
    release=constants.SERVER_NUM
)

master.startMasterWorker()
leaderboardModel = Leaderboard()
cacheModel = Cache()

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self.leaderboardsWork()

    def leaderboardsWork(self):
        def run_work():
            while True:
                leaderboardModel.updateAll()
                time.sleep(600)
        work = threading.Thread(target=run_work)
        work.daemon = True
        work.start()

app = FlaskApp(__name__)

@app.route("/history/<string:server>/<string:name>/<string:tag>", methods=['get'])
def history(server, name, tag):
    if server == 'sea':
        print('history: Riot API not suppport SEA')
        return jsonify([])
    settingInspect = Setting()
    settingInspect.riotServer = Server._value2member_map_[server]
    networkInspect = Network(settingInspect)
    riotInspect = Riot(networkInspect, cacheModel)
    playerInspect = Player(riotInspect, leaderboardModel)
    playerInspect.inspectFlask(name, tag, 10)
    return jsonify([summary.__dict__ for summary in playerInspect.summaries.values()])


@app.route("/name/<string:server>/<string:playername>", methods=['get'])
def get_names(server, playername):
    # to-do move functions to master model
    playernames = set()
    nameListPath = constants.getCacheFilePath(server.lower() + '.json')
    if not os.path.isfile(nameListPath):
        nameListPath = 'Resource/' + server.lower() + '.json'
    try:
        with open(nameListPath, 'r', encoding='utf-8') as fp:
            names = json.load(fp)
            for name in names.items():
                playernames.add(name[0] + '#' + name[1])
    except Exception as e:
        print('updatePlayernames', e)
    playerList = set()
    for name in playernames:
        if name[0:len(playername)].lower() == playername.lower():
            playerList.add(name)
    returnList = jsonify(list(playerList))
    return returnList


@app.route("/search/<string:server>/<string:name>/<string:tag>", methods=['get'])
def search(name, tag, server):
    settingModel = Setting()
    settingModel.riotServer = Server._value2member_map_[server]
    maxNum = 20
    riotModel = Riot(Network(settingModel), cacheModel)
    playerModel = Player(riotModel, leaderboardModel)
    playerModel.inspectFlask(name, tag, maxNum)
    if playerModel.error is None:
        return jsonify(playerModel.matchesJson)
    else:
        return jsonify(playerModel.error), playerModel.error['status']['code']


@app.route("/leaderboard/<string:server>", methods=['get'])
def get_leaderboard(server):
    # refactor to leaderboard model
    board = leaderboardModel.getLeaderboard(server)
    boardWithTag = []
    playlistDict = {}
    if board is None:
        return jsonify(boardWithTag)
    nameListPath = constants.getCacheFilePath(server.lower() + '.json')
    if not os.path.isfile(nameListPath):
        nameListPath = 'Resource/' + server.lower() + '.json'
    try:
        with open(nameListPath, 'r', encoding='utf-8') as fp:
            playlistDict = json.load(fp)
    except Exception as e:
        print('Restful: unable to load player list', e)
    for player in board:
        player['rankChange'] = '+' + str(randrange(10))
        if player['name'] in playlistDict:
            player['tag'] = playlistDict[player['name']]
        else:
            player['tag'] = ''
        boardWithTag.append(player)
    return jsonify(boardWithTag)

@app.route("/", methods=['get'])
def welcome():
    info = {}
    info['matchNum'] = len(cacheModel.matchDetails)
    return jsonify(info)