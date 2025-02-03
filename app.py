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

    # Step 1: Let users choose which columns are input and output variables
    st.subheader("⚙️ Select Input & Output Variables")

    # Let users select input variables from the dataset
    input_variables = st.multiselect("Select Input Variables:", df.columns)

    # Let users select output variables from the dataset
    output_variables = st.multiselect("Select Output Variables:", df.columns)

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
