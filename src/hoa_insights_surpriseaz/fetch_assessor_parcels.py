import asyncio
import logging
import os
import sys
from _collections_abc import Sequence
from asyncio import Semaphore, Task
from logging import Logger
from typing import Any

import aiohttp
from aiohttp import TCPConnector
from aiohttp_retry import ExponentialRetry, RetryClient
from dotenv import load_dotenv
from sqlalchemy import Engine, Row, create_engine, exc, select

from hoa_insights_surpriseaz.database import models_local

load_dotenv()

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_URI: str = f"{os.environ['PROD_LOCAL_DB_URI']}"
LOCAL_DB_NAME: str = f"{os.environ['PROD_LOCAL_DB_NAME']}"

PARCELS_TABLE: str = "parcels"


API_HEADER: dict[str, str] = {os.environ["API_HEADER_TYPE"]: os.environ["API_KEY"]}


def get_parcel_apns() -> list[str]:
    """
    Function retrieves the Accessor Parcel Number (APN) of all parcels from database table: parcels.

    :return: list of all APNs.

    Example:
        APN = ["509-11-444", "509-11-445"]
    """
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}")
        with engine.connect() as conn, conn.begin():
            q_apns: Sequence[Row] = conn.execute(
                statement=select(models_local.Parcel.APN)
            ).all()
            APNs: list[str] = [result[0] for result in q_apns]

        return APNs

    except (exc.OperationalError, exc.ProgrammingError) as err:
        logger.error(f"{err.__cause__}")
        return []


def parcels_api() -> Sequence[dict]:
    """
    Function gets the latest parcel data from Assessor API.

    :return: list of all parcel responses from API.
    """
    APNS: list[str] = get_parcel_apns()
    if APNS:
        logger.info("Fetching parcel data from Assessor API.... ")
        consumed_parcel_data: Sequence[object] = asyncio.run(async_main(APNS))
        logger.info("Fetched parcel data from Assessor API")

        return consumed_parcel_data
    else:
        logger.error(
            "Database setup log file found, but cannot retrieve APNs from database, exiting."
        )
        sys.exit()


async def get_parcel_details(client: RetryClient, sem: Semaphore, url: str) -> dict:
    """
    Function retrieves parcel data from the API.

    :param client: retry client
    :param sem: semaphore for tcp connection limiting
    :param url: API end point suffixed with parcel APN

    :return: parcel API data as dict
    """
    try:
        async with sem, client.get(url) as resp:
            parcel_details: dict = await resp.json()

            return parcel_details

    except aiohttp.ClientResponseError as e:
        print("sleeping")
        await asyncio.sleep(5)
        logger.error(e)
        print("AWAKE", e)

        async with sem, client.get(url) as resp:
            parcel_details: dict = await resp.json()
            logger.warning(f"{url} was retried")

        return parcel_details


async def async_main(apns: list[str]) -> list[dict[Any, Any]]:
    """
    Function asynchronously gathers API responses from Assessor site.

    :param apns: list of APNs used as endpoint for API requests
    :return: list of parcel API response data
    """
    connector: TCPConnector = TCPConnector(
        ssl=False,
        limit=0,
        limit_per_host=20,
        enable_cleanup_closed=False,
        ttl_dns_cache=600,
    )
    async with RetryClient(
        headers=API_HEADER,
        connector=connector,
        raise_for_status=True,
        retry_options=ExponentialRetry(statuses={429}, attempts=5),
    ) as retry_client:
        sem: Semaphore = asyncio.Semaphore(2)
        tasks: list[Task[dict[Any, Any]]] = []
        for apn in apns:
            parcel_url: str = f"https://mcassessor.maricopa.gov/parcel/{apn}"
            tasks.append(
                asyncio.create_task(get_parcel_details(retry_client, sem, parcel_url))
            )

        parcels: list[dict[Any, Any]] = await asyncio.gather(
            *tasks, return_exceptions=False
        )

        return parcels


if __name__ == "__main__":
    parcels_api()
