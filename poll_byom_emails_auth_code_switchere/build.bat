@echo off
pyinstaller --onedir --contents-directory "." --onefile ./poll_byom_emails_for_switchere.py
pause