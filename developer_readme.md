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