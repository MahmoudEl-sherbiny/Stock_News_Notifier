import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv()

STOCK_NAME = "TSLA"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}



COMPANY_NAME = "Tesla Inc"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = os.getenv("NEWS_API")

news_parameters = {
    "apiKey": NEWS_API,
    "qInTitle": COMPANY_NAME
}


TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")




r = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = r.json()["Time Series (Daily)"]  # to get the data of value of this key which is a big dictionary
# print(data)
data_list = [value for (key, value) in data.items()]
# print(data_list)
# value it's a data of day contain open, close , high and other information
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
print(day_before_yesterday_closing_price)

difference = (yesterday_closing_price - day_before_yesterday_closing_price)
up_down = None
if difference > 5:
    up_down = "🔝"
else:
    up_down = "🔽"

percentage = abs(round((difference / yesterday_closing_price) * 100))
# print(percentage)


if percentage >= 1:
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = response.json()["articles"]
    # print(articles)
    first_three_articles = articles[:3]
    # print(first_three_articles)


formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in first_three_articles]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for articlee in formatted_articles:
    message = client.messages.create(
        body=articlee,
        from_=f'whatsapp:{os.getenv("F_NUMBER")}',
        to=f'whatsapp:{os.getenv("T_NUMBER")}'
    )
