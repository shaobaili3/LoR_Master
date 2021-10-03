#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import threading
import time
from Models.leaderboard import Leaderboard
from Models.setting import Setting
from Models.local import Local
from Models.riot import Riot
from Models.network import Network
from Models.player import Player
from Models.setting import Server
from Models.cache import Cache
from Models import master
from Models.process import readLog
import json
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
import io

import sys
import os
import constants
import argparse


isDebug = True

if os.getenv('IS_PUBLISH') == 'true':
    isDebug = False


argParser = argparse.ArgumentParser()
argParser.add_argument('--port', action='store', type=int, default=26531)
args = argParser.parse_args()
print('args: ', args)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
print('utf8 string test: ', '卡尼能布恩', '째남모')

sentry_sdk.init(
    "https://1138a186a6384b00a20a6196273c3009@o958702.ingest.sentry.io/5907306",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    debug=isDebug,
    release=constants.VERSION_NUM
)

sentry_sdk.set_context("info", {
    "version": constants.VERSION_NUM
})

master.startMasterWorker()
leaderboardModel = Leaderboard()
cacheModel = Cache()

settingTrack = Setting()
localTrack = Local(settingTrack)


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self.processWork()
        self.leaderboardsWork()

    def processWork(self):
        def run_work():
            while True:
                readLog(settingTrack)
                time.sleep(3)
        work = threading.Thread(target=run_work)
        work.daemon = True
        work.start()

    def leaderboardsWork(self):
        def run_work():
            while True:
                leaderboardModel.updateAll()
                time.sleep(600)
        work = threading.Thread(target=run_work)
        work.daemon = True
        work.start()


app = FlaskApp(__name__)


@app.route("/process", methods=['get'])
def process():
    process_info = {}
    process_info['server'] = settingTrack.riotServer
    process_info['port'] = settingTrack.port
    return jsonify(process_info)


@app.route("/track", methods=['get'])
def track():
    return jsonify(localTrack.updateStatusFlask())


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
    maxNum = constants.MAX_NUM_INSPECT
    if (name + '#' + tag).lower() == settingTrack.playerId.lower():
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
        if player['name'] in playlistDict:
            player['tag'] = playlistDict[player['name']]
        else:
            player['tag'] = ''
        boardWithTag.append(player)
    return jsonify(boardWithTag)


@app.route("/opInfo", methods=['get'])
def opInfo():
    opInfo = {}
    localTrack.updateTagByName(
        localTrack.positional_rectangles['OpponentName'])
    opInfo['name'] = localTrack.positional_rectangles['OpponentName']
    opInfo['tag'] = localTrack.opponentTag
    opInfo['rank'], opInfo['lp'] = leaderboardModel.checkRank(
        opInfo['name'], settingTrack.riotServer)
    return jsonify(opInfo)


@app.route("/status", methods=['get'])
def get_status():
    status = {}
    status['playerId'] = settingTrack.playerId
    status['port'] = settingTrack.port
    status['server'] = settingTrack.riotServer
    status['language'] = settingTrack.language
    status['lorRunning'] = settingTrack.isLorRunning
    return jsonify(status)


@app.route("/report/<string:message>", methods=['get'])
def report(message):
    sentry_sdk.capture_message(message)
    return jsonify('OK')


app.run(port=args.port, debug=isDebug, use_reloader=False)
