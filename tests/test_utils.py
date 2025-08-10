from hoa_insights_surpriseaz.utils import (
    date_parser,
    file_renamer,
    file_copier,
    number_formatter,
)
from pathlib import Path
from sqlalchemy import null
from datetime import datetime

TEST_ORIG_PDF_FILENAME: str = "TEST-MANAGEMENT.pdf"
TEST_RENAMED_PDF_FILENAME: str = "TEST-RENAMED-MANAGEMENT.pdf"
TEST_ORIG_CSV_FILENAME: str = "test-surpriseaz-hoa-management.csv"
CSV_FILENAME: str = "test-renamed-surpriseaz-hoa-management.csv"

# DATE PARSER
def test_date_parser() -> None:
    date = date_parser.logger_date()
    assert "-" in date


def test_sql_date() -> None:
    date = date_parser.sql_date()
    print(date)


def test_sql_timestamp() -> None:
    date = date_parser.get_now()
    print(date)


def test_format_api_date() -> None:
    no_date: datetime = date_parser.api_date("")
    assert no_date == datetime(1901, 1, 1, 0, 0)

    has_date: datetime = date_parser.api_date("2025-08-09")
    assert has_date == datetime(2025, 8, 9, 0, 0)


def test_first_tuesday() -> None:
    first_tuesday = date_parser.first_tuesday_of_month()
    print(first_tuesday)
    assert not first_tuesday


# NUMBER FORMATTER
def test_number_formatter() -> None:
    num = number_formatter.format_apn("50911455")
    assert num == "509-11-455"
    num = number_formatter.format_phone("6023153315")
    assert num == "(602) 315-3315"
    num = number_formatter.format_phone("~~~~~~~~~~")
    assert num == "(999) 999-9999"


# FILE RENAME
def test_rename_files():
    tests_path = Path.cwd() / "tests" / "output" / "pdf"

    # RENAME ORIG
    assert (
        file_renamer.rename(
            tests_path / TEST_ORIG_PDF_FILENAME, tests_path / TEST_RENAMED_PDF_FILENAME
        )
        == 1
    )

    # RENAME BACK
    assert (
        file_renamer.rename(
            tests_path / TEST_RENAMED_PDF_FILENAME, tests_path / TEST_ORIG_PDF_FILENAME
        )
        == 1
    )


# TODO finish util testing
# def test_file_copier():
#     file_copier.to_folder(CSV_PATH/CSV_FILENAME, Path().parent / "output")


# def test_delete_files():
#     pass


# def test_mailer():
#     pass
