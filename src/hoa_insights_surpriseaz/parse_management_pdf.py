import logging
import pandas as pd
import tabula

from logging import Logger
from pandas import DataFrame
# from test_hoa_surpriseaz import update_management

logger: Logger = logging.getLogger(__name__)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

header: list = [
    "HOA",
    "MANAGEMENT",
    "BOARD SITUS",
    "BOARD CITY",
    "CONTACT_ADX",
    "CONTACT_PH",
]

csv_filename: str = r"./output/csv/surpriseaz-hoa-management.csv"
pdf_filename: str = r"./output/pdf/MANAGEMENT.pdf"


def parse_csv(filename: str) -> None:
    """
    Function takes in a csv filename and creates Pandas dataframe.
    Renames columns and cleans data in dataframe.
    Saves csv file to disk.
    """
    logger.info(f"Parsing csv file: {csv_filename}")

    try:
        managers: DataFrame = pd.read_csv(filename, header=0)
    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)

    managers.rename(
        columns={
            "Board Address (ACC Listed)": header[2],
            "City/Zip": header[3],
            "HOA Name": header[0],
            "Contact Email/Website": header[4],
            "Management Company": header[1],
            "Telephone": header[-1],
        },
        inplace=True,
    )

    #   clean HOA COMMUNITY NAMES
    managers["HOA"] = managers["HOA"].str.replace(" Homeowners Association", "")
    managers["HOA"] = managers["HOA"].str.replace(" Community Association", "")
    managers["HOA"] = managers["HOA"].str.replace(" Community", "")
    managers["HOA"] = managers["HOA"].str.replace(" Association", "")
    managers["HOA"] = managers["HOA"].str.replace("at Surprise ", "")
    managers["HOA"] = managers["HOA"].str.replace("Owners", "")
    managers["HOA"] = managers["HOA"].str.replace(" HOA", "")
    managers["HOA"] = managers["HOA"].str.rstrip()

    #   clean management company name
    managers["MANAGEMENT"] = managers["MANAGEMENT"].str.replace(",", "")
    managers.drop(managers.columns[[1]], axis=1, inplace=True)

    logger.info("Parsing csv complete")

    managers.to_csv(filename)


def convert_pdf(*args) -> None:
    """
    Function converts the downloaded pdf document's table data to csv.
    Sends the csv file to parse_csv() for formatting/parsing/saving.
    """
    logger.info(f"Converting pdf file: {pdf_filename} to csv")

    try:
        tabula.convert_into(
            pdf_filename, csv_filename, output_format="csv", pages="all"
        )

    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        exit()

    logger.info("Converting pdf file to csv complete.")

    parse_csv(csv_filename)

    return csv_filename


if __name__ == "__main__":
    # filename: str = "./output/pdf/MANAGEMENT.pdf"
    convert_pdf()
    # filename: str = "./output/pdf/MANAGEMENT.pdf"
    # parse_csv(csv_filename)
