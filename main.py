#---------------------------------------------------------IMPORTS------------------------------------------------------
import streamlit as st
import tempfile
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import yt_dlp
import whisper
import google.generativeai as genai
import asyncio
import edge_tts
from fpdf import FPDF
from io import BytesIO
import matplotlib.pyplot as plt
from wordcloud import WordCloud
#----------------------------------------------INITIATIONS---------------------------------------
load_dotenv()
genai.configure(api_key = os.getenv("API_KEY"))
global_temp_paths =[]
global_temp_dir = []
#-----------------------------------------TRANSCRIPTION------------------------------------------

def transcribe(audio_path):
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path)
    return result["text"]

def download_audio(url):
    try:
       with tempfile.TemporaryDirectory(delete=False) as tempdir:
        ydl_opts = {
        "format" : "worstaudio",
        "outtmpl" : os.path.join(tempdir,"audio.%(ext)s"),
        "postprocessors" : [{
            'key' : "FFmpegExtractAudio",
            'preferredcodec' : "mp3",
            'preferredquality' : "192",
        }],
        "quiet": True,
        "no_warnings": True
    }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            dir_path = os.path.join(tempdir,"audio.mp3")
            global_temp_dir.append(dir_path)
            return dir_path
    except yt_dlp.utils.DownloadError("Cookies can't be accessed. For URL USE the local desktop version."):
        st.success("Cookies can't be accessed. For URL USE the local desktop version.")

def get_metadata(url):
    ydl_opts={
        'quiet':True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url,download=True)
        thumbnail_url = info.get('thumbnail','')
        vd_title = info.get('title','Untitled')
        tags = info.get('tags',[])

        return {
            "title": vd_title,
            "thumbnail_url": thumbnail_url,
            "tags": tags,
        }

def get_file(file):
    if file is not None:
        suffix = "."+file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.getbuffer())
            tmp_path = tmp.name
            global_temp_paths.append(tmp_path)
            return tmp_path

def get_pdf(summary, title, thumbnail = None):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(family="Helvetica", style="B", size=18)
    pdf.set_text_color(128,0,128)
    pdf.cell(0,10,text=title,ln=True,align="C")
    pdf.ln(5)
    pdf.set_font(family="Helvetica", style="I", size=10)
    pdf.set_text_color(64,64,64)
    pdf.set_line_width(0.5)
    pdf.cell(0,10,f"Generated on:{datetime.now().strftime(r'%Y-%m-%d %H:%M:%S') }",ln=True)
    pdf.ln(5)
    if thumbnail:
        response = requests.get(thumbnail)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
            tmp_img.write(response.content)
            tmp_img_path = tmp_img.name
            global_temp_paths.append(tmp_img_path)
            pdf.image(tmp_img_path,h=80,w=160)
            pdf.ln(10)
    pdf.set_font(family="Helvetica", size=12)
    lines = summary.split("/n")
    for line in lines:
        pdf.multi_cell(0,10,line)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

#---------------------------------------------------PROCESSING--------------------------------------------

def summarize(transcript, style, num_points):
    prompt = f"""
    Summarize the following transcript into {num_points} most important {style}.
    Focus on high-level ideas, key facts, and important takeaways.
    Only return the {style}. No intro, no explanation.
    -------
    {transcript}
    """
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    lines = response.text.strip()
    return lines

