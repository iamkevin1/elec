import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# Streamlit setup
st.set_page_config(page_title="Electricity Reading", layout="centered")
st.title("⚡ Electricity Reading and Analyzer")

st.header("📤 Upload Electricity Reading")

# Optional image upload
uploaded_image = st.file_uploader("Upload meter image (optional)", type=["png", "jpg", "jpeg"])

# kWh reading input
reading = st.number_input("Enter reading (in kWh)", min_value=0.0, format="%.2f")

# Date and time input
date_input = st.date_input("Select the date of reading")
time_input = st.time_input("Select the time of reading (12-hour format)")

# Submit button
if st.button("Submit Reading"):
    if reading and date_input and time_input:
        # Combine date and time, localize to India
        naive_timestamp = datetime.combine(date_input, time_input)
        india = pytz.timezone("Asia/Kolkata")
        localized_timestamp = india.localize(naive_timestamp)

        # Format for display
        display_time = localized_timestamp.strftime("%d-%m-%Y %I:%M %p")
        st.success(f"✅ Reading recorded at: {display_time}")

        # Save to CSV
        new_data = pd.DataFrame({
            "Reading (kWh)": [reading],
            "Timestamp (IST)": [localized_timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")]
        })

        file_path = "readings.csv"
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path)
            df = pd.concat([df_existing, new_data], ignore_index=True)
        else:
            df = new_data

        df.to_csv(file_path, index=False)
        st.success("✅ Reading saved successfully!")
    else:
        st.warning("Please fill in all fields before submitting.")

# View all readings
st.header("📋 All Recorded Readings")
file_path = "readings.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.dataframe(df)
else:
    st.info("No readings available yet.")
