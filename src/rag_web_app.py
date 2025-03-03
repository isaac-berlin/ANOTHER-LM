import streamlit as st
import pandas as pd

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Chatbot", "File Upload", "About", "Settings"])

if page == "Chatbot":
    st.title("Multi-Session Chatbot")

    # Initialize session state for chat sessions
    if "chats" not in st.session_state:
        st.session_state.chats = {}  # Dictionary to hold multiple chats
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = None  # Currently selected chat session

    # Create or select a chat session
    st.sidebar.subheader("Chat Sessions")
    chat_name = st.sidebar.text_input("Enter a new chat name:", placeholder="Chat 1")
    
    if st.sidebar.button("Create Chat") and chat_name:
        if chat_name not in st.session_state.chats:
            st.session_state.chats[chat_name] = []  # Initialize empty chat history
            st.session_state.active_chat = chat_name  # Set new chat as active
        else:
            st.sidebar.warning("Chat name already exists!")

    # List existing chats and allow switching
    if st.session_state.chats:
        selected_chat = st.sidebar.radio("Select a chat:", list(st.session_state.chats.keys()), key="chat_selector")

        if selected_chat:
            st.session_state.active_chat = selected_chat

        # Add delete button for active chat
        if st.sidebar.button("Delete Chat") and st.session_state.active_chat:
            del st.session_state.chats[st.session_state.active_chat]
            st.session_state.active_chat = None  # Reset active chat
            st.rerun()  # Refresh the page to update sidebar

    if not st.session_state.active_chat:
        st.write("Start a new chat from the sidebar.")
    else:
        st.subheader(f"Chat: {st.session_state.active_chat}")

        # Retrieve chat history for the active chat
        chat_history = st.session_state.chats[st.session_state.active_chat]

        # Display previous messages
        for message in chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Get user input
        if prompt := st.chat_input("What is up?"):
            chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                response = f"You said: {prompt}. I'm here to help!"
                st.markdown(response)

            chat_history.append({"role": "assistant", "content": response})

            # Debug: Print chat history
            print(f"\n[DEBUG] Chat '{st.session_state.active_chat}' History:")
            print(chat_history)

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
