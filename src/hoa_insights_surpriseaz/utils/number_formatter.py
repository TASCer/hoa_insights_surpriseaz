import re


def format_apn(apn: str) -> str:
    """
    Function formats Assessor Parcel Number (APN) response from API.

    Args:
        apn (str):

    Returns:
        str:

    Example:
        "50911455" -> "509-11-455".
    """
    apn: str = re.sub(r"(\d{3})(\d{2})(\d{3})", r"\1-\2-\3", apn)

    return apn


def format_phone(num: str) -> str:
    """
    Function formats phone number field reponse from API.

    Args:
        num (str):

    Returns:
        str:

    Example:
        "1234567890" -> "(123) 456-7890"
        "" -> "(999) 999-9999"

    """
    if num == "~~~~~~~~~~" or num is None:
        num: str = "9999999999"

    num: str = re.sub(r"(\d{3})(\d{3})(\d{4})", r"(\1) \2-\3", num)

    return num


def format_price(price: int) -> str:
    """
    Function formats integers.

    Args:
        price (int):

    Returns:
        str: used for reports

    Example:
        534650 -> $534,650
    """
    price = int(price)
    return "${:,}".format(price)


if __name__ == "__main__":
    print(format_apn("50911455"))
    print(format_phone("6023153315"))
    print(format_price(50911455))
    print(format_phone("~~~~~~~~~~"))
