import logging

import tabula

from logging import Logger
from pandas import DataFrame, read_csv
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

FILE_HEADER: list = [
    "HOA",
    "MANAGEMENT",
    "BOARD SITUS",
    "BOARD CITY",
    "CONTACT_ADX",
    "CONTACT_PH",
]


def parse_csv(file: Path) -> Path:
    """
    Function parses, format, and cleans csv file converted from pdf download.

    :param file: converted management csv file
    :return: parsed converted csv file
    """
    logger.info(f"Parsing csv file: {file.name}")

    try:
        managers: DataFrame = read_csv(file, header=0)
    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)

    managers.rename(
        columns={
            "Board Address (ACC Listed)": FILE_HEADER[2],
            "City/Zip": FILE_HEADER[3],
            "HOA Name": FILE_HEADER[0],
            "Contact Email/Website": FILE_HEADER[4],
            "Management Company": FILE_HEADER[1],
            "Telephone": FILE_HEADER[-1],
        },
        inplace=True,
    )

    # CLEANING HOA COMMUNITY NAMES
    managers["HOA"] = managers["HOA"].str.replace(" Homeowners Association", "")
    managers["HOA"] = managers["HOA"].str.replace(" Community Association", "")
    managers["HOA"] = managers["HOA"].str.replace(" Community", "")
    managers["HOA"] = managers["HOA"].str.replace(" Association", "")
    managers["HOA"] = managers["HOA"].str.replace("at Surprise ", "")
    managers["HOA"] = managers["HOA"].str.replace("Owners", "")
    managers["HOA"] = managers["HOA"].str.replace(" HOA", "")
    managers["HOA"] = managers["HOA"].str.rstrip()

    # CLEANING HOA MANAGEMENT COMPANY NAMES
    managers["MANAGEMENT"] = managers["MANAGEMENT"].str.replace(",", "")
    managers.drop(managers.columns[[1]], axis=1, inplace=True)

    logger.info("Parsing csv complete")

    managers.to_csv(file)

    return file


def pdf_to_csv(pdf_file: Path, csv_file: Path) -> Path:
    """
    Function converts the downloaded pdf document's table data to a csv file.

    :param pdf_file: downloaded pdf file
    :param csv_file: csv file to convert pdf file into
    :return: converte csv_file
    """
    logger.info(f"Convert: {pdf_file.name} -> {csv_file.name}")

    try:
        tabula.convert_into(
            str(pdf_file), str(csv_file), output_format="csv", pages="all"
        )

    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        exit()

    logger.info(f"Convert Complete")

    parsed_csv: Path = parse_csv(csv_file)

    return parsed_csv


if __name__ == "__main__":
    CSV_PATH: Path = Path.cwd() / "output" / "csv"
    CSV_FILENAME: str = "surpriseaz-hoa-management.csv"
    PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
    PDF_PATH: Path = Path.cwd() / "output" / "pdf"

    pdf_to_csv(pdf_file=PDF_PATH / PDF_NEW_FILENAME, csv_file=CSV_PATH / CSV_FILENAME)
