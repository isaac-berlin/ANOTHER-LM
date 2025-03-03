import streamlit as st
import pandas as pd
import uuid

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Chatbot", "File Upload", "About", "Settings"])

if page == "Chatbot":
    st.title("myRAG Chatbot")

    # Initialize session state for chat sessions
    if "chats" not in st.session_state:
        st.session_state.chats = {}  # Store chats as {uuid: {"name": "Default", "messages": []}}
    if "active_chat" not in st.session_state:
        # Automatically create and set a default chat session
        new_chat_id = str(uuid.uuid4())
        st.session_state.chats[new_chat_id] = {"name": "Default", "messages": []}
        st.session_state.active_chat = new_chat_id  # Track active chat by unique ID

    # Sidebar for chat sessions
    st.sidebar.subheader("Chat Sessions")

    chat_name = st.sidebar.text_input("Enter a new chat name:", placeholder="Chat name")

    if st.sidebar.button("Create Chat") and chat_name:
        new_chat_id = str(uuid.uuid4())  # Generate unique ID for each chat
        st.session_state.chats[new_chat_id] = {"name": chat_name, "messages": []}
        st.session_state.active_chat = new_chat_id  # Set new chat as active

    # Display existing chats and allow switching
    if st.session_state.chats:
        # Show chat names, but keep track of IDs
        chat_options = {chat_id: st.session_state.chats[chat_id]["name"] for chat_id in st.session_state.chats}
        
        selected_chat_id = st.sidebar.radio("Select a chat:", list(chat_options.keys()), format_func=lambda x: chat_options[x])

        if selected_chat_id:
            st.session_state.active_chat = selected_chat_id

        # Delete button for active chat
        if st.sidebar.button("Delete Chat") and st.session_state.active_chat:
            del st.session_state.chats[st.session_state.active_chat]
            
            # Automatically switch to another available chat or create a new one
            if st.session_state.chats:
                st.session_state.active_chat = next(iter(st.session_state.chats))  # Select first available chat
            else:
                # If all chats are deleted, create a new default chat
                new_chat_id = str(uuid.uuid4())
                st.session_state.chats[new_chat_id] = {"name": "Default", "messages": []}
                st.session_state.active_chat = new_chat_id

            st.rerun()  # Refresh UI

    # Retrieve active chat details
    active_chat = st.session_state.chats.get(st.session_state.active_chat, None)

    if active_chat:
        # Display previous messages
        for message in active_chat["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Get user input
        if prompt := st.chat_input("What is up?"):
            active_chat["messages"].append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                response = f"You said: {prompt}. I'm here to help!"
                st.markdown(response)

            active_chat["messages"].append({"role": "assistant", "content": response})


elif page == "File Upload":
    st.title("Upload Multiple Documents for RAG")

    uploaded_files = st.file_uploader("Upload multiple documents (PDF, TXT, CSV)", 
                                      type=["pdf", "txt", "csv"], 
                                      accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.success(f"Uploaded: {uploaded_file.name}")

            # Process text files
            if uploaded_file.type == "text/plain":
                text = uploaded_file.read().decode("utf-8")
                st.text_area(f"Content of {uploaded_file.name}", text, height=150)

            # Process PDFs (Basic Placeholder - Add PDF parsing here)
            elif uploaded_file.type == "application/pdf":
                st.write(f"PDF processing for {uploaded_file.name} coming soon!")

            # Process CSV files
            elif uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
                st.write(f"Preview of {uploaded_file.name}:")
                st.dataframe(df)  # Display CSV content

elif page == "About":
    st.title("About This App")
    st.write("This is a simple Retrieval-Augmented Generation (RAG) platform built using Streamlit.")

elif page == "Settings":
    st.title("Settings")
    st.write("You can configure RAG settings here in the future.")
