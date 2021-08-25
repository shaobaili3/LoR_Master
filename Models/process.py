import psutil
import subprocess
from Models.setting import Setting, Server
import time
import constants as c
import sentry_sdk

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
        except Exception as e:
            print('error getLoRLogFile: ', e)
    if logFilePath is not None:
        return logFilePath
    else:
        #print('LoR not started')
        return None


def getPort(setting):
    path = getLoRLogFile()
    if path is not None:
        try:
            with open(path, 'r', encoding='utf-8') as lorLog:
                for line in lorLog.readlines():
                    line = line.strip()
                    if '[TrySetShardDnsLive] setting dns data by affinity' in line:
                        # print('server:', line.split()[-1])
                        # setting.setServer(Server._value2member_map_[line.split()[-1]])
                        setting.riotServer = str(line).split().pop()
                    if 'Server opened successfully at port: ' in line:
                        # print('port:', line.split()[-1])
                        setting.port = str(line).split().pop()

                    if 'Using user-preferred language CultureInfo of ' in line:
                        c.DefaultLanguage = str(line).split().pop()
                        # print('Language:  ', c.DefaultLanguage)

                    if '[CheckingForUpdates] StartCheckingForUpdates for user ' in line:
                        playerId = str(line).split().pop()
                        if playerId != setting.playerId:
                            setting.playerId = playerId
                            sentry_sdk.set_user({"id": playerId, "username": setting.riotServer, "ip_address": "{{auto}}"})
                            sentry_sdk.capture_message(playerId + ' ' + setting.riotServer)
        except IOError:
            print('log file not accessible: ', path)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))


def runElectron():
    try:
        isRuning = False
        allProcess = set()
        for proc in psutil.process_iter():
            allProcess.add(proc.name())
            
        if u"LoRMasterTrackerUI.exe" in allProcess:
            isRuning = True

        if isRuning is False:
            subprocess.Popen(
                'UI/app/LoRMasterTrackerUI-win32-x64/LoRMasterTrackerUI.exe',
                shell=False)
    except psutil.AccessDenied:
        print("Permission error or access denied on process")
        return None
    except IndexError as e:
        print('runElectron IndexError: ', e)
        return None
    except Exception as e:
        print('runElectron error:', e)


def isSimulation():
    isPython = True
    try:
        for proc in psutil.process_iter():
            try:
                if proc.name() == u"LoRMasterTracker.exe":
                    isPython = False
                if proc.name() == u"python.exe":
                    isPython = True
            except psutil.AccessDenied:
                print("Permission error or access denied on process")
                return isPython
            except IndexError as e:
                print('runElectron IndexError: ', e)
                return isPython
    except Exception as e:
        print('runElectron error:', e)
        return isPython
    print('isSimulation: ', isPython)
    return isPython


def updateTrackServer(setting):
        getPort(setting)
