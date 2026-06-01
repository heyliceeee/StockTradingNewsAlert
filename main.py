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
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
THRESHOLD = 1

def get_stock_data():
    """
    Get the stock data from Alpha Vantage API
    :return: stock data
    """
    url = f"https://www.alphavantage.co/query" # Alpha Vantage API URL
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": api_key_alpha_avantage
    }

    response = requests.get(url, params=params) # Get the response
    data = response.json()["Time Series (Daily)"] # Get the data

    return data
def calculate_percent_change(data):
    """
    Calculate the percentage change of the stock between the last day and the day before yesterday
    :param data: stock data
    :return: percentage change
    """
    datas = list(data.keys())  # Get the keys of the data
    yesterday = data[datas[0]]  # Get the last day data
    day_before = data[datas[1]]  # Get the day before yesterday data

    # Get the last 2 days data
    close_yesterday = float(yesterday["4. close"]) # Get the close price of the last day
    close_before = float(day_before["4. close"]) # Get the close price of the day before yesterday

    # Calculate the percentage change
    difference = close_yesterday - close_before # Calculate the difference
    percent_change = (difference / close_before) * 100 # Calculate the percentage change

    return percent_change
def get_company_news():
    """
    Get the company news from News API
    :return: news
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": COMPANY_NAME,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 3,
        "apiKey": api_key_news
    }
    response = requests.get(url, params=params) # Get the response
    articles = response.json().get("articles", [])
    return articles[:3]
def check_alert_and_get_news(percent_change):
    """
    Check if the alert should be sent
    :param percent_change: percentage change of a stock
    :param threshold: threshold for alert
    :return:
    """
    print(f"Change: {percent_change:.2f}%")
    if abs(percent_change) >= THRESHOLD: # Check if the percentage change is greater than 5%
        news = get_company_news()
        return news
    else:
        print("No News")
        return []

data = get_stock_data() # Get the stock data
percent_change = calculate_percent_change(data) # Calculate the percentage change
news_list = check_alert_and_get_news(percent_change) # Check if the alert should be sent

for i, article in enumerate(news_list, start=1):
    print(f"\nNotícia {i}:")
    print(article["title"])
    print(article["url"])