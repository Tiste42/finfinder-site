@echo off
cd /d C:\dev\finfinder-site

:: Log file with date stamp
set LOGFILE=C:\dev\finfinder-site\.claude\logs\blog-%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

:: Create logs directory if needed
if not exist "C:\dev\finfinder-site\.claude\logs" mkdir "C:\dev\finfinder-site\.claude\logs"

:: Run the blog command, log output
echo [%date% %time%] Starting daily blog generation >> "%LOGFILE%"
claude --dangerously-skip-permissions --print "Run /project:blog auto" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Finished >> "%LOGFILE%"
