# backend/engine.py

import time
import json
import os
import pandas as pd
from datetime import datetime
from strategy import add_indicators, generate_signal, compute_confidence
from nsepython import nse_quote_ltp

CONFIDENCE_THRESHOLD = 70
FETCH_INTERVAL = 1
CANDLE_INTERVAL = 60
instrument_name = "NIFTY"

price_buffer = []

def is_market_open():
    now = datetime.now()
    return now.weekday() < 5 and (now.hour > 9 or (now.hour == 9 and now.minute >= 15)) and (now.hour < 15 or (now.hour == 15 and now.minute <= 30))

def get_live_price():
    try:
        if is_market_open():
            price = float(nse_quote_ltp(instrument_name))
            save_last_price(price)
            print("✅ Live price:", price)
            return price
        else:
            price = load_last_price()
            print("🔒 Market Closed – Showing last price:", price)
            return price
    except Exception as e:
        print("❌ Error fetching price:", e)
        return load_last_price()

def save_last_price(price):
    with open("last_price.json", "w") as f:
        json.dump({"price": price, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f)

def load_last_price():
    if os.path.exists("last_price.json"):
        with open("last_price.json", "r") as f:
            return json.load(f)["price"]
    return 0

def build_candle(price_buffer):
    open_price = price_buffer[0]
    close_price = price_buffer[-1]
    high_price = max(price_buffer)
    low_price = min(price_buffer)
    volume = 0
    return {
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
        "volume": volume
    }

def write_signal_to_file(signal_data):
    with open("signal_log.json", "w") as f:
        json.dump(signal_data, f)

def read_selected_strategy():
    try:
        with open("selected_strategy.txt", "r") as f:
            return f.read().strip()
    except:
        return "EMA Crossover"

def run_signal_engine():
    print("🧠 Signal Engine Running with Strategy Selection...")
    global price_buffer
    df = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
    last_candle_time = datetime.now().replace(second=0, microsecond=0)

    while True:
        now = datetime.now()
        price = get_live_price()

        if price:
            price_buffer.append(price)

        if (now - last_candle_time).total_seconds() >= CANDLE_INTERVAL:
            if len(price_buffer) > 0:
                new_candle = build_candle(price_buffer)
                df.loc[now] = new_candle
                price_buffer = []
                last_candle_time = now.replace(second=0, microsecond=0)

                df = add_indicators(df)
                confidence = compute_confidence(df)
                selected_strategy = read_selected_strategy()
                signal = generate_signal(df, strategy=selected_strategy)

                if confidence >= CONFIDENCE_THRESHOLD:
                    signal_data = {
                        "time": now.strftime('%Y-%m-%d %H:%M:%S'),
                        "signal": signal,
                        "confidence": confidence
                    }
                    write_signal_to_file(signal_data)
                    print(f"[{signal_data['time']}] ✅ {selected_strategy} Signal: {signal} | Confidence: {confidence}%")
                else:
                    print(f"[{now.strftime('%H:%M:%S')}] ⚠️ Confidence too low: {confidence}% — No signal")
            else:
                print(f"[{now.strftime('%H:%M:%S')}] ⚠️ No price data collected")

        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    run_signal_engine()
