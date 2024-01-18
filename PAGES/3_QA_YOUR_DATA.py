from typing import Literal
import streamlit as st
import sqlalchemy
import pandas as pd
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabase
import speech_recognition as sr
import pyttsx3
from langchain_experimental.sql import SQLDatabaseChain

load_dotenv()


@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str


def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "db_chain" not in st.session_state:
        llm = OpenAI(temperature=0)
        db = SQLDatabase(engine)
        st.session_state.db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)


def speech_to_text():
    global recording
    try:
        r = sr.Recognizer()  # Initialize the recognizer
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            st.write("Listening...")
            audio = r.listen(source)

        text = r.recognize_google(audio)
        st.session_state.human_prompt = text

        # Trigger the query execution
        on_click_callback()

    except sr.UnknownValueError:
        st.warning("No speech detected.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service: {e}")


def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # You can adjust the speech rate here

    # Iterate over each message in the chat history
    for chat in text:
        if chat.origin == "ai":
            engine.say(chat.message)
            engine.runAndWait()


def on_click_callback():
    query = st.session_state.human_prompt

    if query:
        st.session_state.history.append(Message("human", query))

        # Execute the query and display the output
        with st.spinner("Running the query..."):
            output = st.session_state.db_chain.run(query)
        st.success("Query executed successfully!")

        st.session_state.history.append(Message("ai", output))

        # Speak the generated answer
        speak_text([Message("ai", output)])

        # Clear the human_prompt value
        st.session_state.human_prompt = ""

        # Update the chat display with the new message
        chat_placeholder.empty()
        with chat_placeholder:
            for chat in st.session_state.history:
                div = f"""
                <div class="chat-row {'row-reverse' if chat.origin == 'human' else ''}">
                    <img class="chat-icon" src="app/static/{'ai_icon.png' if chat.origin == 'ai' else 'user_icon.png'}" width=32 height=32>
                    <div class="chat-bubble {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                        &#8203;{chat.message}
                    </div>
                </div>
                """
                st.markdown(div, unsafe_allow_html=True)

            for _ in range(3):
                st.markdown("")


def display_database():
    if database_url and table_name:
        try:
            engine = sqlalchemy.create_engine(database_url)
            query = f"SELECT * FROM {table_name} LIMIT 10"
            df = pd.read_sql(query, engine)
            st.sidebar.subheader("Database Preview")
            st.sidebar.write(df)
        except sqlalchemy.exc.SQLAlchemyError as e:
            st.sidebar.error(f"Error: {e}")
    else:
        st.sidebar.info("Please enter the database URL and table name.")


load_css()

# MySQL database URL
database_url = st.text_input("Database URL")
table_name = st.text_input("Table Name")

# Connect to the database using the provided URL
engine = sqlalchemy.create_engine(database_url)

initialize_session_state()

st.title("SQL Query Bot 🤖")

chat_placeholder = st.container()

# Rest of the code remains the same

def add_to_chat(message):
    st.session_state.history.append(message)

def stop_recording():
    global recording
    recording = False


with chat_placeholder:
    for chat in st.session_state.history:
        # Define emojis for AI and human
        ai_emoji = "🤖"
        human_emoji = "👤"

        div = f"""
        <div class="chat-row {'row-reverse' if chat.origin == 'human' else ''}">
            <span class="chat-icon">{ai_emoji if chat.origin == 'ai' else human_emoji}</span>
            <div class="chat-bubble {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                &#8203;{chat.message}
            </div>
        </div>
        """
        st.markdown(div, unsafe_allow_html=True)

    for _ in range(3):
        st.markdown("")


# Create the UI components
record_btn = st.button(":microphone: - ASK YOUR QUERY ")

# Button click handlers
if record_btn:
    speech_to_text()
    
display_database()
