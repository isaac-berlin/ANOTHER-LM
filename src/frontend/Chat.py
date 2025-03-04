import streamlit as st
from components import chat_session

st.set_page_config(
    page_title="Chat",
    page_icon=":speech_balloon:"
)

st.title("myRAG Chatbot")

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

    # Generate assistant response (Replace with actual RAG retrieval later)
    response = f"You said: {prompt}. I'm here to help!"

    with st.chat_message("assistant"):
        st.markdown(response)

    active_chat["messages"].append({"role": "assistant", "content": response})