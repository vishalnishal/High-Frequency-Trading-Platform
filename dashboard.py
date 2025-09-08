# frontend/dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os, json
from datetime import datetime, timedelta
import pytz

# --- Config ---
st.set_page_config(page_title="🦉 Owlstone – Nifty Signal Generator", layout="wide")

# --- Heading ---
st.markdown("""
<h1 style='text-align: center;'>🦉 Owlstone</h1>
<h4 style='text-align: center; color: gray;'>
Smart Nifty signal generator using confidence-based strategies
</h4>
""", unsafe_allow_html=True)

# --- Market Status ---
def is_market_open():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    return now.weekday() < 5 and market_open <= now <= market_close

market_open = is_market_open()
status = "🟢 Open" if market_open else "🔴 Closed"
st.subheader(f"📅 Market Status: {status}")

# --- Live Last Price ---
def load_last_price():
    if os.path.exists("last_price.json"):
        with open("last_price.json", "r") as f:
            data = json.load(f)
            return data["price"], data["timestamp"]
    return 0, "—"

price, ptime = load_last_price()
st.metric(label="📈 Nifty Last Price", value=f"{price}", delta=f"Updated @ {ptime}")

# --- Strategy Select ---
strategy = st.selectbox("📊 Select Strategy", ["EMA Crossover", "RSI", "MACD"], index=0)

# Save to file for engine.py to read
with open("selected_strategy.txt", "w") as f:
    f.write(strategy)


# --- Signal Status ---
def read_signal():
    if os.path.exists("signal_log.json"):
        with open("signal_log.json", "r") as f:
            return json.load(f)
    return None

st.markdown("### 📡 Live Signal Log")
signal_data = read_signal()

if signal_data:
    st.success(f"""
    **Time:** {signal_data['time']}  
    **Signal:** `{signal_data['signal']}`  
    **Confidence:** {signal_data['confidence']}%
    """)
else:
    st.warning("⚠️ Waiting for signal engine...")

st.divider()

# --- Chart Section ---
st.subheader("📊 Real-Time Price Chart")

def load_live_data():
    if os.path.exists("live_candles.csv"):
        df = pd.read_csv("live_candles.csv", index_col=0, parse_dates=True)
        return df
    return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

df = load_live_data()

chart_type = st.radio("Chart View", ["Trend Line", "Candlestick"], horizontal=True)

fig = go.Figure()
if not df.empty:
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            increasing=dict(line=dict(color="green", width=1.5)),
            decreasing=dict(line=dict(color="red", width=1.5))
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["close"],
            mode="lines",
            name="Nifty",
            line=dict(color="blue", width=2)
        ))

    fig.update_layout(
        height=500,
        xaxis_title="Time",
        yaxis_title="Price",
        hovermode="x unified",
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            showline=True,
            tickformat="%H:%M"
        ),
        yaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            showline=True
        ),
        dragmode="pan"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Waiting for engine to collect live candle data...")

# --- Footer ---
st.divider()
st.markdown("### 🚀 Project Objective")
st.markdown("""
Owlstone is a lightweight, real-time Nifty signal system that uses multiple technical strategies  
(EMA crossover, RSI, MACD) to analyze live OHLC data and generate signals with confidence scoring.  
It’s designed for short-term timeframe decisions using free public market data.
""")

st.markdown("### 🙌 Developed By")
st.markdown("""
<div style="text-align: center; font-size: 1.2em;">
    <a href="https://www.linkedin.com/in/vishalnishal/" target="_blank">Vishal</a> &nbsp; | &nbsp;
    <a href="https://www.linkedin.com/in/harshkumar001/" target="_blank">Harsh</a>
</div>
""", unsafe_allow_html=True)
