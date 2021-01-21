import psutil
from setting import Setting, Server
import time


def getLoRLogFile():
    #print('process detecting starts')
    logFilePath = None
    for proc in psutil.process_iter():
        try:
            if proc.name() == u"LoR.exe":
                logFilePath = proc.cmdline()[4]
        except psutil.AccessDenied:
            print("Permission error or access denied on process")

    if logFilePath:
        return logFilePath
    else:
        #print('LoR not started')
        return None


def getPort(setting):
    path = getLoRLogFile()
    if path:
        try:
            with open(path, 'r') as lorLog:
                for line in lorLog:
                    line = line.strip()
                    if '[TrySetShardDnsLive] setting dns data by affinity' in line:
                        # print('server:', line.split()[-1])
                        setting.setServer(Server._value2member_map_[line.split()[-1]])
                    if 'Server opened successfully at port: ' in line:
                        # print('port:', line.split()[-1])
                        setting.port = line.split()[-1]
                        
        except IOError:
            print('log file not accessible: ', path)


def updateTrackServer(setting):
    while (True):
        time.sleep(1)
        getPort(setting)


#updateTrackServer(1)