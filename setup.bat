@echo off
echo ====================================
echo Arabic Novel Parser - Quick Setup
echo ====================================
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To start the application, run:
echo.
echo   streamlit run app.py
echo.
echo The app will open in your browser.
echo.
pause
