import logging
import sys
from logging import Logger
from pathlib import Path

import tabula
from pandas import DataFrame, read_csv

logger: Logger = logging.getLogger(__name__)


ORIGINAL_PDF_COLUMN_COUNT = 7
NEW_FILE_HEADER: list = [
    "HOA",
    "MANAGEMENT",
    "BOARD SITUS",
    "BOARD CITY",
    "CONTACT_ADX",
    "CONTACT_PH",
]


def parse_csv(file: Path) -> Path:
    """
    Function parses, formats, and cleans file.

    :param file: management csv file (converted from downloaded pdf)
    :return: parsed converted csv file
    """
    logger.info(f"Parsing csv file: {file.name}")

    try:
        managers: DataFrame = read_csv(file, header=0)
    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)

    original_file_header = list(managers.columns)

    if len(original_file_header) < ORIGINAL_PDF_COLUMN_COUNT:
        logger.warning("file does not have original number of columns")
        logger.warning(
            f"expected: {ORIGINAL_PDF_COLUMN_COUNT} converted: {len(managers.columns)}"
        )
        logger.warning("ASSUMING last 2 columns were inadverently merged")

        managers["MANAGEMENT"] = managers["Contact Email/Website Management Company"]
        managers.rename(
            columns={"Contact Email/Website Management Company": "CONTACT_ADX"}
        )

        managers.rename(
            columns={
                original_file_header[0]: NEW_FILE_HEADER[0],
                original_file_header[2]: NEW_FILE_HEADER[2],
                original_file_header[3]: NEW_FILE_HEADER[3],
                original_file_header[4]: NEW_FILE_HEADER[-1],
                original_file_header[5]: NEW_FILE_HEADER[4],
            },
            inplace=True,
        )
        # split the inadvertently merged coluimns
        managers["CONTACT_ADX"] = managers["CONTACT_ADX"].apply(
            lambda x: x.split(" ", 1)[0]
        )
        managers["MANAGEMENT"] = managers["MANAGEMENT"].apply(
            lambda x: x.split(" ", 1)[1] if len(x.split()) > 1 else x
        )

    else:
        managers.rename(
            columns={
                original_file_header[0]: NEW_FILE_HEADER[0],
                original_file_header[2]: NEW_FILE_HEADER[2],
                original_file_header[3]: NEW_FILE_HEADER[3],
                original_file_header[4]: NEW_FILE_HEADER[-1],
                original_file_header[5]: NEW_FILE_HEADER[4],
                original_file_header[6]: NEW_FILE_HEADER[1],
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

    managers.to_csv(file)

    logger.info("Parsing csv complete")

    return file


def pdf_to_csv(pdf_file: Path, csv_file: Path) -> Path:
    """
    Function converts the downloaded pdf document's table data to a csv file.

    :param pdf_file: downloaded pdf file
    :param csv_file: csv file to convert pdf file into
    :return: converted csv_file
    """
    logger.info(f"Converting: {pdf_file.name} -> {csv_file.name}")
    try:
        tabula.convert_into(
            str(pdf_file), str(csv_file), output_format="csv", pages="all"
        )

    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        sys.exit()

    logger.info("Conversion Complete")

    parsed_csv: Path = parse_csv(csv_file)

    return parsed_csv


if __name__ == "__main__":
    CSV_PATH: Path = Path.cwd() / "database" / "setup" / "seed_data"
    CSV_FILENAME: str = "surpriseaz-hoa-management.csv"
    PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
    PDF_PATH: Path = Path.cwd().parent.parent / "tests" / "input"

    pdf_to_csv(pdf_file=PDF_PATH / PDF_NEW_FILENAME, csv_file=CSV_PATH / CSV_FILENAME)
    # parse_csv(file=CSV_PATH / CSV_FILENAME)
