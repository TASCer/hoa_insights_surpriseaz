import logging

import tabula

from logging import Logger
from pandas import DataFrame, read_csv
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

header: list = [
    "HOA",
    "MANAGEMENT",
    "BOARD SITUS",
    "BOARD CITY",
    "CONTACT_ADX",
    "CONTACT_PH",
]


def parse_csv(file: Path) -> Path:
    """
    Function takes in a path for a csv file and creates a dataframe.
    Renames columns and cleans data.
    Saves csv file to disk and returns path.
    """
    logger.info(f"Parsing csv file: {file.name}")

    try:
        managers: DataFrame = read_csv(file, header=0)
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
    Function converts the downloaded pdf document's table data to csv.
    Sends the csv file to parse_csv() for formatting/parsing/saving.
    """
    logger.info(f"Converting {pdf_file.name}  to {csv_file.name} ")

    try:
        tabula.convert_into(
            str(pdf_file), str(csv_file), output_format="csv", pages="all"
        )

    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        exit()

    logger.info("Converting pdf file to csv complete.")

    parsed_csv: str = parse_csv(csv_file)

    return parsed_csv


if __name__ == "__main__":
    CSV_PATH: Path = Path.cwd() / "output" / "csv"
    CSV_FILENAME: str = "surpriseaz-hoa-management.csv"
    PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
    PDF_PATH: Path = Path.cwd() / "output" / "pdf"

    pdf_to_csv(pdf_file=PDF_PATH / PDF_NEW_FILENAME, csv_file=CSV_PATH / CSV_FILENAME)
