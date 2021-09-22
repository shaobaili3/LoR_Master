
@REM pyinstaller.exe --icon=logo.ico --noconsole --distpath=./app LoRMasterTracker.py
pyinstaller.exe --icon=./Resource/logo.ico --distpath=./UI/backend LMTService.py
xcopy /S /Q /Y /F  "%CD%"\Resource "%CD%"\UI\backend\LMTService\Resource\
pause