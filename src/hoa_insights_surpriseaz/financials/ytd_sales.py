import logging
import pandas as pd

from hoa_insights_surpriseaz import create_reports
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.utils.number_parser import format_price
from hoa_insights_surpriseaz.utils.date_parser import year_to_date
from logging import Logger
from pandas import DataFrame
from pandas.core.generic import NDFrame
from sqlalchemy import create_engine, exc
from sqlalchemy.engine import Engine

ytd_start, ytd_end = year_to_date()

DB_HOSTNAME: str = f"{my_secrets.prod_debian_dbhost}"
DB_NAME: str = f"{my_secrets.prod_debian_dbname}"
DB_USER: str = f"{my_secrets.prod_debian_dbuser}"
DB_PW: str = f"{my_secrets.prod_debian_dbpass}"


def get_average_sale_price() -> None:
    """
    Function queries owners table data for YTD sales data.
    Creates dataframe of all YTD sales in all communities.
    Sends dataframe to create_reports.financial for procesing.
    """
    logger: Logger = logging.getLogger(__name__)
    try:
        engine: Engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOSTNAME}/{DB_NAME}"
        )

    except (exc.SQLAlchemyError, exc.OperationalError, exc.ProgrammingError) as e:
        logger.critical(e)
        engine: Engine = None

    with engine.connect() as conn, conn.begin():
        try:
            all_sales_ytd: DataFrame = pd.read_sql(
                f"""SELECT 
				p.COMMUNITY,
				o.SALE_DATE,
				o.SALE_PRICE

				FROM
				owners o 
				INNER JOIN parcels p ON p.APN = o.APN
				where o.SALE_DATE >= '{ytd_start}' and o.SALE_DATE < '{ytd_end}';""",
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

        return None

    all_community_sales_ytd: DataFrame = pd.DataFrame(all_sales_ytd)
    all_community_sales_ytd.to_csv(
        f"{my_secrets.csv_finance_path}all_ytd_community_sales.csv"
    )

    community_sold_count: NDFrame = all_community_sales_ytd.groupby("COMMUNITY").count()
    community_sold_count: NDFrame = community_sold_count.rename(
        columns={"SALE_DATE": "#Sold"}
    )

    ytd_avg_price: DataFrame = all_community_sales_ytd.groupby(["COMMUNITY"]).mean(
        ["SALE_PRICE"]
    )

    ytd_avg_price: DataFrame = ytd_avg_price.rename(columns={"SALE_PRICE": "Avg_Price"})

    ytd_community_avg_sale_price: DataFrame = pd.concat(
        [community_sold_count, ytd_avg_price], axis=1
    )
    del ytd_community_avg_sale_price["SALE_PRICE"]

    ytd_community_avg_sale_price["Avg_Price"] = ytd_community_avg_sale_price[
        "Avg_Price"
    ].apply(format_price)

    ytd_community_avg_sale_price.reset_index(inplace=True)
    ytd_community_avg_sale_price.to_csv(
        f"{my_secrets.csv_finance_path}ytd_community_avg_sale_price.csv"
    )

    create_reports.financials(ytd_community_avg_sale_price)


if __name__ == "__main__":
    print(get_average_sale_price())
