@echo off
cd /d C:\dev\finfinder-site

:: Log file with date stamp
set LOGFILE=C:\dev\finfinder-site\.claude\logs\blog-%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

:: Create logs directory if needed
if not exist "C:\dev\finfinder-site\.claude\logs" mkdir "C:\dev\finfinder-site\.claude\logs"

:: Run the blog command with full tool access and generous budget
echo [%date% %time%] Starting daily blog generation >> "%LOGFILE%"
claude --dangerously-skip-permissions -p --max-budget-usd 5 "/project:blog auto" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Finished (exit code: %ERRORLEVEL%) >> "%LOGFILE%"
