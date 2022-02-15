import psutil
import constants as c
import sentry_sdk
import locale
import requests
import json
import threading
import time

class Process():
    def __init__(self, setting):
        self.sysLanguage = locale.getdefaultlocale()[0]
        self.setting = setting

    def getLogPath(self):
        logFilePath = None
        for proc in psutil.process_iter():
            try:
                if proc.name() == u"LoR.exe":
                    logFilePath = proc.cmdline()[4]
            except psutil.AccessDenied:
                print("Permission error or access denied on process")
                return None
            except Exception as e:
                print('getLogPath error: ', e)
                return None
        return logFilePath


    def readLog(self):
        path = self.getLogPath()
        if path is None:
            self.setting.isLorRunning = False
        else:
            self.setting.isLorRunning = True
            try:
                with open(path, 'r', encoding='utf-8') as lorLog:
                    for line in lorLog.readlines():
                        line = line.strip()
                        if '[TrySetShardDnsLive] setting dns data by affinity' in line:
                            self.setting.riotServer = str(line).split().pop()
                        if 'Server opened successfully at port: ' in line:
                            self.setting.port = str(line).split().pop()
                        if 'Using user-preferred language CultureInfo of ' in line:
                            self.setting.language = str(line).split().pop()
                        if '[CheckingForUpdates] StartCheckingForUpdates for user ' in line:
                            playerId = str(line).split("[CheckingForUpdates] StartCheckingForUpdates for user ", 1)[1]
                            if playerId != self.setting.playerId:
                                self.setting.playerId = playerId
                                sentry_sdk.set_user({"id": playerId, "username": playerId + ' ' + self.setting.riotServer, "ip_address": "{{auto}}"})
                                sentry_sdk.capture_message(
                                    playerId + ' ' + self.setting.riotServer)
                                try:
                                    data = {}
                                    data['riot_id'] = self.setting.playerId
                                    data['server'] = self.setting.riotServer
                                    data['riot_language'] = self.setting.language
                                    data['sys_language'] = self.sysLanguage
                                    url = "https://lormaster.herokuapp.com/login"
                                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                                    response = requests.post(url, data=json.dumps(data), headers=headers)
                                    print(response.text)
                                except requests.exceptions.HTTPError as e:
                                    print('post error', e.response.text)
            except IOError:
                print('log file not accessible: ', path)
            except Exception as e:
                print('readLog error', e)


    def getInfo(self):
        while True:
            time.sleep(5)
            self.readLog()

    def startProcessWorker(self):
        n = threading.Thread(target=self.getInfo)
        n.daemon = True
        n.start()
