import streamlit as st
import uuid
from components import chat_session

st.set_page_config(
    page_title="Chat",
)

st.title("myRAG Chatbot")

chat_session.initialize_chat()

# Sidebar for chat sessions
chat_session.sidebar_controls()

# Retrieve active chat session
active_chat = chat_session.get_active_chat()

if active_chat:
    for message in active_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    if prompt := st.chat_input("What is up?"):
        active_chat["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            response = f"You said: {prompt}. I'm here to help!"
            st.markdown(response)

        active_chat["messages"].append({"role": "assistant", "content": response})
