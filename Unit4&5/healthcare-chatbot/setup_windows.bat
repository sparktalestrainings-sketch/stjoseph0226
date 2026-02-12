@echo off
echo ========================================
echo MedAssist Healthcare AI - Quick Setup
echo ========================================
echo.

REM Check Python version
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.10 or 3.11
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing dependencies (this may take 2-3 minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages failed. Trying one-by-one...
    pip install streamlit==1.32.2
    pip install langchain==0.1.20
    pip install langchain-community==0.0.38
    pip install langchain-groq==0.1.3
    pip install langchain-cohere==0.1.5
    pip install sentence-transformers==2.7.0
    pip install faiss-cpu==1.8.0
    pip install pypdf==4.2.0
    pip install python-dotenv==1.0.1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Edit .streamlit\secrets.toml and add your API key
echo 2. Get free key from: https://console.groq.com
echo 3. Run: streamlit run app.py
echo.
pause
