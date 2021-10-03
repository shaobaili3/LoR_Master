python.exe cdci.py
pyinstaller.exe --icon=./Resource/logo.ico --distpath=./UI/backend LMTService.py --noconsole
xcopy /S /Q /Y /F  "%CD%"\Resource "%CD%"\UI\backend\LMTService\Resource\