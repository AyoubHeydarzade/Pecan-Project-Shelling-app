import streamlit as st
import pandas as pd

# App title
st.title("📊 Pecan Project: Shelling Dataset Analysis Application")

# Upload dataset
st.subheader("Upload a Dataset (Excel or CSV)")
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📋 Data Preview")
    st.write(df)

    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

