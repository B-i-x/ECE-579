@echo off
REM Check if the virtual environment activation script exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Could not find ".venv\Scripts\activate.bat" in the current directory.
    pause
    exit /B 1
)

REM Call the activation script so that it affects the current shell
call .venv\Scripts\activate.bat
echo Virtual environment activated.