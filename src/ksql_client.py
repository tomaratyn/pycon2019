import json
import os
import time
import logging

import click
import requests

KSQL_SERVER = os.environ["KSQL_SERVER"]


@click.command("ksql_client")
def main():
    logging.basicConfig()
    print(f"Hello world")
    response = requests.get(f"http://{KSQL_SERVER}/info")
    print(response.content)
    response = requests.post(
        f"http://{KSQL_SERVER}/query",
        json={
            "ksql": """select * from attendance_count limit 10;""",
            "streamsProperties": {},
        },
        # stream=True,
    )
    # for _ in range(4):
    #     print(response.raw.read(10))
    print(response.content)


if __name__ == "__main__":
    main()
