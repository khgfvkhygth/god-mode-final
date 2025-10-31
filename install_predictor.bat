@echo off
SETLOCAL ENABLEEXTENSIONS

echo [🚀] Godmode Predictor Full Installer for Windows
echo -----------------------------------------------

REM -- Step 1: Ensure user is in correct directory
echo [🔎] Current directory: %CD%

REM -- Step 2: Create bustabit-browser folders
echo [📁] Creating directories...
mkdir "C:\Users\joe\bustabit-browser\chrome-win64" 2>nul
mkdir "C:\Users\joe\bustabit-browser\chromedriver-win64" 2>nul

REM -- Step 3: Download Chrome for Testing
echo [⬇️ ] Downloading Chrome for Testing...
curl -L -o chrome-win64.zip https://storage.googleapis.com/chrome-for-testing-public/142.0.7444.52/win64/chrome-win64.zip
powershell -Command "Expand-Archive -Path 'chrome-win64.zip' -DestinationPath 'C:\Users\joe\bustabit-browser\' -Force"
move "C:\Users\joe\bustabit-browser\chrome-win64\chrome-win64" "C:\Users\joe\bustabit-browser\" >nul 2>&1
del chrome-win64.zip

REM -- Step 4: Download ChromeDriver
echo [⬇️ ] Downloading ChromeDriver...
curl -L -o chromedriver-win64.zip https://storage.googleapis.com/chrome-for-testing-public/142.0.7444.52/win64/chromedriver-win64.zip
powershell -Command "Expand-Archive -Path 'chromedriver-win64.zip' -DestinationPath 'C:\Users\joe\bustabit-browser\' -Force"
move "C:\Users\joe\bustabit-browser\chromedriver-win64\chromedriver-win64" "C:\Users\joe\bustabit-browser\" >nul 2>&1
del chromedriver-win64.zip

REM -- Step 5: Check for Tesseract
IF EXIST "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [✅] Tesseract already installed.
) ELSE (
    echo [⚠️] Tesseract is not installed.
    echo [👉] Download from: https://github.com/tesseract-ocr/tesseract/releases
    start https://github.com/tesseract-ocr/tesseract/releases
)

REM -- Step 6: Install Python packages
echo [📦] Installing required Python packages...
pip install -r requirements.txt

REM -- Done
echo -----------------------------------------------
echo [✅] Setup complete. You may now run start_predictor.bat
pause