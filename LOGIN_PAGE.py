import streamlit as st

# Set page title and icon
st.set_page_config(
    page_title="MULTI_PAGE_APP",
    page_icon="GLOBE"
)

# Define valid username and password
valid_username = "shyam"
valid_password = "shyam"

# Page title
st.image("assets\login.png")
st.subheader("LOGIN HERE")


# Username input
username = st.text_input("Username")

# Password input
password = st.text_input("Password", type="password")

# Login button
login_button = st.button("Login")

# Validate username and password
if login_button:
    if username == valid_username and password == valid_password:
        st.success("Login successful!")

    else:
        st.error("Invalid username or password. Please try again.")
