# Use Alpine as the base image
FROM alpine:3.14

# Install Bash
RUN apk add --no-cache bash


# Install Python and Java
RUN apk add --no-cache python3 openjdk11 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY wait-for-kakfa.sh /app/wait-for-kakfa.sh
RUN chmod +x /app/wait-for-kakfa.sh


# Copy your Python script into the container
COPY producer.py /app/producer.py
COPY consumer.py /app/consumer.py


