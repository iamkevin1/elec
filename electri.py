import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os

# App title
st.set_page_config(page_title="Electricity Analyzer", layout="centered")
st.title("⚡ Electricity Reading and Analyzer")

# Section 1: Upload and Enter Reading
st.header("📥 Upload Electricity Reading")

uploaded_image = st.file_uploader("Upload meter image", type=["png", "jpg", "jpeg"])
reading = st.number_input("Enter reading (in kWh)", step=0.1)

# Use separate date & time input (fix for datetime bug)
date = st.date_input("Select date of reading", datetime.date.today())
time = st.time_input("Select time of reading", datetime.datetime.now().time())
timestamp = datetime.datetime.combine(date, time)

if st.button("Save Reading"):
    data = {"timestamp": [timestamp], "reading": [reading]}
    df = pd.DataFrame(data)

    if os.path.exists("readings.csv"):
        df_old = pd.read_csv("readings.csv", parse_dates=["timestamp"])
        df_all = pd.concat([df_old, df], ignore_index=True)
    else:
        df_all = df

    df_all.to_csv("readings.csv", index=False)
    st.success("Reading saved!")

# Section 2: View All Readings
st.header("📋 View All Electricity Data")

if os.path.exists("readings.csv"):
    df = pd.read_csv("readings.csv", parse_dates=["timestamp"])
    st.dataframe(df.sort_values("timestamp"))

# Section 3: Graphs & Trends
st.header("📈 Analyze Usage Trends")

if os.path.exists("readings.csv") and len(df) > 1:
    df = df.sort_values("timestamp")
    df["diff_kWh"] = df["reading"].diff()
    df["date"] = df["timestamp"].dt.date

    fig = px.line(df, x="timestamp", y="reading", title="Total Reading Over Time")
    st.plotly_chart(fig)

    fig2 = px.bar(df, x="date", y="diff_kWh", title="Daily Consumption (kWh)")
    st.plotly_chart(fig2)

# Section 4: Appliance Estimator
st.header("🔌 Estimate Appliance Usage")

appliance = st.text_input("Appliance name")
wattage = st.number_input("Power rating (Watts)", step=10)
hours_per_day = st.number_input("Usage per day (hours)", step=0.5)

if st.button("Estimate Daily Usage"):
    kWh_per_day = (wattage * hours_per_day) / 1000
    st.success(f"{appliance} consumes approximately {kWh_per_day:.2f} kWh/day")
