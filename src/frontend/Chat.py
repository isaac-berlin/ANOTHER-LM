import streamlit as st
import requests
import json
from components import chat_session
import os

st.set_page_config(
    page_title="Chat",
    page_icon=":speech_balloon:"
)

st.title("myRAG Chatbot")

url_base = os.getenv("API_URL", "http://localhost:8000")
API_URL = f"{url_base}/query"

# Initialize chat sessions
chat_session.initialize_chat()

# Sidebar controls for managing chat sessions
chat_session.sidebar_controls()

# Retrieve active chat session, ensuring one always exists
active_chat = chat_session.get_active_chat()

# Display chat messages
if active_chat:
    for message in active_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    if not active_chat:
        active_chat = chat_session.get_active_chat()  # Ensure a chat exists

    active_chat["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        source = None
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": prompt})
                if response.status_code == 200:
                    print(response.json())
                    rag_response = response.json().get("response")
                    source = response.json().get("sources")
                else:
                    rag_response = "Error: Failed to retrieve response."
            except requests.exceptions.RequestException as e:
                rag_response = f"API request failed: {str(e)}"
                
        st.markdown(rag_response)
        if source:
            st.markdown(f"Source: {source}")

    active_chat["messages"].append({"role": "assistant", "content": rag_response})