async def echo(text, voice ="en-US-AriaNeural"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        filename = tmp_audio.name
        communicate = edge_tts.Communicate(text=text, voice=voice)
        global_temp_paths.append(filename)
        await communicate.save(filename)
    return filename

#----------------------------------------------------GRAPHICS-------------------------------------------
def show_tags(tags):
    if not tags:
        st.warning("No tags found.")
        return
    text =" ".join(tags)
    wc = WordCloud(width=800,height=400,background_color="#0E1117",colormap="viridis").generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

#------------------------------------------------------MAIN------------------------------------------------------

def main():
    st.set_page_config(
    page_title="CRUX",
    layout="centered",
    page_icon=":material/token:",
    initial_sidebar_state="expanded",
)
    st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bungee+Tint&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <img src="https://avatars.githubusercontent.com/u/210644959?v=4" alt="Nishan Kashyap" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; margin-bottom: 10px;"/>
                <h4 style="margin: 5px 0; font-size: 18px;">Made by Nishan Kashyap</h4>
                <p style="font-size: 20px; color: #888;">@nishankx</p>
                <a href="https://github.com/nishankx" target="_blank" style="text-decoration: none; font-size: 20px;"> GitHub </a>  |
                <a href="https://x.com/nishankx" target="_blank" style="text-decoration: none; font-size: 20px;"> X.com </a>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""<div style="text-align: center;">
                    <p>If you are in a Cloud/Codespace the URL's wont work due to authentication restrictions & cookie unavailability. Hence Consider using the desktop version.</p>
                    </div>""", unsafe_allow_html=True)
    st.markdown("""<h3 style="margin: 5px 0;font-family:'Bungee Tint',sans-serif; font-size: 220px;letter-spacing:0px ;text-align: center">CRUX</h3>""", unsafe_allow_html=True)
    st.markdown("*CRUX distills long-form content into clear, structured insights - fast." \
    " Upload a video file or an URL (from Youtube) and get clean summaries in **Bullet points**, **Chapters** "
    "or well structured **Question & Answers**.*")

    result = ""
    url = ""
    st.divider()
    ColX, ColY = st.columns(2)
    with ColX:
        typ = st.radio("What Are you Running Crux on?",["Desktop(Local)","Remote System/ Cloud/ Codespaces"])
    if typ =="Desktop(Local)":
        with ColY:
            input_type = st.radio("Choose Method",["Paste URL", "Upload File"])
    else:
        with ColY:
            input_type = st.radio("Choose Method",["Upload File"])
    st.divider()
    if input_type == "Paste URL":
        url = st.text_input("Paste URL")
    elif input_type == "Upload File":
        file = st.file_uploader("Upload File")
        audio_file = get_file(file)
    style = st.selectbox("Choose a Summary Style",["Bullet Points", "Chapter-Based Summary","Important Question & Answers"])
    num = st.number_input(f"How Many {style} you want? ", min_value=1, max_value=20)
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        aud = st.radio("Do you want the Summary Audio? ",["Yes", "No"])
    with col2:
        pd = st.radio("Do you want the Summary PDF? ",["Yes", "No"])
    st.divider()
    if st.button("Fetch & Summarize"):
        with st.spinner("Fetching Files..."):
            if input_type == "Paste URL":
                audio_file = download_audio(url)
                meta = get_metadata(url)
            transcript = transcribe(audio_file)
            st.success("Transcript Extracted")
            with st.expander("Transcript"):
                st.text_area(transcript)
            st.audio(audio_file)
        with st.spinner("Summarizing......"):
            result = summarize(transcript,style,num)
            st.success("Operation Complete")
            if input_type=="Paste URL":
                st.header(meta["title"])
                st.image(meta["thumbnail_url"])
            st.markdown(result)
        safe_text = result.encode("ascii","ignore").decode().replace("*","").replace("#","")
        if aud == "Yes":
            filename = "output.mp3"
            with st.spinner("Generating voice...."):
                filename = asyncio.run(echo(safe_text))
                with open(filename, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
        if pd =="Yes":
            with st.spinner("Generating PDF...."):
                if input_type =="Paste URL":
                    title = meta["title"]
                    pdf_bytes = get_pdf(safe_text, title,meta["thumbnail_url"])
                else:
                    title = "Crux Summary"
                    pdf_bytes = get_pdf(safe_text, title)
        if input_type =="Paste URL":
            show_tags(meta["tags"])

        if pd =="Yes":
            st.download_button(
                    label="Download Summary as PDF",
                    data=pdf_bytes,
                    file_name=f"{title}",
                    mime='application/pdf'
                )


        for path in global_temp_dir:
            os.remove(path)
        for path in global_temp_paths:
            os.remove(path)



if __name__=="__main__":
    main()
