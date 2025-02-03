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

    # Define column categories
    initial_info_columns = ["Date", "Variety", "Batch Size (lb)", "Machine", "Exp. #"]
    input_variables = ["Gap between Rings (in)", "Tilt Angle (θ)", "Paddle Shaft RPM", "Drum RPM", "Moisture Level (%)"]
    output_variables = ["Intact Halves (%)", "Weight dist1. (%)", "Weight dist2. (%)", "Weight dist3. (%)",
                        "Discharge Throughput (lbs. %)", "Loss (%)"]

    # Filter the dataset to show only Input & Output variables
    filtered_columns = input_variables + output_variables
    filtered_data = df[filtered_columns] if all(col in df.columns for col in filtered_columns) else df

    st.subheader("📊 Filtered Data (Only Input & Output Variables)")
    st.write(filtered_data)

    st.subheader("📊 Summary Statistics")
    st.write(filtered_data.describe())
