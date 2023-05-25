# Libraries to be used
import streamlit as st
import requests
import json
import os

# Title and favicon
st.set_page_config(page_title="Speech to Text Transcription App", page_icon="👄")

# Logo and header
st.title("Speech to text transcription app")
st.markdown("---")
st.write("""  
- Upload a wav file, transcribe it, then export it to a text file!
- Use cases: call centres, team meetings, training videos, school calls etc.
""")

# Center-align the image
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
    st.image("https://emojipedia-us.s3.amazonaws.com/source/skype/289/parrot_1f99c.png", width=125)
    st.markdown('</div>', unsafe_allow_html=True)

# File upload and transcription
st.markdown("---")
with st.form(key="my_form"):
    file = st.file_uploader("Upload a .wav file", type=[".wav"])
    submit_button = st.form_submit_button("Transcribe")

if file is not None:
    st.audio(file, format="wav")
    file_size = round(file.size / 1000000, 1)

    if file_size < 5:
        # To read file as bytes:
        bytes_data = file.read()

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

else:
    st.stop()
