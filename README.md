# 📈 Golden Cross Strategy Bot with MetaSync & Python

This tutorial demonstrates how to build a **simple trading bot** using **MetaSync API** on RapidAPI.  
The bot fetches live **tick data** from MetaTrader 5 (MT5), calculates **moving averages (MA)**, and generates trading signals based on the **Golden Cross** and **Death Cross** strategy.

---

## 🚀 What You'll Learn
- Connect to MetaTrader 5 using **MetaSync API**  
- Fetch live **EURUSD tick data**  
- Calculate **50-period** and **200-period moving averages**  
- Detect **Golden Cross (BUY)** and **Death Cross (SELL)** signals  
- Run a **continuous loop** to monitor signals in real time  

---

## 📦 Requirements

- Python 3.8+  
- Libraries:  
  ```bash
  pip install requests pandas


* A **RapidAPI account** with access to [MetaSync API](https://rapidapi.com/metasync-metasync-default/api/metasyc)
* MetaTrader 5 terminal open and connected to your broker

---

## 🔑 Setup

1. Sign up at [RapidAPI](https://rapidapi.com) and subscribe to **MetaSync API**
2. Copy your **X-RapidAPI-Key**
3. Replace the placeholders in the script:

   ```python
   API_KEY = "your-rapidapi-key"
   HOST = "metasyc.p.rapidapi.com"
   SYMBOL = "EURUSD"
   ```

---

## 🐍 Example Code

```python
import pandas as pd
import requests
from datetime import datetime
import time

# RapidAPI credentials
API_KEY = "your-rapidapi-key"
HOST = "metasyc.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": HOST
}
SYMBOL = "EURUSD"

# Fetch recent tick data
def fetch_recent_ticks(symbol, num_ticks=250):
    url = f"https://{HOST}/tick"
    ticks_list = []
    for _ in range(num_ticks):
        querystring = {"symbol": symbol}
        response = requests.get(url, headers=HEADERS, params=querystring)
        data = response.json()
        ticks_list.append({'time': data['time'], 'bid': data['bid']})
        time.sleep(0.1)
    return ticks_list

# Check for crossover (Golden or Death Cross)
def check_for_cross(price_data):
    df = pd.DataFrame(price_data)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    short_ma = df['bid'].rolling(window=50).mean()
    long_ma = df['bid'].rolling(window=200).mean()

    current_short = short_ma.iloc[-1]
    current_long = long_ma.iloc[-1]
    previous_short = short_ma.iloc[-2]
    previous_long = long_ma.iloc[-2]

    signal = "HOLD"
    if previous_short < previous_long and current_short > current_long:
        signal = "BUY"
        print("🎯 GOLDEN CROSS DETECTED! BUY SIGNAL!")
    elif previous_short > previous_long and current_short < current_long:
        signal = "SELL"
        print("🎯 DEATH CROSS DETECTED! SELL SIGNAL!")

    print(f"Short MA (50): {current_short:.5f}")
    print(f"Long MA (200): {current_long:.5f}")
    print(f"Signal: {signal}")
    return signal

# Main bot loop
def main():
    data = fetch_recent_ticks(SYMBOL)
    while True:
        url = f"https://{HOST}/tick"
        querystring = {"symbol": SYMBOL}
        response = requests.get(url, headers=HEADERS, params=querystring)
        new_tick = response.json()

        data.append({'time': new_tick['time'], 'bid': new_tick['bid']})
        data.pop(0)

        signal = check_for_cross(data)

        # TODO: Add trade execution here
        if signal == "BUY":
            print("Execute BUY order here")
        elif signal == "SELL":
            print("Execute SELL order here")

        time.sleep(10)

if __name__ == "__main__":
    main()
```

---

## ✅ Sample Output

```
Fetching 250 ticks for EURUSD...
Short MA (50): 1.08325
Long MA (200): 1.08310
Signal: HOLD
Waiting...
🎯 GOLDEN CROSS DETECTED! BUY SIGNAL!
Short MA (50): 1.08350
Long MA (200): 1.08320
Signal: BUY
```

---

## ⚡ Next Steps

* Implement the `order_send()` function to place trades via MetaSync
* Extend strategy with Stop Loss & Take Profit
* Store data in a database or Google Sheets for backtesting

---

## 📌 Notes

* Always test on a **demo account** first.
* Avoid hitting RapidAPI **rate limits** (add `time.sleep()` between requests).
* This strategy is **educational only** — not financial advice.

---

## 🤝 Support

Questions? Issues?

* Open a GitHub Issue
