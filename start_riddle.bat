echo LockMyScreenRiddle started >> log.txt
@echo off
cd /d C:\LockMyScreenRiddle
call venv\Scripts\activate.bat
python lockscreen.py
