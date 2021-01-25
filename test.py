import psutil
from setting import Setting, Server
import time
import os


def getLoRLogFile():
    print('getLoRLogFile')
    log('getLoRLogFile')
    logFilePath = None
    for proc in psutil.process_iter():
        try:
            if proc.name() == u"LoR.exe":
                logFilePath = proc.cmdline()[4]
        except psutil.AccessDenied:
            print("Permission error or access denied on process")

    if logFilePath is not None:
        print('LogFile: ' + logFilePath)
        log('LogFile:' + logFilePath)
        return logFilePath
    else:
        print('LoR not started')
        log('LoR not started')
        return None


def getPort():
    path = getLoRLogFile()
    print('getPort')
    print('getPort')
    if path is not None:
        try:
            with open(path, 'r') as lorLog:
                print('filed opened' + lorLog.readline())
                log('filed opened' + lorLog.readline())
                for line in lorLog.readlines():
                    line = line.strip()
                    print('inside loop: line' + line)
                    log('inside loop: line' + line)
                    if '[TrySetShardDnsLive] setting dns data by affinity' in line:
                        # print('server:', line.split()[-1])
                        # setting.setServer(Server._value2member_map_[line.split()[-1]])
                        print('[TrySetShardDnsLive]')
                        log('log' + '[TrySetShardDnsLive]')
                        server = str(line).split().pop()

                        print('server: ' + str(server))
                        log('server: ' + str(server))
                    if 'Server opened successfully at port: ' in line:
                        # print('port:', line.split()[-1])
                        print('successfully at port:')
                        log('log' + 'successfully at port:')
                        port = str(line).split().pop()
                        print('port: ' + port)
                        log('port: ' + port)
        except IOError:
            print('log file not accessible: ' + path)
            log('log file not accessible: ' + path)


def updateTrackServer():
    while (True):
        time.sleep(2)
        getPort()


def log(txt):
    file_object = open('log.txt', 'a')
    # Append 'hello' at the end of file
    file_object.write(txt + '\n')
    # Close the file
    file_object.close()


updateTrackServer()

input()

# def test(path):
#     path = 'Logs/' + path
#     print(path)
#     print('getPort')
#     print('getPort')
#     if path is not None:
#         try:
#             with open(path, 'r') as lorLog:
#                 for line in lorLog:
#                     line = line.strip()
#                     if '[TrySetShardDnsLive] setting dns data by affinity' in line:
#                         # print('server:', line.split()[-1])
#                         # setting.setServer(Server._value2member_map_[line.split()[-1]])
#                         print('server: ' + line.split()[-1].lower())
#                         log('server: ' + line.split()[-1].lower())
#                     if 'Server opened successfully at port: ' in line:
#                         # print('port:', line.split()[-1])
#                         print('port: ' + line.split()[-1])
#                         log('port: ' + line.split()[-1])
#         except IOError:
#             print('log file not accessible: ', path)
#             log('log file not accessible: ' + path)

# arr = os.listdir('Logs')
# for a in arr:
#     test(a)