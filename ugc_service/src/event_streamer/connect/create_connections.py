import json
import logging
from typing import Generator
import os
from http import HTTPStatus

import aiohttp
import backoff

from core.config import settings

logging.basicConfig(level=logging.INFO)


def read_properties_files(path: str) -> Generator:
    for file_connect in os.listdir(path):
        with open(os.path.join(path, file_connect)) as fs:
            yield json.load(fs), file_connect


@backoff.on_exception(
    backoff.expo,
    (
        aiohttp.client_exceptions.ClientConnectorError,
        aiohttp.client_exceptions.ServerDisconnectedError,
    ),
    max_time=1000,
    max_tries=10,
)
async def request_connect(http_client: aiohttp.ClientSession, json_connect: dict):
    response = await http_client.post(
        url=f"http://{settings.connect.host}:{settings.connect.port}/connectors",  # type: ignore
        headers={"Content-Type": "application/json"},
        data=json.dumps(json_connect),
    )
    return response


async def init_connections():
    http_client = aiohttp.ClientSession()
    for json_connect, file_connect in read_properties_files(
        r"./event_streamer/connect/connections"
    ):
        response = await request_connect(http_client, json_connect)
        logging.info(f"status: {response.status}")
        if HTTPStatus.CREATED != response.status:
            logging.error(f"ERROR create connect by file: {file_connect}")
