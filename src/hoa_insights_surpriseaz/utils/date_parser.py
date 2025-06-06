import calendar
import datetime as dt

from datetime import date
from dateutil.parser import parse


def logger_date() -> str:
    """
    Function uses datetime.date.today object
    Returns formatted str for logger's log files.
    """
    now: date = dt.date.today()
    todays_date: str = now.strftime("%D").replace("/", "-")

    return todays_date


def sql_date() -> date:
    """
    Function returns todays date for historical mysql table timestamp (TS) col.
    """
    todays_date: date = dt.date.today()

    return todays_date


def get_now() -> dt:
    """
    Function returns current datetime.
    used for 'latest_update' table located on remote website.
    """
    now: dt = dt.datetime.now()

    return now


# KEEP in case need for another automated monthly task
# def last_saturday_of_month() -> int:
#     """
#     Application is scheduled to run every Tuesday and Saturday morning @ 2am.
#     Function determines the date for the LAST SATURDAY of each month.
#     Used to update HOA management data monthly.
#     Returns date as int.
#     """
#     cur_year = dt.date.today().year
#     cur_month = dt.date.today().month
#     cur_month_calendar = calendar.monthcalendar(year=cur_year, month=cur_month)

#     last_saturday: int = max(
#         cur_month_calendar[-1][calendar.SATURDAY], cur_month_calendar[-2][calendar.SATURDAY]
#     )

#     return last_saturday


def first_tuesday_of_month() -> bool:
    """
    Function determines if today is the FIRST TUESDAY of this month.
    Used to update HOA management data on a monthly during a scheduled run.
    """
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    current_month_calendar = calendar.monthcalendar(
        year=current_year, month=current_month
    )
    first_tuesday_date: int = max(
        current_month_calendar[0][calendar.TUESDAY],
        current_month_calendar[1][calendar.TUESDAY],
    )

    is_today_first_tuesday: bool = (
        int(logger_date().split("-")[1]) == first_tuesday_date
    )

    return is_today_first_tuesday


def api_date(date: str) -> dt.datetime:
    """
    Function takes a date from API fetch result.
    Returns formatted str for mysql date fields.
    If date not parseable, returns "1901-01-01".
    """
    try:
        date_parsed: dt.datetime = parse(date)

    except TypeError:
        date_parsed = parse("1901-01-01")

    return date_parsed


def year_to_date() -> tuple[str]:
    """
    Function returns str representing current year and next year and appends "-01-01" to them.
    Used for YTD Sales table query.
    i.e. 2024-04-01, 2025-01-01.
    """
    now: date = dt.datetime.now()
    ytd_start: str = f"{now.year}-01-01"
    ytd_end: str = f"{now.year + 1}-01-01"

    return ytd_start, ytd_end


if __name__ == "__main__":
    # print(last_saturday_of_month())
    print(api_date({}))
    # print(sql_timestamp())
    # print(sql_date())
    # print(log_date())
    # print(f"{}")
