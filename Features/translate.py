import winreg
import hashlib
import shutil
import constants as c

lorBinPath = ''
lorChineseBinPath = 'Resource/LocalizedText_en_us.bin'


def regEdit(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(
        aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0,
        winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            # this line will break if using debug mode ????
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(
                    asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(
                    asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            try:
                software['InstallLocation'] = winreg.QueryValueEx(
                    asubkey, "InstallLocation")[0]
            except EnvironmentError:
                software['InstallLocation'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list


####md5检测算法####
def hash(file_path, Bytes=1024):
    #print(file_path)
    md5_1 = hashlib.md5()  #创建一个md5算法对象
    with open(file_path, 'r', encoding='utf-8') as f:  #打开一个文件，必须是'rb'模式打开
        while 1:
            data = f.read(Bytes)  #由于是一个文件，每次只读取固定字节
            if data:  #当读取内容不为空时对读取内容进行update
                md5_1.update(data)
            else:  #当整个文件读完之后停止update
                break
    ret = md5_1.hexdigest()  #获取这个文件的MD5值
    return ret


def detect():
    # To-do: handle unknow error, add GUI for error message
    try:
        software_list = regEdit(
            winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + regEdit(
                winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + regEdit(
                    winreg.HKEY_CURRENT_USER, 0)

        for software in software_list:
            #print('Name=%s, Version=%s, Publisher=%s' % (software['name'], software['InstallLocation'], software['publisher']))
            if software['name'] == 'Legends of Runeterra':
                #print(software['InstallLocation'])
                lorBinPath = software['InstallLocation'].replace(
                    '/Game', ''
                ) + '/PatcherData/PatchableFiles/GamePlayData/LocalizedText_'
    except Exception as e:
        print('translate detect error:', e)

    if lorBinPath is None:
        print('LoR.exe is not found')
        return
    print(lorBinPath)
    #shutil.copy(lorChineseBinPath, lorBinPath)
    while True:
        finalPath = lorBinPath + c.DEFAULT_LANGUAGE.lower().replace('-', '_') + '.bin'
        if hash(finalPath) != hash(
                lorChineseBinPath):  #一旦检查到游戏的汉化文件和我们替换的汉化文件不相等（因为被游戏客户端修正了）            
            print(finalPath)
            shutil.copy(lorChineseBinPath, finalPath)  #再次替换汉化文件到游戏的存放汉化文件的目录