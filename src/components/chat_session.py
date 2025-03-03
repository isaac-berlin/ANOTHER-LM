import streamlit as st
import uuid

def initialize_chat():
    if "chats" not in st.session_state:
        st.session_state.chats = {}  
    if "active_chat" not in st.session_state:
        new_chat_id = str(uuid.uuid4())
        st.session_state.chats[new_chat_id] = {"name": "Default", "messages": []}
        st.session_state.active_chat = new_chat_id

def sidebar_controls():
    st.sidebar.subheader("Chat Sessions")
    chat_name = st.sidebar.text_input("Enter a new chat name:", placeholder="Chat name")

    if st.sidebar.button("Create Chat") and chat_name:
        new_chat_id = str(uuid.uuid4())
        st.session_state.chats[new_chat_id] = {"name": chat_name, "messages": []}
        st.session_state.active_chat = new_chat_id

    if st.session_state.chats:
        chat_options = {chat_id: st.session_state.chats[chat_id]["name"] for chat_id in st.session_state.chats}
        selected_chat_id = st.sidebar.radio("Select a chat:", list(chat_options.keys()), format_func=lambda x: chat_options[x])

        if selected_chat_id:
            st.session_state.active_chat = selected_chat_id

        if st.sidebar.button("Delete Chat"):
            del st.session_state.chats[st.session_state.active_chat]
            if st.session_state.chats:
                st.session_state.active_chat = next(iter(st.session_state.chats))
            else:
                new_chat_id = str(uuid.uuid4())
                st.session_state.chats[new_chat_id] = {"name": "Default", "messages": []}
                st.session_state.active_chat = new_chat_id
            st.rerun()

def get_active_chat():
    return st.session_state.chats.get(st.session_state.active_chat, None)
