import streamlit as st
import pandas as pd

# Set up the Streamlit app title
st.title("📊 Simple Data Viewer App")

# Upload dataset
st.subheader("Upload a Dataset (Excel or CSV)")
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1]

    # Read the dataset based on file type
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Display dataset preview
    st.subheader("📋 Data Preview")
    st.write(df)

    # Display summary statistics
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

else:
    st.write("📌 Please upload a dataset to view the contents.")
