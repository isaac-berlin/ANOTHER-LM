import streamlit as st
import uuid

def initialize_chat():
    """Initialize chat sessions if not already set up."""
    if "chats" not in st.session_state:
        st.session_state.chats = {}

    # Ensure an active chat always exists
    if "active_chat" not in st.session_state or not st.session_state.chats:
        create_new_chat("Default")

def create_new_chat(name):
    """Create a new chat session and set it as active."""
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats[new_chat_id] = {"name": name, "messages": []}
    st.session_state.active_chat = new_chat_id

def delete_active_chat():
    """Deletes the active chat and creates a new one if needed."""
    if "active_chat" in st.session_state:
        del st.session_state.chats[st.session_state.active_chat]

    if not st.session_state.chats:  # If all chats were deleted, create a new one
        create_new_chat("Default")
    else:
        st.session_state.active_chat = next(iter(st.session_state.chats))  # Set first available chat as active

    st.rerun()  # Refresh UI after deletion

def sidebar_controls():
    """Handles sidebar UI for managing chat sessions."""
    st.sidebar.subheader("Chat Sessions")

    # Create a new chat session
    chat_name = st.sidebar.text_input("Enter a new chat name:", placeholder="Chat name")

    if st.sidebar.button("Create Chat") and chat_name:
        create_new_chat(chat_name)
        st.rerun()  # Refresh UI after creation

    if st.session_state.chats:
        chat_options = {chat_id: st.session_state.chats[chat_id]["name"] for chat_id in st.session_state.chats}
        selected_chat_id = st.sidebar.radio("Select a chat:", list(chat_options.keys()), format_func=lambda x: chat_options[x])

        if selected_chat_id:
            st.session_state.active_chat = selected_chat_id

        # Delete chat button
        if st.sidebar.button("Delete Chat"):
            delete_active_chat()  # Properly delete and refresh

def get_active_chat():
    """Retrieve the active chat session."""
    return st.session_state.chats.get(st.session_state.active_chat, None)
