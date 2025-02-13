import aiohttp
import asyncio
import json
import logging
import platform

from aiohttp import TCPConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from asyncio import Semaphore, Task
from logging import Logger
from sqlalchemy import Engine, TextClause, create_engine, exc, text, CursorResult, Row
from hoa_insights_surpriseaz.utils import date_parser
from hoa_insights_surpriseaz import my_secrets

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"
LOCAL_DB_NAME: str = f"{my_secrets.prod_debian_dbname}"

PARCELS_TABLE: str = "parcels"

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

API_HEADER: dict[str, str] = {my_secrets.api_header_type: my_secrets.api_header_creds}


def get_parcel_apns() -> tuple[str]:
    """
    Function retrieves the APN of all parcels from database.
    Returns tuple of APNs and db engine.
    """
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}")
        with engine.connect() as conn, conn.begin():
            result: TextClause = conn.execute(
                text(f"SELECT APN FROM {LOCAL_DB_NAME}.{PARCELS_TABLE};")
            )
            all_results: CursorResult = result.all()
            APNs: list[Row] = [x[0] for x in all_results]

        return APNs

    except exc.OperationalError as oe:
        logger.error(f"{oe.__cause__}")
        logger.warning(
            "*** check server or run 'uv run db-init.py' from database/setup dir. ***"
        )
        logger.info("\t\tlogfile: '__rdbms-creation__.log' will be created.")
        print(
            f"** ISSUE: check log: '{date_parser.log_date()}.log'. If initial setup, run 'uv run db-init.py' from database/setup dir. **"
        )
        exit()

    except BaseException as be:
        logger.error(f"{be}")
        print(be)
        exit()


def parcels_api() -> tuple[dict]:
    """
    Function gets each community parcel APN from database.
    Fetches latest data for APN from Accessor API.
    Returns tuple of api results as dict.
    """
    APNS: list[str] = get_parcel_apns()
    logger.info("Accessing Assessor API to get latest parcel data")
    consumed_parcel_data: tuple[dict] = asyncio.run(async_main(APNS))
    logger.info("All latest parcel data consumed from API")

    return consumed_parcel_data


async def get_parcel_details(client: RetryClient, sem: Semaphore, url: str) -> dict:
    """
    Function takes an api retry client, semaphore, and url to get latest parcel data from API endpoint.
    Returns a dictionary object
    """
    try:
        async with sem, client.get(url) as resp:
            parcel_details: dict = await resp.json()
            if resp.status != 200:
                print(url, resp.status)
            return parcel_details

    except aiohttp.client_exceptions.ClientOSError as os:
        logger.error(f"{os} - {url}")

        return exit()

    except (
        json.JSONDecodeError,
        aiohttp.client.ContentTypeError,
        aiohttp.ClientResponseError,
        TypeError,
        aiohttp.ClientPayloadError,
    ) as e:
        logger.warning(f"{url} -  {e} ")

        await asyncio.sleep(4)

        async with sem, client.get(url) as resp:
            parcel_details: dict = await resp.json()
            logger.warning(f"{url} {e} -- After Retry")

        return parcel_details


async def async_main(apns: list) -> list[dict]:
    """
    Function takes in a list of APN's.
    Creates API connection and retry client.
    Iterates through list of APN's creating get_parcel_details tasks.
    Returns a tuple of dictionary objects for each parcel processed.
    """
    connector: TCPConnector = TCPConnector(
        ssl=False, limit=40, limit_per_host=40, enable_cleanup_closed=False
    )
    async with RetryClient(
        headers=API_HEADER,
        connector=connector,
        raise_for_status=True,
        retry_options=ExponentialRetry(attempts=3),
    ) as retry_client:
        sem: Semaphore = asyncio.Semaphore(40)
        tasks: list[Task[object]] = []
        for apn in apns:
            parcel_url: str = f"https://mcassessor.maricopa.gov/parcel/{apn}"
            tasks.append(
                asyncio.create_task(get_parcel_details(retry_client, sem, parcel_url))
            )

        parcels: list = await asyncio.gather(*tasks, return_exceptions=True)

        return parcels


if __name__ == "__main__":
    print(parcels_api())
