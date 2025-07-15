from sqlalchemy import null
from hoa_insights_surpriseaz.utils import (
    date_parser,
    file_renamer,
    file_copier,
    number_formatter,
)
from pathlib import Path
from datetime import datetime


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


def test_api_date() -> None:
    date: datetime = date_parser.api_date(null)
    print(date)


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


# MISC

# def test_delete_files():
#     pass

# def test_file_copier():
#     pass

# def test_mailer():
#     pass


def test_rename_files():
    # RENAME FILE
    assert (
        file_renamer.rename(
            old=Path(
                "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-ORIGINAL-PDF.pdf"
            ),
            new=Path(
                "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-RENAMED-PDF.pdf"
            ),
        )
        == 1
    )
    # RENAME BACK
    assert (
        file_renamer.rename(
            old=Path(
                "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-RENAMED-PDF.pdf"
            ),
            new=Path(
                "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-ORIGINAL-PDF.pdf"
            ),
        )
        == 1
    )
