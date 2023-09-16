from kafka import KafkaConsumer
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import json

# MongoDB settings
mongo_database = "twitter_covid_db"
mongo_collection = "tweets_and_cases"
mongo_host= "mongo"
mongo_port = 27027
mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'twitter_topic',  # Topic name
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Function to fetch COVID-19 total cases
def fetch_cases():
    covid_worldmeter_url = "https://www.worldometers.info/coronavirus/"
    page = requests.get(covid_worldmeter_url)
    soup = BeautifulSoup(page.content, "html.parser")
    total_cases = soup.find("div", {"class": "maincounter-number"}).get_text().strip().replace(",", "")
    return int(total_cases)

# Function to store tweets and cases into MongoDB
def store_in_mongo(message):
    client = MongoClient(mongo_uri)
    db = client[mongo_database]
    collection = db[mongo_collection]

    total_cases = fetch_cases()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    document = {
        "content": message,
        "timestamp": timestamp,
        "total_case_count": total_cases
    }

    print(document)
    collection.insert_one(document)


# Consume tweets from Kafka and store in MongoDB
for message in consumer:
    tweet = message.value
    store_in_mongo(tweet)
