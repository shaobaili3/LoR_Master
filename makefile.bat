nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=pylint-warnings --recurse-all --output-dir=app/debug --windows-icon=Resource/image.ico --nofollow-import-to=pystray,PIL,aiohttp LoRMasterTracker.py

nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=pylint-warnings --recurse-all --output-dir=app --windows-icon=Resource/image.ico --nofollow-import-to=pystray,PIL,aiohttp --windows-disable-console LoRMasterTracker.py

pause

nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=pylint-warnings --recurse-all --output-dir=app/debug --windows-icon=test.ico --nofollow-import-to=aiohttp --plugin-enable=qt-plugins LoRMasterInspector.py
nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=pylint-warnings --recurse-all --output-dir=app --windows-icon=test.ico --nofollow-import-to=aiohttp --windows-disable-console --plugin-enable=qt-plugins LoRMasterInspector.py



pyinstaller.exe --onefile --icon=test.ico --noconsole LoRMasterInspector.py