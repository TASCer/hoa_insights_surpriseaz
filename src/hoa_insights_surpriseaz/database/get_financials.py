import logging
import sys
from logging import Logger
from pathlib import Path

# from dotenv import load_dotenv
from pandas import DataFrame, read_sql
from sqlalchemy import create_engine, exc
from sqlalchemy.engine import Engine

from hoa_insights_surpriseaz.database.config import PROD_LOCAL_DB_URI
from hoa_insights_surpriseaz.utils.number_formatter import format_price


def average_sale_prices(finances: Path) -> DataFrame:
    """
    Function determines the YTD average parcel sale price for each community.

    :param finances: financial csv directory
    :return: communities average sale price YTD
    """
    logger: Logger = logging.getLogger(__name__)
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{PROD_LOCAL_DB_URI}")

    except (exc.SQLAlchemyError, exc.OperationalError, exc.ProgrammingError) as e:
        logger.critical(e)

    with engine.connect() as conn, conn.begin():
        q_ytd_sales = """SELECT * FROM community_sales;"""
        q_communities = """SELECT COMMUNITY, COUNT FROM communities"""
        try:
            all_sales_ytd: DataFrame = read_sql(
                q_ytd_sales,
                con=conn,
                parse_dates=[1],
                coerce_float=False,
            )
            all_sales_ytd.dropna(inplace=True)

            community_totals = read_sql(
                q_communities,
                con=conn,
                coerce_float=False,
            )

        except KeyError as e:
            logger.critical(str(e))
            sys.exit()

    if all_sales_ytd.empty:
        logger.info("NO SALES YET THIS YEAR")

        return DataFrame()

    all_community_sales_ytd: DataFrame = DataFrame(all_sales_ytd)
    all_community_sales_ytd.to_csv(f"{finances / 'all_ytd_community_sales.csv'}")

    ytd_community_avg_sale_price: DataFrame = all_community_sales_ytd.groupby(
        by="COMMUNITY"
    ).agg({"SALE_DATE": "count", "SALE_PRICE": "mean"})

    ytd_community_avg_sale_price: DataFrame = ytd_community_avg_sale_price.rename(
        columns={"SALE_PRICE": "Avg_Price", "SALE_DATE": "#SOLD"}
    )

    ytd_community_avg_sale_price["Avg_Price"] = ytd_community_avg_sale_price[
        "Avg_Price"
    ].apply(format_price)

    ytd_community_avg_sale_price.reset_index(inplace=True)

    ytd_community_avg_sale_price = ytd_community_avg_sale_price.merge(
        community_totals, on="COMMUNITY"
    )
    ytd_community_avg_sale_price = ytd_community_avg_sale_price.round(2)

    ytd_community_avg_sale_price["MANAGED_ID"] = (
        (
            ytd_community_avg_sale_price["#SOLD"]
            / ytd_community_avg_sale_price["COUNT"]
            * 100
        )
        .round(decimals=2)
        .map(lambda x: f"{x:g}")
    )

    ytd_community_avg_sale_price = ytd_community_avg_sale_price.rename(
        columns={"MANAGED_ID": "%SOLD", "COUNT": "PARCELS"}
    )

    col2move = ytd_community_avg_sale_price.pop("PARCELS")
    ytd_community_avg_sale_price.insert(1, "PARCELS", col2move)

    ytd_community_avg_sale_price.to_csv(
        f"{f'{finances / "ytd_community_avg_sale_price.csv"}'}"
    )

    return ytd_community_avg_sale_price
