#!/bin/bash

KAFKA_HOST=$1
KAFKA_PORT=$2
SCRIPT=$3

until $(nc -zv $KAFKA_HOST $KAFKA_PORT); do
  >&2 echo "Waiting for Kafka to be available - sleeping"
  sleep 5
done

>&2 echo "Kafka is up - executing command"

exec python3 $SCRIPT
