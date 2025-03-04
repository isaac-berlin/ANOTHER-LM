import streamlit as st
import requests

API_URL = "http://localhost:8000/upload"

def handle_uploaded_files(uploaded_files):
    """Handles multiple file uploads and aborts if any fails."""
    
    for uploaded_file in uploaded_files:
        if not hasattr(uploaded_file, "name"):  # Ensure it's an UploadedFile object
            st.error("Invalid file format. Aborting upload.")
            return
        
        st.write(f"Uploading: {uploaded_file.name}...")

        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

        try:
            response = requests.post(API_URL, files=files)
            response.raise_for_status()  # Raises exception for HTTP 4xx/5xx errors
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Upload failed for {uploaded_file.name}: {e}")
            return

        # If upload succeeds
        if response.status_code == 200:
            st.success(f"✅ Uploaded successfully: {uploaded_file.name}")
            st.json(response.json())  # Show server response
        else:
            st.error(f"⚠️ Server error ({response.status_code}) for {uploaded_file.name}")
            return
