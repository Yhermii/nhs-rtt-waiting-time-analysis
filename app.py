#  Import libraries 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression

# Page config 
# This sets the browser tab title, icon, and layout of the app
st.set_page_config(
    page_title="NHS RTT Waiting Time Analysis",
    page_icon="🏥",
    layout="wide"
)

#  Load data 
# @st.cache_data load the CSV once and remembers it
@st.cache_data
def load_data():
    df = pd.read_csv('nhs_rtt_clean.csv')
    df["week_ending"] = pd.to_datetime(df["week_ending"])
    return df

df = load_data()

# Header
# st.title adds large heading at the top of the page
st.title("🏥 NHS England — RTT Waiting Time Analysis")
st.markdown("**Referral to Treatment (RTT) data — September 2021 to February 2026**")

# A horizontal line to separate the header from the content
st.divider()

#  Key Metrics Row 
# st.columns splits the page into side-by-side sections
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Peak Waiting List",
    value="7.68M",
    delta="from 5.37M in Sep 2021"
)
col2.metric(
    label="Avg % Within 18 Weeks",
    value="59%",
    delta="-33% below NHS target",
    delta_color="inverse"
)
col3.metric(
    label="NHS 18-Week Target",
    value="92%",
)
col4.metric(
    label="Peak 2yr+ Waiters",
    value="25,519",
    delta_color="inverse"
)

st.divider()

# Sidebar 
st.sidebar.header("📅 Filter Data")

# Date range slider to zoom into a specific period
min_date = df["week_ending"].min()
max_date = df["week_ending"].max()

start_date, end_date = st.sidebar.date_input(
    "Select date range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter the dataframe based on whatever date range the user picks
mask = (df["week_ending"] >= pd.to_datetime(start_date)) & \
       (df["week_ending"] <= pd.to_datetime(end_date))
filtered_df = df[mask]

st.sidebar.markdown(f"**{len(filtered_df)} weeks selected**")

# Chart 1: Total Waiting List
st.subheader("📈 Total Waiting List Over Time")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=filtered_df["week_ending"],
    y=filtered_df["total_waiting_list"],
    mode="lines",
    name="Total Waiting List",
    line=dict(color="#003087", width=2)
))
fig1.add_hline(y=7_000_000, line_dash="dash",
               line_color="red", annotation_text="7 million mark")
fig1.update_layout(
    template="plotly_white", height=400,
    yaxis_tickformat=".2s"
)
# st.plotly_chart renders an interactive plotly chart in the app
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: % Within 18 Weeks 
st.subheader("🎯 % Seen Within 18 Weeks vs 92% NHS Target")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=filtered_df["week_ending"],
    y=filtered_df["pct_within_18w"] * 100,
    mode="lines",
    name="% Within 18w",
    line=dict(color="#009639", width=2)
))
fig2.add_hline(y=92, line_dash="dash",
               line_color="red", annotation_text="92% NHS Target")
fig2.update_layout(
    template="plotly_white", height=400,
    yaxis_title="% Within 18 Weeks"
)
st.plotly_chart(fig2, use_container_width=True)

# Charts 3 & 4 side by side 
# use_container_width splits these two charts into two columns
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚠️ Long Waiters Over Time")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=filtered_df["week_ending"],
        y=filtered_df["52_to_65w"],
        mode="lines", name="52–65 weeks",
        line=dict(color="#FF6900", width=2)
    ))
    fig3.add_trace(go.Scatter(
        x=filtered_df["week_ending"],
        y=filtered_df["over_104w"],
        mode="lines", name="Over 104 weeks",
        line=dict(color="darkred", width=2)
    ))
    fig3.update_layout(template="plotly_white", height=350)
    st.plotly_chart(fig3, use_container_width=True)

with col_right:
    st.subheader("📊 Wait Band Breakdown")
    wait_bands = ["within_18w", "18_to_26w", "26_to_40w",
                  "40_to_52w", "52_to_65w", "over_104w"]
    labels = ["Within 18w", "18–26w", "26–40w",
              "40–52w", "52–65w", "Over 104w"]
    colors = ["#009639", "#78BE20", "#FFB81C",
              "#FF6900", "#DA291C", "#7B1C1C"]
    fig4 = go.Figure()
    for band, label, color in zip(wait_bands, labels, colors):
        fig4.add_trace(go.Scatter(
            x=filtered_df["week_ending"],
            y=filtered_df[band],
            mode="lines", name=label,
            stackgroup="one",
            line=dict(color=color)
        ))
    fig4.update_layout(template="plotly_white", height=350)
    st.plotly_chart(fig4, use_container_width=True)

# Wait Time Estimator 
st.divider()
st.subheader("⏱️ Personal Wait Time Estimator")
st.markdown("Enter your referral date to estimate where you might sit on the waiting list.")

est_col1, est_col2 = st.columns(2)

with est_col1:
    referral_date = st.date_input("Your referral date", value=pd.Timestamp("2025-01-01"))
    weeks_waited = (pd.Timestamp.today() - pd.Timestamp(referral_date)).days // 7
    st.metric("Weeks waited so far", f"{weeks_waited} weeks")

with est_col2:
    # Use the most recent % within 18w to give a simple risk estimate
    latest_pct = df["pct_within_18w"].iloc[-1] * 100
    if weeks_waited <= 18:
        risk = "🟢 Low — you are within the 18-week window"
    elif weeks_waited <= 52:
        risk = "🟡 Medium — you have exceeded the 18-week target"
    else:
        risk = "🔴 High — you have been waiting over 52 weeks"

    st.markdown(f"**Current system performance:** {latest_pct:.1f}% seen within 18 weeks")
    st.markdown(f"**Your wait status:** {risk}")

# Raw Data Explorer 
st.divider()
st.subheader("🔍 Data Explorer")

# Checkbox so users can show/hide the raw data table
if st.checkbox("Show raw data"):
    st.dataframe(filtered_df, use_container_width=True)

# Download button so users can export the filtered data as CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download filtered data as CSV",
    data=csv,
    file_name="nhs_rtt_filtered.csv",
    mime="text/csv"
)

# Footer 
st.divider()
st.caption("Data source: NHS England Waiting List Minimum Data Set (WLMDS) | Analysis by Adeyemi Abodunrin")