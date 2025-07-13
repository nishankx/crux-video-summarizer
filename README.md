# CRUX: The Ultimate Video Summarizer
#### Video Demo : https://youtu.be/F6NYITedhrM?si=FBWk3ImsD0sbtbrL

_CRUX is a minimal GUI tool using Python, designed to download, transcribe, and summarize long-form YouTube videos or uploaded media into crisp, structured insights. Whether it's a lecture, documentary, interview, or talk—CRUX extracts the essence, fast._

<img src="screenshots/Screenshot 2025-07-13 144539.png" width ="800" height ="350">

---

## 📌 Key Features

1. 🔗 YouTube Link Support\
Paste any public YouTube video link to begin.

2. 📁 Direct File Uploads\
 Use your own .mp4, .mp3, or .wav files.

3. 🧠 Accurate Transcription\
Uses OpenAI’s Whisper model for multilingual speech-to-text conversion.

4. ✍ Smart Summarization\
Choose from styles like: Bullet Digest (key takeaways), Outline (Chapter-wise summary) or Questions & Answers

5. 🖥 Dual Mode Support
   - Local Desktop Mode : \
Full access to private/age-restricted content using cookies.
   - Web Cloud Mode : \
Public video links or uploaded files only. Streamlit-powered interface.

6. ⬇️ Download Summary PDF ot Summary Audio\
After Summary is displayed, user can extract everything in a pdf file or through a audio clip of the summary using edge_tts

7. ⏱ Batch Input Handling\
Submit multiple links or files in a single session.

8. 🧭 Non-Editable History View\
All transcripts and summaries are logged but immutable, preserving reflection integrity.


<img src="screenshots/Screenshot 2025-07-13 172843.png" width ="800" height ="600">

---

# 🔧 Setup & Usage
1. Clone the Repo
```
git clone https://github.com/your-username/crux.git
```
2. Install Requirements
```
pip install -r requirements.txt
```
Make sure ffmpeg is installed and accessible via PATH.

3. Configure Environment
   Create a .env file:
```
OPENAI_API_KEY=your_openai_api_key
```
---

# 🎮 Running the App

### ✅ Local Desktop Mode

```
streamlit run main.py
```
Supports both:
  - YouTube links (including private/restricted via cookies)

  - Local video/audio files


### ☁ Web Cloud Mode (Public Access Only)

Deploy using:

  - Streamlit Cloud

  - GitHub Codespaces (file upload mode only)

---

# 📁 Project Structure

crux/ \
│\
├── main.py \
├── .env  \
├── requirements.txt \
└── README.md \

---

# 📈 Ideal For

+ Students summarizing long lectures

+ Researchers reviewing interviews or documentaries

+ Journalists parsing press conferences

+ Creators studying competitors’ content

+ Anyone trying to reclaim their time from 2-hour videos

---

# ❗ Known Limitations

- Local mode is required for age-restricted/private content.

- Cloud mode cannot bypass login-based videos.
---

# 🛠 Credits

- Transcription: Whisper by OpenAI

- Summarization: Google gemini

- Download: yt-dlp

- Conversion: ffmpeg

- Interface: Streamlit
---

# 📜 License
MIT License. Free for personal and educational use.

---
