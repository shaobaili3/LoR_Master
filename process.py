import psutil




logFilePath = None
for proc in psutil.process_iter():
    try:
        if proc.name() == u"LoR.exe":
            #print(proc)
            #proc.cmdline()
            logFilePath = proc.cmdline()[4]
    except psutil.AccessDenied:
        print("Permission error or access denied on process")

if logFilePath:
    print(logFilePath)
else:
    pass


