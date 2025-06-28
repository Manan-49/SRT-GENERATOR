@echo off
REM ================================================
REM Subtitle Generator - Fixed Build Script
REM ================================================

SETLOCAL ENABLEDELAYEDEXPANSION

title Subtitle Generator Build Process

REM 1. Python Detection
echo.
echo 🔍 Checking Python installation...
where python >nul 2>&1 || (
    echo ❌ ERROR: Python not found in PATH
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 2. Verify Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" || (
    echo ❌ ERROR: Python 3.8 or higher required
    python --version
    pause
    exit /b 1
)

REM 3. Install PyInstaller properly
echo.
echo 📦 Checking PyInstaller...
python -c "import pyinstaller" 2>nul || (
    echo Installing PyInstaller...
    pip install --upgrade pip || (
        echo ❌ Failed to update pip
        pause
        exit /b 1
    )
    pip install pyinstaller || (
        echo ❌ Failed to install PyInstaller
        echo Trying with --user flag...
        pip install --user pyinstaller || (
            echo ❌ Completely failed to install PyInstaller
            pause
            exit /b 1
        )
    )
)

REM 4. Virtual Environment Setup
echo.
echo 🛠 Setting up virtual environment...
if not exist ".venv\" (
    python -m venv .venv || (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM 5. Activate and install requirements
echo.
echo ⚙ Activating virtual environment...
call .venv\Scripts\activate || (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing requirements...
pip install -r requirements.txt || (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

REM 6. Build executable
echo.
echo 🔨 Building executable...
python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name SubtitleGenerator ^
  --add-binary "ffmpeg.exe;." ^
  --add-data "models;models" ^
  --add-data "video;video" ^
  --hidden-import="customtkinter" ^
  --hidden-import="PIL._tkinter_finder" ^
  --hidden-import="vosk" ^
  --hidden-import="soundfile" ^
  --collect-all customtkinter ^
  --collect-all vosk ^
  --clean ^
  --noconfirm ^
  tkinter_gui_app.py || (
    echo ❌ Build failed
    pause
    exit /b 1
  )

REM 7. Package output
echo.
echo 📦 Packaging output...
if not exist "dist\output" mkdir "dist\output"
xcopy "video" "dist\video" /E /I /Y >nul
xcopy "models" "dist\models" /E /I /Y >nul

powershell -Command "$ProgressPreference = 'SilentlyContinue'; Compress-Archive -Path 'dist\SubtitleGenerator.exe', 'dist\models', 'dist\video' -DestinationPath 'SubtitleGenerator.zip' -Force" || (
    echo ❌ Failed to create ZIP
    echo Creating manual ZIP...
    powershell -Command "Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist', 'SubtitleGenerator.zip')"
)

echo.
echo ✅ BUILD SUCCESSFUL!
echo 📦 Output: dist\SubtitleGenerator.exe
echo 📦 Package: SubtitleGenerator.zip
pause