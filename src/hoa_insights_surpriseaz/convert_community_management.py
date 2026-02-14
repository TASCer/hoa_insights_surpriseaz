import logging
import tabula

from logging import Logger
from pandas import DataFrame, read_csv
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

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
    Function parses, formats, and cleans csv file converted from pdf download.

    :param file: management csv file (converted from downloaded pdf)
    :return: parsed converted csv file
    """
    logger.info(f"Parsing csv file: {file.name}")

    try:
        managers: DataFrame = read_csv(file, header=0)
    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)

    original_file_header = list(managers.columns)
    original_file_header = [h.replace('"', '') for h in original_file_header]

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

    ### FIX for page 2 pdf conversion issue.contact_adx field null and phone had adx field combined ###
    # fill missing adx with combined phone field
    # managers["CONTACT_ADX"] = managers["CONTACT_ADX"].fillna(managers["CONTACT_PH"])
    # split combined phone field to leave phone number
    # managers["CONTACT_PH"] = managers["CONTACT_PH"].str.rsplit(pat=" ").str.get(0)
    # find combined adx fields
    # mask_bad_address = managers["CONTACT_ADX"].str.contains("^[1-9]", na=False)
    # remove phone number from adx field
    # fix_address = (
    #     managers.loc[mask_bad_address]["CONTACT_ADX"]
    #     .str.rsplit(pat=" ", n=1)
    #     .str.get(1)
    # )
    # TODO https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html#chained-assignment
    # managers["CONTACT_ADX"][mask_bad_address] = fix_address

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
    logger.info(f"Convert: {pdf_file.name} -> {csv_file.name}")
    try:
        tabula.convert_into(
            str(pdf_file), str(csv_file), output_format="csv", pages="all"
        )

    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        exit()

    logger.info("Convert Complete")

    parsed_csv: Path = parse_csv(csv_file)

    return parsed_csv


if __name__ == "__main__":
    CSV_PATH: Path = Path.cwd() / "output" / "csv"
    CSV_FILENAME: str = "surpriseaz-hoa-management.csv"
    PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
    PDF_PATH: Path = Path.cwd() / "output" / "pdf"

    pdf_to_csv(pdf_file=PDF_PATH / PDF_NEW_FILENAME, csv_file=CSV_PATH / CSV_FILENAME)
    # parse_csv(file=CSV_PATH / CSV_FILENAME)
