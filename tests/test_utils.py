from sqlalchemy import null
from hoa_insights_surpriseaz.utils import date_parser, number_formatter


def test_date_parser():
    date = date_parser.log_date()
    assert "-" in date


def test_sql_date():
    date = date_parser.sql_date()
    print(date)


def test_sql_timestamp():
    date = date_parser.sql_timestamp()
    print(date)


def test_api_date():
    date = date_parser.api_date(null)
    print(date)


def test_number_formatter():
    num = number_formatter.format_apn("50911455")
    assert num == "509-11-455"
    num = number_formatter.format_phone("6023153315")
    assert num == "(602) 315-3315"


    # print(last_saturday_of_month())
    # print(first_tuesday_of_month())
    # print(format_apn("50911455"))
    # print(format_phone("6023153315"))
    # print(format_price("50911455"))
    # print(format_phone("~~~~~~~~~~"))
