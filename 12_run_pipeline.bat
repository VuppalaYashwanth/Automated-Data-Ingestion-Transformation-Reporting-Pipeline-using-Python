@echo off
REM Quick run script for the data pipeline (Windows)

echo ==========================================
echo Starting Market ^& News Data Pipeline
echo ==========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the pipeline
echo Running pipeline...
cd src
python main.py
cd ..

REM Deactivate virtual environment
if exist venv\Scripts\deactivate.bat (
    call venv\Scripts\deactivate.bat
)

echo.
echo ==========================================
echo Pipeline execution completed!
echo ==========================================
pause
