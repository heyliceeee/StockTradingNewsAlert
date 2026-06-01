import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

api_key_alpha_avantage = os.getenv("API_KEY_ALPHA_AVANTAGE")
api_key_news = os.getenv("API_KEY_NEWS")
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
THRESHOLD = 5

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

    close_yesterday = float(yesterday["4. close"]) # Get the close price of the last day
    close_before = float(day_before["4. close"]) # Get the close price of the day before yesterday

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
def format_percent_change(percent_change):
    """
    Format the percentage change
    :param percent_change:
    :return: formatted percentage change
    """
    arrow = "🔺" if percent_change > 0 else "🔻" # Determine the arrow based on the percentage change
    percent = f"{abs(percent_change):.2f}%" # Format the percentage change
    return f"{arrow}{percent}" # Return the formatted percentage change
def format_news_message(percent_change, article):
    """
    Format the news message
    :param percent_change:
    :param article:
    :return:
    """
    formatted = format_percent_change(percent_change)
    title = article.get("title", "No title") # Get the title of the article
    description = article.get("description", "No description") # Get the description of the article

    message = (
        f"{STOCK}: {formatted}\n"
        f"Headline: {title}\n"
        f"Brief: {description}"
    )
    return message
def send_telegram_message(text):
    if not text: # if the text is empty
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"} # create the payload
    requests.post(url, data=payload)
def process_stock_alert():
    """
    Processes the stock alert
    :return: true if alert sent, false otherwise
    """
    data = get_stock_data() # Get the stock data
    percent_change = calculate_percent_change(data) # Calculate the percentage change

    if abs(percent_change) >= THRESHOLD: # If change >= 5%
        articles = get_company_news() # Get the company news

        for article in articles:
            msg = format_news_message(percent_change, article) # Format the news message
            send_telegram_message(msg) # Send the news message
        return True
    return False

process_stock_alert() # Process the stock alert