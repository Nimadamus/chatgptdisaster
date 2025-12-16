@echo off
echo ============================================
echo ChatGPT Disaster - Daily Content Update
echo ============================================
echo.

cd /d C:\Users\Nima\chatgptdisaster\scripts

echo Checking Python...
python --version

echo.
echo Running content generator...
python auto_content_generator.py

echo.
echo ============================================
echo Update complete!
echo ============================================
pause
