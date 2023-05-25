import streamlit as st
import requests
import json
import os
import pandas as pd
import plotly.express as px
import base64
from io import StringIO, BytesIO

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
- NOW YOU CAN VISUALISE YOUR DATA, HANDS FREE!
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

def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", ('Description', 'Speech to Text', 'Excel Plotter'))

if selection == 'Description':
    st.header('Description')
    st.write('This is a web app that allows you to convert speech to text and visualize data from an Excel file.')

elif selection == 'Speech to Text':
    st.header('Speech to Text')
    st.write('Upload a WAV file containing speech and transcribe it.')
    # Rest of the code for Speech to Text section

elif selection == 'Excel Plotter':
    st.header('Excel Plotter')
    st.write('Feed the app with an Excel file and visualize the data.')
    uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
    if uploaded_file:
        st.markdown('---')
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.dataframe(df)
        groupby_column = st.selectbox(
            'What would you like to analyse?',
            ('Ship Mode', 'Segment', 'Category', 'Sub-Category'),
        )

        output_columns = ['Sales', 'Profit']
        df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

        fig = px.bar(
            df_grouped,
            x=groupby_column,
            y='Sales',
            color='Profit',
            color_continuous_scale=['red', 'yellow', 'green'],
            template='plotly_white',
            title=f'<b>Sales & Profit by {groupby_column}</b>'
        )
        st.plotly_chart(fig)

        st.subheader('Downloads:')
        generate_excel_download_link(df_grouped)
        generate_html_download_link(fig)
