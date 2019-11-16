import json
import logging
import os

import click
import kafka
from kafka.structs import KafkaMessage

TOPIC = os.environ.get("KAFKA_TOPIC", "PyConRegistration")


@click.command("consumer_python_kafka")
def main():
    logging.basicConfig()
    print("Event Registration Consumer")
    bootstrap_server = os.environ["KAFKA_BOOTSTRAP"]
    consumer_group = os.environ["CONSUMER_GROUP_ID"]
    consumer = kafka.KafkaConsumer(
        TOPIC, bootstrap_servers=bootstrap_server, group_id=consumer_group,
    )
    mgs: KafkaMessage
    for msg in consumer:
        key = msg.key.decode()
        value = json.loads(msg.value.decode())
        print(
            f"[{TOPIC}][{key}] {value['name']} for {value['session']} at {value['event']}"
        )


if __name__ == "__main__":
    main()
