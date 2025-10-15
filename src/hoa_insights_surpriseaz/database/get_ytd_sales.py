import logging

from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.utils.number_formatter import format_price

from logging import Logger
from pandas import DataFrame, read_sql, concat
from pathlib import Path
from sqlalchemy import create_engine, exc
from sqlalchemy.engine import Engine

DB_HOSTNAME: str = f"{my_secrets.prod_debian_dbhost}"
DB_NAME: str = f"{my_secrets.prod_debian_dbname}"
DB_USER: str = f"{my_secrets.prod_debian_dbuser}"
DB_PW: str = f"{my_secrets.prod_debian_dbpass}"


def get_average_sale_price(finances: Path) -> DataFrame:
    """
    Function determines the YTD average parcel sale price for each community.

    :param finances: financial csv diretory
    :return: communities avgerage sale price YTD
    """
    logger: Logger = logging.getLogger(__name__)
    try:
        engine: Engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOSTNAME}/{DB_NAME}"
        )

    except (exc.SQLAlchemyError, exc.OperationalError, exc.ProgrammingError) as e:
        logger.critical(e)

    with engine.connect() as conn, conn.begin():
        try:
            all_sales_ytd: DataFrame = read_sql(
                """SELECT 
                    *
				FROM
				community_sales 
				;""",
                con=conn,
                parse_dates=[1],
                coerce_float=False,
            )
            all_sales_ytd.dropna(inplace=True)

        except KeyError as e:
            logger.critical(str(e))
            exit()

    if all_sales_ytd.empty:
        logger.info("NO SALES YET THIS YEAR")

        return DataFrame()

    all_community_sales_ytd: DataFrame = DataFrame(all_sales_ytd)
    all_community_sales_ytd.to_csv(f"{finances / 'all_ytd_community_sales.csv'}")

    community_sold_count: DataFrame = all_community_sales_ytd.groupby(
        "COMMUNITY"
    ).count()
    community_sold_count: DataFrame = community_sold_count.rename(
        columns={"SALE_DATE": "#Sold"}
    )

    ytd_avg_price: DataFrame = all_community_sales_ytd.groupby(by=["COMMUNITY"]).mean(
        ["SALE_PRICE"]
    )

    ytd_avg_price: DataFrame = ytd_avg_price.rename(columns={"SALE_PRICE": "Avg_Price"})

    ytd_community_avg_sale_price: DataFrame = concat(
        [community_sold_count, ytd_avg_price], axis=1
    )
    del ytd_community_avg_sale_price["SALE_PRICE"]

    ytd_community_avg_sale_price["Avg_Price"] = ytd_community_avg_sale_price[
        "Avg_Price"
    ].apply(format_price)

    ytd_community_avg_sale_price.reset_index(inplace=True)
    ytd_community_avg_sale_price.to_csv(
        f"{f'{finances / "ytd_community_avg_sale_price.csv"}'}"
    )

    return ytd_community_avg_sale_price
