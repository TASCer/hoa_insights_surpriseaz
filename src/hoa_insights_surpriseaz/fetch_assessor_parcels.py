import aiohttp
import asyncio
import json
import logging
import platform

from aiohttp import TCPConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from asyncio import Semaphore, Task
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database import models_local

from logging import Logger
from sqlalchemy import Engine, Sequence, Tuple, create_engine, exc, Row, select

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
LOCAL_DB_NAME: str = f"{my_secrets.prod_local_dbname}"

PARCELS_TABLE: str = "parcels"

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

API_HEADER: dict[str, str] = {my_secrets.api_header_type: my_secrets.api_header_creds}


def get_parcel_apns() -> list[str]:
    """
    Function retrieves the APN of all parcels from database table: parcels.

    :return: sequence of all APNs.

    Example:
        APN = ["509-11-444", "509-11-445"]
    """
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}")
        with engine.connect() as conn, conn.begin():
            q_apns: Sequence[Row[Tuple[str]]] = conn.execute(
                select(models_local.Parcel.APN)).all()
            APNs = [result[0] for result in q_apns]

        return APNs

    except (exc.OperationalError, exc.ProgrammingError) as err:
        logger.error(f"{err.__cause__}")
        return []


def parcels_api() -> list[dict]:
    """
    Function gets the latest parcel data from Assessor API.

    :return: sequence of all parcel responses from API.
    """
    APNS: list[str] = get_parcel_apns()
    if APNS:
        logger.info("Accessing Assessor API to get latest parcel data")
        consumed_parcel_data: list[dict] = asyncio.run(async_main(APNS))
        logger.info("All latest parcel data consumed from API")

        return consumed_parcel_data
    else:
        logger.error("Database setup log file found, but cannot retrieve APNs from database, exiting.")
        exit()


async def get_parcel_details(client: RetryClient, sem: Semaphore, url: str) -> dict:
    """
    Function retrieves parcel data from the API.

    :param client: retry client
    :param sem: semaphore for tcp connection limiting
    :param url: API end point suffixed with parcel APN

    :return: parcel latest data
    """
    try:
        async with sem, client.get(url) as resp:
            response_code: int = resp.status
            if response_code != 200:
                logger.warning(f"NON 200 Code Errer {response_code}")
            parcel_details: dict = await resp.json()

            return parcel_details

    except aiohttp.ClientOSError as os:
        logger.error(f"{os} - {url}")

        return exit()

    except (
        json.JSONDecodeError,
        aiohttp.ContentTypeError,
        aiohttp.ClientResponseError,
        TypeError,
        aiohttp.ClientPayloadError,
    ) as e:
        print("sleeping")
        await asyncio.sleep(4)
        print("ERROR", e)
        logger.error(e)
        async with sem, client.get(url) as resp:
            parcel_details: dict = await resp.json()
            logger.warning(f"{url} was retried")

        return parcel_details


async def async_main(apns: list[str]) -> list[dict]:
    """
    Function asynchronously gathers API responses from Assessor site.

    :param apns: collection of APNs used as endpoint for API
    :return: sequence of parcel API response data
    """
    connector: TCPConnector = TCPConnector(
        ssl=False,
        limit=0,
        limit_per_host=20,
        enable_cleanup_closed=False,
    )
    async with RetryClient(
        headers=API_HEADER,
        connector=connector,
        raise_for_status=True,
        retry_options=ExponentialRetry(attempts=3),
    ) as retry_client:
        sem: Semaphore = asyncio.Semaphore(2)
        tasks: list[Task[object]] = []
        for apn in apns:
            parcel_url: str = f"https://mcassessor.maricopa.gov/parcel/{apn}"
            tasks.append(
                asyncio.create_task(get_parcel_details(retry_client, sem, parcel_url))
            )

        parcels: list[dict] = await asyncio.gather(*tasks, return_exceptions=False)

        return parcels


if __name__ == "__main__":
    parcels_api()
