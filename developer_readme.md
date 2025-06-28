# 🛠 Subtitle Generator - Developer Setup

## Prerequisites
- Python 3.8+
- Git
- FFmpeg (for manual testing)

## Setup

1. **Clone & Prepare**:
```bash
git clone https://github.com/Manan-49/SRT-GENERATOR.git
cd subtitle-generator
python -m venv .venv

# Activate & Install:
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

#Run/Build:
# Run GUI:
python tkinter_gui_app.py

# Build EXE (Windows):
build.bat

## Model Installation
1. Create `models` folder in your project root
2. Download models from [VOSK Models](https://alphacephei.com/vosk/models):
```bash
# Recommended models (small size):
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -P models/
wget https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip -P models/

# Extract:
unzip "models/*.zip" -d models/

FFmpeg Setup
Download Windows build from FFmpeg Official

Place ffmpeg.exe in project root

Verify installation:

bash
ffmpeg -version
Folder Structure After Setup
text
project/
├── models/
│   ├── vosk-model-small-en-us-0.15/
│   └── vosk-model-small-hi-0.22/
└── ffmpeg.exe  <-- Must be in root
💡 For Linux/macOS, install FFmpeg via package manager:

bash
# Ubuntu/Debian
sudo apt install ffmpeg
# macOS
brew install ffmpeg
