import pandas as pd
import requests
from datetime import datetime
import time

# Insert your RapidAPI key and host here
API_KEY = "your-rapid-api-key"
HOST = "metasyc.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": HOST
}
SYMBOL = "EURUSD"

def fetch_recent_ticks(symbol, num_ticks=250):
    """Fetches a list of recent tick data to build a price history."""
    url = "https://metasyc.p.rapidapi.com/tick"
    ticks_list = []
    
    print(f"Fetching {num_ticks} ticks for {symbol}...")
    for _ in range(num_ticks):
        try:
            querystring = {"symbol": symbol}
            response = requests.get(url, headers=HEADERS, params=querystring)
            data = response.json()
            # Append the bid price and the time to our list
            ticks_list.append({
                'time': data['time'],
                'bid': data['bid']
            })
            time.sleep(0.1)  # Pause briefly to avoid hitting rate limits
        except Exception as e:
            print(f"Error fetching tick: {e}")
            continue
            
    return ticks_list

def check_for_cross(price_data):
    """Calculates moving averages and checks for a Golden or Death Cross."""
    # Ensure we have enough data points to calculate the long moving average
    if len(price_data) < 200:
        print("Not enough data to calculate moving averages. Need 200 ticks.")
        return "HOLD"

    # Create a Pandas DataFrame from our list of ticks
    df = pd.DataFrame(price_data)
    # Convert the 'time' string to a datetime object
    df['time'] = pd.to_datetime(df['time'])
    # Set the time as the index (makes calculations easier)
    df.set_index('time', inplace=True)
    
    # Calculate the moving averages
    short_ma = df['bid'].rolling(window=50).mean()  # 50-period MA
    long_ma = df['bid'].rolling(window=200).mean()   # 200-period MA
    
    try:
        # Get the very last values
        current_short = short_ma.iloc[-1]
        current_long = long_ma.iloc[-1]
        # Get the previous values to compare
        previous_short = short_ma.iloc[-2]
        previous_long = long_ma.iloc[-2]
    except IndexError:
        # This can happen if there's not enough data for iloc[-2]
        print("Not enough data for crossover comparison yet.")
        return "HOLD"

    # Logic to detect a crossover
    signal = "HOLD"  # Default signal
    # Golden Cross: Short MA was below Long MA and is now above
    if previous_short < previous_long and current_short > current_long:
        signal = "BUY"
        print("🎯 GOLDEN CROSS DETECTED! BUY SIGNAL!")
    # Death Cross: Short MA was above Long MA and is now below
    elif previous_short > previous_long and current_short < current_long:
        signal = "SELL"
        print("🎯 DEATH CROSS DETECTED! SELL SIGNAL!")
        
    # Print the current values for clarity
    print(f"Short MA (50): {current_short:.5f}")
    print(f"Long MA (200): {current_long:.5f}")
    print(f"Signal: {signal}")
    
    return signal

def main():
    """Main function to run the Golden Cross strategy in a loop."""
    print("Starting Golden Cross Strategy Bot...")
    print("-------------------------------------")
    
    # First, fetch initial data
    data = fetch_recent_ticks(SYMBOL)
    
    while True:
        try:
            # Get the latest tick to update our dataset
            url = "https://metasyc.p.rapidapi.com/tick"
            querystring = {"symbol": SYMBOL}
            response = requests.get(url, headers=HEADERS, params=querystring)
            new_tick = response.json()
            
            # Add the new tick to our list and remove the oldest one
            data.append({'time': new_tick['time'], 'bid': new_tick['bid']})
            data.pop(0)  # Keep our list at a fixed length (e.g., 250 items)
            
            # Check for a signal with the updated data
            signal = check_for_cross(data)
            
            # Here is where you would add code to EXECUTE the trade!
            if signal == "BUY":
              order_send(action='buy')
            elif signal == "SELL":
              order_send(action='sell')
            
            # Wait before checking again
            print("Waiting...")
            time.sleep(10) # Check for a signal every 10 seconds
            
        except KeyboardInterrupt:
            print("\nBot stopped by user.")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
