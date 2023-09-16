from kafka import KafkaProducer
import socket
from datetime import datetime
from datetime import datetime, timedelta
import json

# clean individual tweets
def clean_tweet(tweet):
    tweet = tweet.replace("#", "").replace("RT:", "")
    return ' '.join(word for word in tweet.split() if not word.startswith("http"))


# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Read tweets from TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the twitter stream simulator on the port 5555 of the server
server_address = ("simulator", 5555)
client_socket.connect(server_address)

buffered_tweets = []
last_flush_time = datetime.utcnow()

try:
    while True:
        received_data = client_socket.recv(10000)
        if received_data:
            # Clean the tweet
            cleaned_data = clean_tweet(received_data.decode('utf-8'))

            # Buffer the tweet
            buffered_tweets.append(cleaned_data)

            current_time = datetime.utcnow()
            time_difference = current_time - last_flush_time

            # If 20 seconds or more have passed, send the buffered tweets to Kafka
            if time_difference >= timedelta(seconds=20):
                producer.send('twitter_topic', value=buffered_tweets)
                # Reset
                buffered_tweets = []
                last_flush_time = current_time
finally:
    client_socket.close()

