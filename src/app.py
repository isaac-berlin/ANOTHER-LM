import streamlit as st
from pages import chatbot, file_upload, about, settings

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Chatbot", "File Upload", "About", "Settings"])

if page == "Chatbot":
    chatbot.show()
elif page == "File Upload":
    file_upload.show()
elif page == "About":
    about.show()
elif page == "Settings":
    settings.show()
