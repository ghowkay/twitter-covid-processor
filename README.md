# Twitter and COVID-19 Data Pipeline

## Overview

This project ingests live Twitter data using simular app, fetch COVID-19 total case numbers, and store the merged information into a MongoDB instance.

## Architecture

1. **Kafka Streaming**: For tweet ingestion and processing
2. **BeautifulSoup**: For web scraping COVID-19 stats
3. **MongoDB**: For data storage


## Brief Documentation

### Introduction

The application serves as a data pipeline to collect, process, and store Twitter messages alongside global COVID-19 case counts. The technology stack includes Kafka for data ingestion and processing, BeautifulSoup for web scraping, and MongoDB for data storage. All services are also containerized using docker.

### Architecture

The architecture is built on three main components:

1. **Data Ingestion (Kakfa Producer)**: The application setups a kafka Streaming producer that listens to a simulated Twitter stream on `localhost:5555`. Messages are collected in batches every 20 seconds and pushed to a kafka topic
  
2. **Data Processing (Kafka Consumer & BeautifulSoup)**: kafka consumer listens to incoming Twitter messages from the topic. The messages are cleaned to remove hashtags, 'RT:', and URLs. Concurrently, COVID-19 case counts are scraped from worldometer.info.

3. **Data Storage (MongoDB)**: The processed Twitter messages and COVID-19 case counts are stored together in a MongoDB database.


### How to Run

```bash
docker-compose up
```
