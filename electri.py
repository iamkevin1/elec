import streamlit as st
import pandas as pd
import datetime
import pytz
import plotly.express as px
import os

# Set Indian Standard Time (IST)
IST = pytz.timezone("Asia/Kolkata")

# App title
st.set_page_config(page_title="Electricity Analyzer", layout="centered")
st.title("⚡ Electricity Reading and Analyzer")

# Tabs for interface
tab1, tab2, tab3, tab4 = st.tabs(["📥 Upload Reading", "📋 View Data", "📈 Analyze", "🔌 Appliances"])

# 1. Upload Reading
with tab1:
    st.header("Upload Electricity Reading")
    
    uploaded_image = st.file_uploader("Upload meter image", type=["png", "jpg", "jpeg"])
    reading = st.number_input("Enter reading (in kWh)", step=0.1)

    # Time input in IST with AM/PM format
    ist_now = datetime.datetime.now(IST)
    date = st.date_input("Select date", ist_now.date())
    time = st.time_input("Select time (AM/PM format)", ist_now.time())  # 12-hour input
    timestamp = datetime.datetime.combine(date, time)
    timestamp = IST.localize(timestamp)

    if st.button("💾 Save Reading"):
        data = {"timestamp": [timestamp.isoformat()], "reading": [reading]}
        df = pd.DataFrame(data)

        # Save to CSV
        if os.path.exists("readings.csv"):
            df_old = pd.read_csv("readings.csv")
            df_all = pd.concat([df_old, df], ignore_index=True)
        else:
            df_all = df

        df_all.to_csv("readings.csv", index=False)
        st.success("✅ Reading saved successfully!")

# 2. View Data
with tab2:
    st.header("📋 All Recorded Readings")
    if os.path.exists("readings.csv"):
        df = pd.read_csv("readings.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert("Asia/Kolkata")
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %I:%M %p")  # 12-hour format with AM/PM
        st.dataframe(df.sort_values("timestamp", ascending=False))

# 3. Analyze
with tab3:
    st.header("📈 Analyze Consumption")
    if os.path.exists("readings.csv"):
        df = pd.read_csv("readings.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert("Asia/Kolkata")
        df = df.sort_values("timestamp")
        df["diff_kWh"] = df["reading"].diff()
        df["date"] = df["timestamp"].dt.date

        fig1 = px.line(df, x="timestamp", y="reading", title="📊 Total Reading Over Time")
        st.plotly_chart(fig1)

        fig2 = px.bar(df, x="date", y="diff_kWh", title="🔋 Daily Consumption")
        st.plotly_chart(fig2)
    else:
        st.info("No data available. Please upload a reading first.")

# 4. Appliance Estimator
with tab4:
    st.header("🔌 Appliance Usage Estimator")

    appliance = st.text_input("Appliance name")
    wattage = st.number_input("Power rating (in Watts)", step=10)
    hours = st.number_input("Average usage per day (hours)", step=0.5)

    if st.button("⚙️ Estimate Usage"):
        if appliance and wattage > 0 and hours > 0:
            kWh = (wattage * hours) / 1000
            st.success(f"{appliance} consumes approx. {kWh:.2f} kWh/day")
        else:
            st.warning("Please enter all appliance details.")
