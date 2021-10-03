python.exe cdci.py
@REM --noconsole
pyinstaller.exe --icon=./Resource/logo.ico --distpath=./UI/backend LMTService.py 
xcopy /S /Q /Y /F  "%CD%"\Resource "%CD%"\UI\backend\LMTService\Resource\