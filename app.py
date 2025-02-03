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

    # Predefined input and output variables
    predefined_input_variables = ["Gap between Rings (in)", "Tilt Angle (θ)", "Paddle Shaft RPM", "Drum RPM", "Moisture Level (%)"]
    predefined_output_variables = ["Intact Halves (%)", "Weight dist1. (%)", "Weight dist2. (%)", "Weight dist3. (%)", 
                                   "Discharge Throughput (lbs. %)", "Loss (%)"]

    # Step 1: Let users choose which input and output variables they have
    st.subheader("⚙️ Select Input & Output Variables")

    # Filter options based on what exists in the dataset
    available_input_variables = [var for var in predefined_input_variables if var in df.columns]
    available_output_variables = [var for var in predefined_output_variables if var in df.columns]

    # Let users select only from the filtered predefined lists
    input_variables = st.multiselect("Select Input Variables:", available_input_variables)
    output_variables = st.multiselect("Select Output Variables:", available_output_variables)

    # Ensure at least one input and one output variable is selected
    if input_variables and output_variables:
        filtered_data = df[input_variables + output_variables]
        st.subheader("📊 Filtered Data (Selected Input & Output Variables)")
        st.write(filtered_data)

        # Show summary statistics
        st.subheader("📊 Summary Statistics for Selected Variables")
        st.write(filtered_data.describe())

    else:
        st.warning("⚠️ Please select at least one Input Variable and one Output Variable to proceed.")
