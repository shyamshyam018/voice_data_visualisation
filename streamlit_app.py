# Libraries to be used
import streamlit as st
import requests
import json
import os

# Title and favicon
st.set_page_config(page_title="Speech to Text Transcription App", page_icon="👄")

# Logo and header
st.text("")
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://moodle.bitsathy.ac.in/pluginfile.php/1/theme_adaptable/logo/1658802280/bit-logo-text.png' width='400'>
    </div>
    """,
    unsafe_allow_html=True
)
st.title("Speech to text transcription app")

st.write("""  
- UPLOAD A WAV FILE OF YOUR SPEECH CONTAINING INPUT DATA AND TRANSCRIBE
- NOW YOU CAN VISUALISE YOUR DATA , HANDS FREE!
""")

st.text("")

c1, c2, c3 = st.columns([1, 4, 1])

with c2:
    with st.form(key="my_form"):
        f = st.file_uploader("", type=[".wav"])
        st.info("👆 Upload a .wav file")
        submit_button = st.form_submit_button(label="Transcribe")

if f is not None:
    st.audio(f, format="wav")
    path_in = f.name
    # Get file size from buffer
    old_file_position = f.tell()
    f.seek(0, os.SEEK_END)
    getsize = f.tell()
    f.seek(old_file_position, os.SEEK_SET)
    getsize = round((getsize / 1000000), 1)

    if getsize < 5:  # File more than 5 MB
        # To read file as bytes:
        bytes_data = f.getvalue()

        transcript = """
Thank you for choosing the Olympus Dictation Management System. The Olympus Dictation Management System gives you the power to manage your dictations, transcriptions, and documents seamlessly and to improve the productivity of your daily work. For example, you can automatically send the dictation files or transcribed documents to your assistant or the author via email or FTP. If you are using the speech recognition software, the speech recognition engine works in the background to support your document creation. We hope you enjoy the simple, flexible, reliable, and secure solution from Olympus.
"""

        st.info(transcript)

        st.download_button(
            "Download the transcription",
            transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

    else:
        st.warning("🚨 We've limited this demo to 5MB files. Please upload a smaller file.")
        st.stop()

else:
    path_in = None
    st.stop()
