import calendar
import datetime as dt

from datetime import date, datetime
from dateutil.parser import parse, ParserError


def logger_date() -> str:
    """
    Function retieves today datetime date object and formats for logger file.

    Returns:
        str: today's date
    
    Example:
        datetime.date(2025, 1, 25) -> '01-25-26' 
    """
    todays_date: str = get_now().strftime("%D").replace("/", "-")

    return todays_date


def sql_date() -> date:
    """
    Function provides today's date used for historical table timestamp (TS) columns

    Returns:
        date: todays date
    """
    todays_date: date = dt.date.today()

    return todays_date


def get_now() -> datetime:
    """
    Function gets datetime.now at time of invocation.

    Returns:
        datetime: used for 'latest_update' table located on remote website.

    """
    now: datetime = dt.datetime.now()

    return now


def first_tuesday_of_month() -> bool:
    """
    Function determines if today is the FIRST TUESDAY of this month.

    Returns:
        bool: If true, updates HOA management data.

    """
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    current_month_calendar = calendar.monthcalendar(
        year=current_year, month=current_month
    )

    first_tuesday_date: int = min(
        current_month_calendar[0][calendar.TUESDAY],
        current_month_calendar[1][calendar.TUESDAY],
    )

    if first_tuesday_date == 0:
        first_tuesday_date: int = max(
            current_month_calendar[0][calendar.TUESDAY],
            current_month_calendar[1][calendar.TUESDAY],
        )

    is_today_first_tuesday: bool = (
        int(logger_date().split("-")[1]) == first_tuesday_date
    )

    return is_today_first_tuesday


def api_date(date: str) -> datetime:
    """
    Function parses date field from API fetch result.

    Args:
        date (str): date from API response

    Returns:
        datetime: parsed date or "1901-01-01"
    """
    try:
        date_parsed: datetime = parse(date)

    except (TypeError, ParserError):
        date_parsed: datetime = parse("1901-01-01")

    return date_parsed
