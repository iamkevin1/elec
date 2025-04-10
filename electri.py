import streamlit as st
import pandas as pd
import datetime
import pytz
import plotly.express as px
import os

# Set IST timezone
IST = pytz.timezone("Asia/Kolkata")

# Streamlit Page Config
st.set_page_config(page_title="Electricity Analyzer", layout="centered")
st.title("⚡ Electricity Reading and Analyzer")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📥 Upload Reading", "📋 View Data", "📈 Analyze", "🔌 Appliances"])

# 1. Upload Tab
with tab1:
    st.header("📥 Upload Electricity Reading")

    uploaded_image = st.file_uploader("Upload meter image", type=["jpg", "png", "jpeg"])
    reading = st.number_input("Enter reading (in kWh)", step=0.1)

    # Date Input
    date = st.date_input("Enter Date", datetime.datetime.now(IST).date())

    # Manual time input
    time_input_str = st.text_input("Enter time (e.g., 03:45 PM)", value="06:00 PM")

    try:
        time_obj = datetime.datetime.strptime(time_input_str, "%I:%M %p").time()
        timestamp = datetime.datetime.combine(date, time_obj)
        timestamp = IST.localize(timestamp)
    except ValueError:
        st.warning("⚠️ Invalid time format. Use format like 04:30 PM")
        timestamp = None

    if st.button("💾 Save Reading") and timestamp:
        data = {"timestamp": [timestamp.isoformat()], "reading": [reading]}
        df = pd.DataFrame(data)

        if os.path.exists("readings.csv"):
            df_old = pd.read_csv("readings.csv")
            df_all = pd.concat([df_old, df], ignore_index=True)
        else:
            df_all = df

        df_all.to_csv("readings.csv", index=False)
        st.success("✅ Reading saved successfully!")

# 2. View Data Tab
with tab2:
    st.header("📋 All Recorded Readings")

    if os.path.exists("readings.csv"):
        df = pd.read_csv("readings.csv")

        # Parse timestamp correctly
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert("Asia/Kolkata")
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %I:%M %p")  # AM/PM format
        st.dataframe(df.sort_values("timestamp", ascending=False))
    else:
        st.info("No readings yet. Please upload one.")

# 3. Analysis Tab
with tab3:
    st.header("📈 Analyze Consumption")

    if os.path.exists("readings.csv"):
        df = pd.read_csv("readings.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert("Asia/Kolkata")
        df = df.sort_values("timestamp")
        df["diff_kWh"] = df["reading"].diff()
        df["date"] = df["timestamp"].dt.date

        st.plotly_chart(px.line(df, x="timestamp", y="reading", title="📊 Total Reading Over Time"))
        st.plotly_chart(px.bar(df, x="date", y="diff_kWh", title="🔋 Daily Consumption"))
    else:
        st.info("No data available yet.")

# 4. Appliance Estimator Tab
with tab4:
    st.header("🔌 Appliance Usage Estimator")

    appliance = st.text_input("Appliance name")
    wattage = st.number_input("Power rating (Watts)", step=10)
    hours = st.number_input("Usage per day (hours)", step=0.5)

    if st.button("⚙️ Estimate Usage"):
        if appliance and wattage > 0 and hours > 0:
            kwh = (wattage * hours) / 1000
            st.success(f"{appliance} consumes approx. {kwh:.2f} kWh/day")
        else:
            st.warning("Fill all details correctly.")
