import streamlit as st
import pandas as pd
from components import file_processing

def show():
    st.title("Upload Multiple Documents for RAG")
    
    uploaded_files = st.file_uploader("Upload multiple documents (PDF, TXT, CSV)", 
                                      type=["pdf", "txt", "csv"], 
                                      accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_processing.handle_uploaded_file(uploaded_file)
