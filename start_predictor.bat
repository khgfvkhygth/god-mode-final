@echo off
echo [🚀] Launching Godmode Predictor System...
echo --------------------------------------------

REM Activate your virtual environment here if using one
REM call C:\Users\joe\myenv\Scripts\activate.bat

REM Start Streamlit app in a new terminal
start cmd /k "streamlit run app.py"

REM Start live predictor
python live_predictor.py

pause