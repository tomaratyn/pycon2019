import json
import os
import logging
import random
import time

import click
import faker
import kafka
from kafka.producer.future import FutureRecordMetadata, RecordMetadata

PYCONS = {
    "PyConCa": (
        "Python is great",
        "Python is better than X",
        "Python is the humblest",
    ),
    "EuroPython": (
        "Kubernetes 101 for Python Developers",
        "Keep Those Ducks in (Type) Check!",
        "How to power up your product by machine learning with python micro-service",
    ),
    "PyConPl": (
        "ML model from an idea to production with the help of Python",
        "Python internals - how does CPython work?",
        "Going FaaS with Python",
    ),
    "PyConAfrica": (
        "How Python rises in Nambia",
        "AfroPython: Empowering black people using Python in Brazil",
        "Bridging the talent gap between Python communities and industry",
    ),
    "PyConJP": (
        "Using Python in Music Signal Processing, Speech Recognition and "
        "Intent Classification in Chatbot",
        "Yet Another Isolation - Debian Package",
        "Why Python is Eating the World",
    ),
}

TOPIC_NAME = os.environ["KAFKA_TOPIC"]


def config_logging():
    logging.basicConfig()


@click.command("event_registration_producer")
def main():
    config_logging()
    print("Starting Event Registration Producer")
    registration_faker = faker.Faker()
    bootstrap_servers = os.environ["KAFKA_BOOTSTRAP"]
    print(f"Bootstrap servers are {bootstrap_servers}")
    producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)
    while True:
        name = registration_faker.name()
        event = random.choice([*PYCONS.keys()])
        session = random.choice(PYCONS[event])
        item = {
            "event": event,
            "name": name,
            "session": session,
        }
        print(f"{name} registered for {session} at {event}")
        future: FutureRecordMetadata = producer.send(
            TOPIC_NAME, value=json.dumps(item).encode(), key=event.encode()
        )
        result: RecordMetadata = future.get(timeout=10)
        time.sleep(1)


if __name__ == "__main__":
    main()
