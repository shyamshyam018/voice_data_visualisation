import streamlit as st
import pyshorteners as pyst
import pyperclip
shortener=pyst.shortener()
def copying():
    pyperclip.copy(shorted_url)
st.markdown("<h1 style='text-align: center;'URL SHORTENER</h1>",unsafe_allow_html=True)
form=st.form("name")
url=form.text_input("URL HERE")
s_btn=form.form_submit_button("SHORT")
if s_btn:
    shortened_url=shortener.tinyurl.short(url)
    st.makrdown("<h3>Shorted Url</h3>" , unsafe_allow_html=True)
    st.markdown(f"<h6 style='text-align;center;'>{shorted_url}</h6>",unsafe_allow_html=True)
    st.button("Copy",on_click=copying)
