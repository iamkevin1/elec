import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

st.set_page_config(page_title="Electricity Reading and Analyzer", layout="centered")
st.title("⚡ Electricity Reading and Analyzer")

st.header("📤 Upload Electricity Reading")

# Upload image (optional)
uploaded_image = st.file_uploader("Upload meter image", type=["png", "jpg", "jpeg"])

# Enter kWh reading
reading = st.number_input("Enter reading (in kWh)", min_value=0.0, format="%.2f")

# Manually select date and time
date_input = st.date_input("Select date of reading")
time_input = st.time_input("Select time of reading (12-hour with AM/PM)")

# Save button
if st.button("Submit Reading"):
    if reading and date_input and time_input:
        # Combine date and time
        timestamp = datetime.combine(date_input, time_input)

        # Convert to Asia/Kolkata timezone
        india = pytz.timezone("Asia/Kolkata")
        timestamp = india.localize(timestamp)

        # Format display time
        display_time = timestamp.strftime("%d-%m-%Y %I:%M %p")
        st.success(f"Reading recorded at: {display_time}")

        # Save to CSV
        new_data = pd.DataFrame({
            "reading": [reading],
            "timestamp": [timestamp.isoformat()]
        })

        file_path = "readings.csv"
        if os.path.exists(file_path):
            existing = pd.read_csv(file_path)
            df = pd.concat([existing, new_data], ignore_index=True)
        else:
            df = new_data

        df.to_csv(file_path, index=False)
        st.success("Reading saved successfully.")
    else:
        st.warning("Please fill out all fields before submitting.")

# View all readings
st.header("📋 All Recorded Readings")

file_path = "readings.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    # Safely parse datetime and convert to IST
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Kolkata")
    df["Time (IST)"] = df["timestamp"].dt.strftime("%d-%m-%Y %I:%M %p")

    st.dataframe(df[["reading", "Time (IST)"]])
else:
    st.info("No readings recorded yet.")
