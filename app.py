import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- FORCE SIDEBAR WIDTH ADJUSTMENT ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 400px !important;
        max-width: 450px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LEFT SIDEBAR: TITLE AND USER OPTIONS ---
st.sidebar.title("📊 Pecan Project: Shelling Dataset Analysis Application")  # Move the title to the sidebar
st.sidebar.header("🔧 Options")

# Upload dataset in the sidebar
uploaded_file = st.sidebar.file_uploader("📂 Upload a Dataset (Excel or CSV)", type=["xlsx", "csv"])

# --- MAIN PAGE: DATA ANALYSIS RESULTS ---
st.title("📊 Data Analysis Results")  # Show this title on the right side (main page)

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # --- LEFT SIDEBAR: VARIABLE SELECTION ---
    st.sidebar.subheader("⚙️ Select Variables")

    # Predefined input and output variables
    predefined_input_variables = ["Gap between Rings (in)", "Tilt Angle (θ)", "Paddle Shaft RPM", "Drum RPM", "Moisture Level (%)"]
    predefined_output_variables = ["Intact Halves (%)", "Weight dist1. (%)", "Weight dist2. (%)", "Weight dist3. (%)", 
                                   "Discharge Throughput (lbs. %)", "Loss (%)"]

    # Filter options based on what exists in the dataset
    available_input_variables = [var for var in predefined_input_variables if var in df.columns]
    available_output_variables = [var for var in predefined_output_variables if var in df.columns]

    # Let users select only from the filtered predefined lists
    input_variables = st.sidebar.multiselect("📥 Select Input Variables:", available_input_variables)
    output_variables = st.sidebar.multiselect("📤 Select Output Variables:", available_output_variables)

    # --- MAIN PAGE: DISPLAY RESULTS ---
    if input_variables and output_variables:
        # Display dataset preview
        st.subheader("📋 Data Preview")
        filtered_data = df[input_variables + output_variables]
        st.write(filtered_data)

        # Summary statistics for selected output variables
        st.subheader("📊 Summary Statistics for Selected Output Variables")
        output_data = df[output_variables]
        st.write(output_data.describe())

        # Step 2: Generate histograms for selected output variables
        st.subheader("📈 Histograms for Selected Output Variables")

        for var in output_variables:
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Plot histogram with blue color
            sns.histplot(output_data[var], bins=20, kde=True, ax=ax, color="blue")

            ax.set_title(f"Histogram of {var}")
            ax.set_xlabel(var)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        # Step 3: Pair Plot Between Input & Output Variables
        if len(input_variables) > 0 and len(output_variables) > 0:
            st.subheader("🔗 Pair Plot: Input Variables vs. Output Variables")
            input_output_data = df[input_variables + output_variables]  # Select input & output columns
            
            # Create and display the pair plot
            fig = sns.pairplot(input_output_data, diag_kind="kde", plot_kws={'alpha': 0.6})
            st.pyplot(fig)

        # Step 4: Pair Plot Between Output Variables
        if len(output_variables) > 1:
            st.subheader("🔗 Pair Plot: Output Variables vs. Output Variables")
            output_data = df[output_variables]  # Select output columns
            
            # Create and display the pair plot
            fig = sns.pairplot(output_data, diag_kind="kde", plot_kws={'alpha': 0.6})
            st.pyplot(fig)

    else:
        st.warning("⚠️ Please select at least one Input Variable and one Output Variable to proceed.")
