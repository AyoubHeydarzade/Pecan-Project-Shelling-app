import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols

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
st.sidebar.title("📊 Pecan Project: Shelling Dataset Analysis Application")  
st.sidebar.header("🔧 Options")

# Upload dataset in the sidebar
uploaded_file = st.sidebar.file_uploader("📂 Upload a Dataset (Excel or CSV)", type=["xlsx", "csv"])

# --- MAIN PAGE: DATA ANALYSIS RESULTS ---
st.title("📊 Data Analysis Results")  

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

    # --- LEFT SIDEBAR: ANALYSIS OPTIONS ---
    st.sidebar.subheader("📊 Analysis Options")
    show_histogram = st.sidebar.checkbox("Show Histograms for Output Variables")
    show_pairplot = st.sidebar.checkbox("Show Pair Plots (Input & Output Variables)")
    perform_anova = st.sidebar.checkbox("Perform One-Way ANOVA Analysis")
    show_main_effects = st.sidebar.checkbox("Show Main Effects Plots")

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

        # Step 1: Show histograms if selected
        if show_histogram:
            st.subheader("📈 Histograms for Selected Output Variables")
            for var in output_variables:
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.histplot(output_data[var], bins=20, kde=True, ax=ax, color="blue")
                ax.set_title(f"Histogram of {var}")
                ax.set_xlabel(var)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)

        # Step 2: Show Pair Plot if selected
        if show_pairplot:
            st.subheader("📊 Pair Plot of Input & Output Variables")
            pairplot_data = df[input_variables + output_variables].dropna()  # Remove missing values

            if pairplot_data.empty:
                st.warning("⚠️ Not enough valid data for a pair plot. Please check your dataset.")
            else:
                pairplot_fig = sns.pairplot(pairplot_data)
                st.pyplot(pairplot_fig)

        # Step 3: Perform One-Way ANOVA if selected
        if perform_anova:
            st.subheader("📊 One-Way ANOVA Analysis")
            for response_var in output_variables:
                st.write(f"**ANOVA Results for {response_var}**")

                # Ensure relevant columns are numeric
                for col in input_variables + [response_var]:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                # Drop rows with missing values
                df_cleaned = df[input_variables + [response_var]].dropna()

                if df_cleaned.empty:
                    st.warning(f"⚠️ Not enough valid data for {response_var} after cleaning. Please check your dataset.")
                    continue

                # Define main effects model
                main_effects_formula = f'Q("{response_var}") ~ ' + " + ".join([f'C(Q("{var}"))' for var in input_variables])
                model = ols(main_effects_formula, data=df_cleaned).fit()
                anova_results = sm.stats.anova_lm(model, typ=2)
                st.write(anova_results)

        # Step 4: Show Main Effects Plots if selected
        if show_main_effects:
            st.subheader("📊 Main Effects Plots")
            for response_var in output_variables:
                st.write(f"**Main Effects Plots for {response_var}**")
                fig, ax = plt.subplots(len(input_variables), 1, figsize=(10, len(input_variables) * 5))

                for i, var in enumerate(input_variables):
                    if len(input_variables) > 1:
                        sns.boxplot(x=var, y=response_var, data=df, ax=ax[i])
                        ax[i].set_title(f"Effect of {var} on {response_var}")
                    else:
                        sns.boxplot(x=var, y=response_var, data=df, ax=ax)
                        ax.set_title(f"Effect of {var} on {response_var}")

                st.pyplot(fig)

    else:
        st.warning("⚠️ Please select at least one Input Variable and one Output Variable to proceed.")
