nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=pylint-warnings --recurse-all --output-dir=app/debug --windows-icon=Resource/image.ico --nofollow-import-to=pystray,PIL,aiohttp LoRmaster.py

nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=pylint-warnings --recurse-all --output-dir=app --windows-icon=Resource/image.ico --nofollow-import-to=pystray,PIL,aiohttp --windows-disable-console LoRmaster.py

pause