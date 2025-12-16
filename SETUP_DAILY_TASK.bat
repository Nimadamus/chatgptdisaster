@echo off
echo ============================================
echo Setting up Daily ChatGPT Disaster Updates
echo ============================================
echo.

REM Delete existing task if it exists
schtasks /delete /tn "ChatGPT Disaster Daily Update" /f 2>nul

REM Create new scheduled task to run at 9 AM daily
schtasks /create /tn "ChatGPT Disaster Daily Update" /tr "C:\Users\Nima\chatgptdisaster\DAILY_UPDATE.bat" /sc daily /st 09:00 /f

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Daily task scheduled for 9:00 AM
    echo.
    echo The site will automatically update every day at 9 AM.
    echo.
    schtasks /query /tn "ChatGPT Disaster Daily Update"
) else (
    echo.
    echo ERROR: Could not create scheduled task.
    echo Try running this script as Administrator.
)

echo.
pause
