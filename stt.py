import streamlit as st
from pydub import AudioSegment, silence

st.markdown("<h1 style='text-align:center;'>AUDIO TO TEXT</h1>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

audio = st.file_uploader("UPLOAD YOUR AUDIO FILE", type=['mp3', 'wav'])

if audio:
    audio_segment = AudioSegment.from_file(audio)
    chunks = silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS - 20,
                                      keep_silence=100)
