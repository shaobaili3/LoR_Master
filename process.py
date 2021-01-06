import psutil

for proc in psutil.process_iter():
    try:
        if proc.name() == u"LoR.exe":
            print(proc)
            print(proc.cmdline())
    except psutil.AccessDenied:
        print("Permission error or access denied on process")