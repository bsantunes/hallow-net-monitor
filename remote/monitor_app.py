import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# --- Configuration ---
LOG_FILE = "monitor_hallow_results.log"
DEVICE_NAME = "Network Fleet Monitor"

st.set_page_config(page_title=DEVICE_NAME, layout="wide")

def load_data():
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame()

    data = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 4:
                continue
            
            # Extract IP from the log line
            log_ip = parts[2].replace("IP: ", "")
            
            entry = {
                "Timestamp": pd.to_datetime(parts[0]),
                "Status": parts[1],
                "IP": log_ip
            }

            if parts[1] == "SUCCESS":
                rtt_parts = parts[3].replace("RTT: ", "").split(" ")[0].split("/")
                if len(rtt_parts) == 4:
                    entry["Min"] = float(rtt_parts[0])
                    entry["Avg"] = float(rtt_parts[1])
                    entry["Max"] = float(rtt_parts[2])
                    entry["Mdev"] = float(rtt_parts[3])
            else:
                entry["Min"], entry["Avg"], entry["Max"], entry["Mdev"] = None, None, None, None
            
            data.append(entry)
    
    return pd.DataFrame(data)

# Header & Meta
st.title(f"📡 {DEVICE_NAME}")
st.write(f"Last updated: {time.strftime('%H:%M:%S')}")

df = load_data()

if df.empty:
    st.warning("No data found in the log file.")
else:
    # --- Global Metrics ---
    total_checks = len(df)
    unique_ips = df["IP"].nunique()
    overall_uptime = (len(df[df["Status"] == "SUCCESS"]) / total_checks) * 100
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Checks (All IPs)", total_checks)
    c2.metric("Active Devices", unique_ips)
    c3.metric("Global Uptime %", f"{overall_uptime:.1f}%")

    # --- Multi-Device Plot ---
    st.subheader("Latency Trend by Device (Avg RTT)")
    success_df = df.dropna(subset=["Avg"]).sort_values("Timestamp")
    
    if not success_df.empty:
        # Added 'color="IP"' to differentiate devices on the chart
        fig = px.line(
            success_df, 
            x="Timestamp", 
            y="Avg", 
            color="IP", 
            template="plotly_dark",
            labels={"Avg": "Latency (ms)", "Timestamp": "Time"},
            hover_data=["Min", "Max"]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No successful ping data available to display in chart.")

    # --- Log Table ---
    st.subheader("Combined History")
    # Show the latest logs first
    st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True)

# Auto-refresh trigger (30 seconds)
time.sleep(30)
st.rerun()
