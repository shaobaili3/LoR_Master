import psutil
import subprocess
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
            return None
        except IndexError:
            print('Index error')
            return None
    if logFilePath is not None:
        return logFilePath
    else:
        #print('LoR not started')
        return None


def getPort(setting):
    path = getLoRLogFile()
    if path is not None:
        try:
            with open(path, 'rt', encoding='utf-8') as lorLog:
                for line in lorLog.readlines():
                    line = line.strip()
                    if '[TrySetShardDnsLive] setting dns data by affinity' in line:
                        # print('server:', line.split()[-1])
                        # setting.setServer(Server._value2member_map_[line.split()[-1]])
                        setting.riotServer = str(line).split().pop()
                    if 'Server opened successfully at port: ' in line:
                        # print('port:', line.split()[-1])
                        setting.port = str(line).split().pop()
        except IOError:
            print('log file not accessible: ', path)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))

def runElectron():
    try:
        isRuning = False
        for proc in psutil.process_iter():
            try:
                if proc.name() == u"LoRMasterTracker.exe":
                    isRuning = True
            except psutil.AccessDenied:
                print("Permission error or access denied on process")
                return None
            except IndexError:
                print('Index error')
                return None

        if isRuning is False:
            subprocess.run('UI/app/LoRMasterTrackerUI-win32-x64/LoRMasterTrackerUI.exe', shell=False)
    except Exception as e:
        print('runElectron error:', e)


def updateTrackServer(setting):
    while (True):
        time.sleep(2)
        getPort(setting)
        