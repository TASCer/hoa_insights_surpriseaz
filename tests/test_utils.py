import pytest

from datetime import datetime

from hoa_insights_surpriseaz.utils import (
    date_parser,
    file_renamer,
    file_copier,
    number_formatter,
)
from pathlib import Path
from sqlalchemy import null
from datetime import datetime as dt

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
    assert date == dt.today().date()


def test_sql_timestamp() -> None:
    date = date_parser.get_now()
    assert dt.isoformat(date)


def test_format_api_date() -> None:
    no_date: datetime = date_parser.api_date("")
    assert no_date == dt(1901, 1, 1, 0, 0)

    has_date: datetime = date_parser.api_date("2025-08-09")
    assert has_date == dt(2025, 8, 9, 0, 0)


def test_first_tuesday() -> None:
    first_tuesday = date_parser.first_tuesday_of_month()

    assert not first_tuesday, "Is today the 1st Tuesday of this month?"


# APN NUMBER FORMATTER
@pytest.mark.parametrize(
    "apn_before, len_before, apn_after, len_after",
    [("50911455", 8, "509-11-455", 10), ("50911600", 8, "509-11-600", 10)],
)
def test_apn_formatter(apn_before, len_before, apn_after, len_after) -> None:
    assert apn_before.isdigit() is True
    assert len_before == 8
    apn_after: str = number_formatter.format_apn(apn_before)
    assert len_after == 10
    assert apn_after == apn_after
    assert "-" in apn_after
    assert apn_after.isdigit() is False


# PHONE NUMBER FORMATTER
@pytest.mark.parametrize(
    "ph_num, expected",
    [
        ("6023153315", "(602) 315-3315"),
        ("3038889999", "(303) 888-9999"),
        ("9999999999", "(999) 999-9999"),
        ("", ""),
    ],
)
def test_phones(ph_num, expected):
    ph_num = number_formatter.format_phone(ph_num)
    assert ph_num == expected


# FILE RENAME
@pytest.mark.skip("WIP")
def test_rename_files() -> None:
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
@pytest.mark.skip("WIP")
def test_file_copier():
    file_copier.to_folder(
        TEST_ORIG_CSV_FILENAME / CSV_FILENAME, Path().parent / "output"
    )


@pytest.mark.skip("WIP")
def test_delete_files():
    pass


@pytest.mark.skip("WIP")
def test_mailer():
    pass
