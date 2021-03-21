import psutil
import subprocess
from setting import Setting, Server
import time
import constants as c 


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
            subprocess.Popen('UI/app/LoRMasterTrackerUI-win32-x64/LoRMasterTrackerUI.exe', shell=False)
    except Exception as e:
        print('runElectron error:', e)


runElectron()