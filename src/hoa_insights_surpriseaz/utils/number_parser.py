import re


def parse_apn(apn: str) -> str:
    """
    Takes an unformatted APN value (xxxxxxxx) from API
    Returns a formatted xxx-xx-xxx str
    """
    apn: str = re.sub(r"(\d{3})(\d{2})(\d{3})", r"\1-\2-\3", apn)

    return apn


def parse_ph_nums(num: str) -> str:
    """
    Takes phone number field data reponse from API
    Returns a formatted (xxx) xxx-xxxx number, empty fields are all 9's
    """
    if num == "~~~~~~~~~~" or num is None:
        num: str = "9999999999"

    num: str = re.sub(r"(\d{3})(\d{3})(\d{4})", r"(\1) \2-\3", num)

    return num


def format_price(price: int) -> str:
    """
    Returns formatted price str in $USD
    ex: 534650 -> $534,650
    """
    price = int(price)
    return "${:,}".format(price)
