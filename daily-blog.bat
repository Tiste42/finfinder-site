@echo off
cd /d C:\dev\finfinder-site

:: Log file with date stamp
set LOGFILE=C:\dev\finfinder-site\.claude\logs\blog-%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

:: Create logs directory if needed
if not exist "C:\dev\finfinder-site\.claude\logs" mkdir "C:\dev\finfinder-site\.claude\logs"

:: Run the blog command with full tool access and generous budget
echo [%date% %time%] Starting daily blog generation >> "%LOGFILE%"
claude --dangerously-skip-permissions -p --max-budget-usd 5 "/project:blog auto" >> "%LOGFILE%" 2>&1
set BLOG_EXIT=%ERRORLEVEL%
echo [%date% %time%] Blog generation finished (exit code: %BLOG_EXIT%) >> "%LOGFILE%"

:: If blog generation failed, attempt to commit whatever was generated
if %BLOG_EXIT% NEQ 0 (
    echo [%date% %time%] ERROR: Blog generation failed. Attempting to salvage and commit partial work... >> "%LOGFILE%"

    :: Stage any new blog images and updated blog_posts.json
    git add static/*.webp blog_posts.json >> "%LOGFILE%" 2>&1
    git diff --cached --quiet
    if %ERRORLEVEL% NEQ 0 (
        git commit -m "Add partial blog post (pipeline error - manual review needed)" >> "%LOGFILE%" 2>&1
        echo [%date% %time%] Salvage commit created >> "%LOGFILE%"
    ) else (
        echo [%date% %time%] No files to salvage >> "%LOGFILE%"
    )
)

:: Clean up temp files regardless of success/failure
if exist "gen_image.py" del "gen_image.py" >> "%LOGFILE%" 2>&1
if exist "tmp_new_post.json" del "tmp_new_post.json" >> "%LOGFILE%" 2>&1
if exist "tmp_write_post.py" del "tmp_write_post.py" >> "%LOGFILE%" 2>&1
for %%f in (tmp_*.py tmp_*.json) do del "%%f" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Temp files cleaned up >> "%LOGFILE%"

:: Push if there are commits ahead of remote
git log origin/main..HEAD --oneline > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    git push >> "%LOGFILE%" 2>&1
    echo [%date% %time%] Push completed (exit code: %ERRORLEVEL%) >> "%LOGFILE%"
)

echo [%date% %time%] Daily blog pipeline complete >> "%LOGFILE%"
