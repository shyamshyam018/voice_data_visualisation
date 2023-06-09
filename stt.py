import streamlit as st
from pydub import AudioSegment, silence
import speech_recognition as sr

recog = sr.Recognizer()
final_result = ""

st.markdown("<h1 style='text-align:center;'>AUDIO TO TEXT</h1>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

audio = st.file_uploader("UPLOAD YOUR AUDIO FILE", type=['mp3', 'wav'])

if audio:
    audio_segment = AudioSegment.from_file(audio)
    chunks = silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS - 20,
                                      keep_silence=100)
    for index, chunk in enumerate(chunks):
        chunk.export(str(index) + ".wav", format="wav")
        with sr.AudioFile(str(index) + ".wav") as source:
            recorded = recog.record(source)
            try:
                text = recog.recognize_google(recorded)
                final_result += text
                st.write(text)
            except:
                st.write("None")
                final_result += "Unaudible"
    st.text_area("", value=final_result)
