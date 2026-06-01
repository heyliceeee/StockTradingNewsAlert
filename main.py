import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

api_key_alpha_avantage = os.getenv("API_KEY_ALPHA_AVANTAGE")
api_key_news = os.getenv("API_KEY_NEWS")
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")
dir_path = os.path.dirname(os.path.realpath(__file__)) # Get the directory of the current script
STOCK = "AMC"
COMPANY_NAME = "AMC Entertainment"

# 1. Search diary data
url = f"https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_alpha_avantage
}

response = requests.get(url, params=params) # Get the response
data = response.json()["Time Series (Daily)"] # Get the data

# 2. Get the last 2 days data
datas = list(data.keys()) # Get the keys of the data
yesterday = data[datas[0]] # Get the last day data
day_before = data[datas[1]] # Get the day before yesterday data

close_yesterday = float(yesterday["4. close"]) # Get the close price of the last day
close_before = float(day_before["4. close"]) # Get the close price of the day before yesterday

# 3. Calculate the percentage change
difference = close_yesterday - close_before # Calculate the difference
percent_change = (difference / close_before) * 100 # Calculate the percentage change
print(f"Change: {percent_change:.2f}%")

if abs(percent_change) >= 5: # Check if the percentage change is greater than 5%
    print("Get News")
else:
    print("No News")




