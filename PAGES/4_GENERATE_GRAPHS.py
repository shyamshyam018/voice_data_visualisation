import streamlit as st
import pandas as pd
import speech_recognition as sr
import pyttsx3
from streamlit_echarts import st_echarts


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        st.warning("No speech detected.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service: {e}")
    return ""


def text_to_speech(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


def generate_pie_chart(data, column_name):
    st.header(f"Pie Chart for '{column_name}'")
    options = {
        "title": {"text": f"Pie Chart for '{column_name}'", "subtext": "Purely fictional", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [
            {
                "name": column_name,
                "type": "pie",
                "radius": "50%",
                "data": [{"value": val, "name": index} for index, val in data[column_name].value_counts().items()],
                "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}},
            }
        ],
    }
    st_echarts(options=options, height="600px")
    text_to_speech("Pie chart generated!")


def generate_bar_chart(data, column_x, y_column):
    st.header(f"Bar Chart for '{column_x}' and '{y_column}'")
    options = {
        "xAxis": {"type": "category", "data": data[column_x].tolist()},
        "yAxis": {"type": "value"},
        "series": [{"data": data[y_column].tolist(), "type": "bar"}]
    }
    st_echarts(options=options, height="500px")
    text_to_speech("Bar chart generated!")


def generate_area_chart(data, column_x, y_column):
    st.header(f"Area Chart for '{column_x}' and '{y_column}'")
    options = {
        "xAxis": {"type": "category", "boundaryGap": False, "data": data[column_x].tolist()},
        "yAxis": {"type": "value"},
        "series": [{"data": data[y_column].tolist(), "type": "line", "areaStyle": {}}]
    }
    st_echarts(options=options, height="500px")
    text_to_speech("Area chart generated!")


def generate_scatter_chart(data, column_x, y_column):
    st.header(f"Scatter Chart for '{column_x}' and '{y_column}'")
    options = {
        "xAxis": {},
        "yAxis": {},
        "series": [{"symbolSize": 20, "data": data[[column_x, y_column]].values.tolist(), "type": "scatter"}]
    }
    st_echarts(options=options, height="500px")
    text_to_speech("Scatter chart generated!")


def find_numeric_column(data, exclude_column=None):
    columns = data.columns
    for column in columns:
        if column.lower().replace("_", " ") != exclude_column.lower().replace("_", " ") and data[column].dtype in [int, float]:
            return column
    return None


def main():
    st.title("Voice-Enabled Chatbot")

    # User input
    user_input = st.text_input("You:")
    speech_input_button = st.button("Speak")

    # Convert speech input to text
    if speech_input_button:
        user_input = speech_to_text()
        st.text_input("You:", user_input)  # Display the recognized text

    # Generate visualization
    if user_input:
        st.write(f"Generating your visualization...")
        text_to_speech(f"Generating your visualization...")

        if uploaded_file is not None:
            st.success("File uploaded successfully!")
            data = pd.read_csv(uploaded_file)

            if user_input.startswith("generate pie chart for"):
                column_name = user_input.split("generate pie chart for")[1].strip()
                column_name = column_name.replace("_", " ").lower()
                if column_name in data.columns:
                    generate_pie_chart(data, column_name)
                else:
                    st.error(f"Column '{column_name}' does not exist in the data.")

            elif user_input.startswith("generate bar chart for"):
                column_names = user_input.split("generate bar chart for")[1].strip().split(" and ")
                if len(column_names) == 2:
                    column_x, y_column = column_names
                    column_x = column_x.replace("_", " ").lower()
                    y_column = y_column.replace("_", " ").lower()
                    if column_x in data.columns and y_column in data.columns:
                        generate_bar_chart(data, column_x, y_column)
                    else:
                        st.error("One or both of the specified columns do not exist in the data.")
                else:
                    st.error("Please specify both X and Y columns for the bar chart.")

            elif user_input.startswith("generate area chart for"):
                column_names = user_input.split("generate area chart for")[1].strip().split(" and ")
                if len(column_names) == 2:
                    column_x, y_column = column_names
                    column_x = column_x.replace("_", " ").lower()
                    y_column = y_column.replace("_", " ").lower()
                    if column_x in data.columns and y_column in data.columns:
                        generate_area_chart(data, column_x, y_column)
                    else:
                        st.error("One or both of the specified columns do not exist in the data.")
                else:
                    st.error("Please specify both X and Y columns for the area chart.")

            elif user_input.startswith("generate scatter chart for"):
                column_names = user_input.split("generate scatter chart for")[1].strip().split(" and ")
                if len(column_names) == 2:
                    column_x, y_column = column_names
                    column_x = column_x.replace("_", " ").lower()
                    y_column = y_column.replace("_", " ").lower()
                    if column_x in data.columns and y_column in data.columns:
                        generate_scatter_chart(data, column_x, y_column)
                    else:
                        st.error("One or both of the specified columns do not exist in the data.")
                else:
                    st.error("Please specify both X and Y columns for the scatter chart.")

            else:
                st.error("Invalid visualization command.")

            st.write("Visualization generated!")
            text_to_speech("Here is the generated visualization!")
        else:
            st.warning("Please upload a CSV file.")


if __name__ == "__main__":
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.write("Please upload a CSV file:")
    uploaded_file = st.file_uploader("Choose a CSV file")

    if uploaded_file is not None:
        main()
