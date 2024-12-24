import yfinance as yf

# Define the stock ticker
stock_ticker = "BEL.NS"  # Ticker for Bharat Electronics Limited on NSE

# Fetch stock data using yfinance
stock = yf.Ticker(stock_ticker)

try:
    # Fetch stock information
    info = stock.info
    print("Debug Info:", info)  # Log raw info for debugging
    
    # Extract relevant fields
    current_price = info.get("regularMarketPrice", "Data not available")
    previous_close = info.get("previousClose", "Data not available")
    day_high = info.get("dayHigh", "Data not available")
    day_low = info.get("dayLow", "Data not available")

    # Print the extracted data
    print(f"BEL (Bharat Electronics Limited) Stock Data:")
    print(f"  Current Price: ₹{current_price} INR")
    print(f"  Previous Close: ₹{previous_close} INR")
    print(f"  Day High: ₹{day_high} INR")
    print(f"  Day Low: ₹{day_low} INR")

except Exception as e:
    print(f"Error fetching data for {stock_ticker}: {e}")
