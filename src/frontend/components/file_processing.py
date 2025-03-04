import streamlit as st
import pandas as pd

def handle_uploaded_file(uploaded_file):
    st.success(f"Uploaded: {uploaded_file.name}")

    if uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
        st.text_area(f"Content of {uploaded_file.name}", text, height=150)

    elif uploaded_file.type == "application/pdf":
        st.write(f"PDF processing for {uploaded_file.name} coming soon!")

    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.write(f"Preview of {uploaded_file.name}:")
        st.dataframe(df)
