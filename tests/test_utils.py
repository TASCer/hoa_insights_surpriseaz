from sqlalchemy import null
from hoa_insights_surpriseaz.utils import date_parser, number_formatter


# DATE PARSER
def test_date_parser():
    date = date_parser.logger_date()
    assert "-" in date


def test_sql_date():
    date = date_parser.sql_date()
    print(date)


def test_sql_timestamp():
    date = date_parser.get_now()
    print(date)


def test_api_date():
    date = date_parser.api_date(null)
    print(date)


def test_first_tuesday():
    first_tuesday = date_parser.first_tuesday_of_month()
    print(first_tuesday)
    assert not first_tuesday


# NUMBER FORMATTER
def test_number_formatter():
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

# def test_rename_files():
#     pass
