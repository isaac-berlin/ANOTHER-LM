import streamlit as st
import requests

API_URL = "placeholder"

def handle_uploaded_file(uploaded_file):
    # send the file to the server via a POST request
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(API_URL, files=files)

    # check if the request was successful
    if response.status_code == 200:
        st.success("File uploaded successfully!")
    else:
        st.error("Failed to upload file. Please try again.")