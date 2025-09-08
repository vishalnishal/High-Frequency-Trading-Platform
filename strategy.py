# backend/strategy.py

import pandas as pd
import numpy as np
import ta  # Ensure ta is installed: pip install ta

def add_indicators(df):
    df = df.copy()
    df["EMA_10"] = ta.trend.ema_indicator(df['close'], window=10).fillna(0)
    df["EMA_20"] = ta.trend.ema_indicator(df['close'], window=20).fillna(0)
    df["RSI"] = ta.momentum.rsi(df['close'], window=14).fillna(0)
    macd = ta.trend.macd_diff(df['close'])
    df["MACD"] = macd.fillna(0)
    return df

def compute_confidence(df):
    latest = df.iloc[-1]
    score = 0
    if latest["EMA_10"] > latest["EMA_20"]:
        score += 30
    if latest["RSI"] > 50:
        score += 20
    if latest["MACD"] > 0:
        score += 20
    return min(score + 30, 100)

def generate_signal(df, strategy="EMA Crossover"):
    if df.empty:
        return "Exit"

    latest = df.iloc[-1]

    if strategy == "EMA Crossover":
        if latest["EMA_10"] > latest["EMA_20"]:
            return "Buy"
        elif latest["EMA_10"] < latest["EMA_20"]:
            return "Sell"
        else:
            return "Exit"

    elif strategy == "RSI":
        if latest["RSI"] > 70:
            return "Sell"
        elif latest["RSI"] < 30:
            return "Buy"
        else:
            return "Exit"

    elif strategy == "MACD":
        if latest["MACD"] > 0:
            return "Buy"
        elif latest["MACD"] < 0:
            return "Sell"
        else:
            return "Exit"

    return "Exit"
