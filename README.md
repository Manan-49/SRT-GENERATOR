# SRT-GENERATOR
# 🎬 Subtitle Generator - Offline Desktop App

![App Screenshot](![Screenshot 2025-06-28 144806](https://github.com/user-attachments/assets/7a1caba5-b0ce-4e41-a93f-20c3c91c91da)
) *(Replace with actual screenshot)*

## 🖥️ Usage Guide (Step-by-Step)

### 1. Launching the App
- Double-click `SubtitleGenerator.exe`  
  *(Windows may show a security warning → Click "More info" → "Run anyway")*

![First Run Warning](![Screenshot 2025-06-28 145444](https://github.com/user-attachments/assets/8ce65cba-e604-42df-bf87-c5ae9cb0f526)
) *(Screenshot example)*

---

### 2. Loading Your Video
- Click **"Browse"** next to "Video File"  
- Select your video (MP4/AVI/MOV etc.)  
- App auto-detects compatible files

![Video Selection](![Screenshot 2025-06-28 145039](https://github.com/user-attachments/assets/556aed19-4705-4bbd-ba6b-81abd75157f7)
)

---

### 3. Setting Output (Optional)
- Default: Saves to `output/video_name.srt`  
- To change: Click **"Browse"** next to "Output SRT File"

---

### 4. Language Selection
| Option | Action |
|--------|--------|
| English | Leave default selected |
| Hindi | Select "Hindi" radio button |
| Custom Model | Choose "Custom Model" and browse to model folder |

![Language Selection](![Screenshot 2025-06-28 145132](https://github.com/user-attachments/assets/926521b4-398d-4bcc-926d-5bc193742c2b)
)

---

### 5. Advanced Options
- ☑ **Keep extracted audio** - Saves temporary WAV file  
- ☑ **Debug mode** - Shows detailed logs *(developers only)*

---

### 6. Generating Subtitles
1. Click **"Generate Subtitles"** button  
2. Progress bar shows:  
   - Audio extraction  
   - Speech recognition  
   - SRT file creation  
3. Completion popup appears  

![Processing Screen](![Screenshot 2025-06-28 145224](https://github.com/user-attachments/assets/5fec79d0-cb45-4ce9-88bd-77036b15e987)
)
click yes to get directed to output folder
---

### 7. Viewing Results
- App automatically opens the generated `.srt` file  
- Subtitles are formatted as:
```srt
1
00:00:01,000 --> 00:00:04,000
This is your first subtitle line

2
00:00:05,500 --> 00:00:08,200
Second subtitle appears here
