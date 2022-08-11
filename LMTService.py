#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
from Models.setting import Setting
from Models.local import Local
from Models.cache import Cache
from Models.process import Process
from flask import Flask, jsonify, redirect
import io
import sys
import constants
import argparse
from waitress import serve
from flask_cors import CORS

argParser = argparse.ArgumentParser()
argParser.add_argument('--port', action='store', type=int, default=26531)
argParser.add_argument('--status', action='store', type=str, default='dev')
args = argParser.parse_args()
print('args: ', args)

isDebug = False

if args.status == 'dev':
    isDebug = True


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
cacheModel = Cache()
settingTrack = Setting()
localTrack = Local(settingTrack, cacheModel)
processTrack = Process(settingTrack)
processTrack.startProcessWorker()
localTrack.startWorker()

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

app = FlaskApp(__name__)
CORS(app)


@app.route("/track", methods=['get'])
def track():
    return jsonify(localTrack.trackJson)

@app.route("/status", methods=['get'])
def get_status():
    status = {}
    status['playerId'] = settingTrack.playerId
    status['port'] = settingTrack.port
    status['server'] = settingTrack.riotServer
    status['language'] = settingTrack.language
    status['lorRunning'] = settingTrack.isLorRunning
    # isLocalApiEnable is updated by track restful
    status['isLocalApiEnable'] = settingTrack.isLocalApiEnable
    return jsonify(status)

@app.route("/local", methods=['get'])
def get_local():
    return jsonify(cacheModel.localMatches)


@app.route("/report/<string:message>", methods=['get'])
def report(message):
    sentry_sdk.capture_message(message)
    return jsonify('OK')

if isDebug:
    app.run(port=args.port, debug=True, use_reloader=False)
else:
    serve(app, host='0.0.0.0', port=args.port)
