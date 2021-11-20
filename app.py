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
from flask import Flask, jsonify, redirect
from flask_cors import CORS
import os
import constants
from Models.heroku import Heroku

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
herokuModel = Heroku(leaderboardModel)

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self.leaderboardsWork()

    def leaderboardsWork(self):
        def run_work():
            while True:
                leaderboardModel.updateAll()
                time.sleep(3000)
        work = threading.Thread(target=run_work)
        work.daemon = True
        work.start()

app = FlaskApp(__name__)
CORS(app)
app.config["DEBUG"] = False
app.config["DEVELOPMENT"] = False

@app.route("/history/<string:server>/<string:name>/<string:tag>", methods=['get'])
def history(server, name, tag):
    return jsonify(herokuModel.getHistory(server, name, tag))


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
    return redirect("https://lormaster.herokuapp.com/search/" + server + '/' + name + '/' + tag)


@app.route("/leaderboard/<string:server>", methods=['get'])
def get_leaderboard(server):
    # # refactor to leaderboard model
    # board = leaderboardModel.getLeaderboard(server)
    # boardWithTag = []
    # playlistDict = {}
    # if board is None:
    #     return jsonify(boardWithTag)
    # nameListPath = constants.getCacheFilePath(server.lower() + '.json')
    # if not os.path.isfile(nameListPath):
    #     nameListPath = 'Resource/' + server.lower() + '.json'
    # try:
    #     with open(nameListPath, 'r', encoding='utf-8') as fp:
    #         playlistDict = json.load(fp)
    # except Exception as e:
    #     print('Restful: unable to load player list', e)
    # for player in board:
    #     change = player['rankChange']
    #     if isinstance(change,int):
    #         if change > 0:
    #             player['rankChange'] = '+' + str(change)
    #         elif change < 0:
    #             player['rankChange'] = str(change)
    #         else:
    #             player['rankChange'] = ''
    #     if player['name'] in playlistDict:
    #         player['tag'] = playlistDict[player['name']]
    #     else:
    #         player['tag'] = ''
    #     boardWithTag.append(player)
    # return jsonify(boardWithTag)
    return redirect("https://lormaster.herokuapp.com/ccgboard/" + server)

@app.route("/", methods=['get'])
def welcome():
    info = {}
    info['matchNum'] = len(cacheModel.matchDetails)
    return jsonify(info)

is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
if not is_gunicorn:
    app.run(port='26531', debug=True, use_reloader=False)